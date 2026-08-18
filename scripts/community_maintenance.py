"""Run the recurring, non-destructive community maintenance pass.

The pass keeps the issue and pull-request queue visible for human decisions;
it never merges code or closes a report automatically.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request


API = "https://api.github.com"
REPO = os.environ.get("GITHUB_REPOSITORY", "like-study1/Oh-My-DSH")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
MARKER = "<!-- community-maintenance:triage -->"

LABELS = {
    "社区维护": ("5319e7", "由定期社区维护流程登记"),
    "待审阅": ("0075ca", "等待维护者审阅"),
    "待作者": ("d93f0b", "等待提交者补充或修正"),
    "待分诊": ("fbca04", "等待维护者分诊"),
}


def api(method, path, payload=None):
    if not TOKEN:
        raise RuntimeError("GH_TOKEN or GITHUB_TOKEN is required")
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API + path,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "oh-my-dsh-community-maintenance",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def ensure_labels():
    for name, (color, description) in LABELS.items():
        encoded = urllib.parse.quote(name, safe="")
        if api("GET", f"/repos/{REPO}/labels/{encoded}") is None:
            api("POST", f"/repos/{REPO}/labels", {
                "name": name,
                "color": color,
                "description": description,
            })


def add_labels(number, labels):
    if labels:
        api("POST", f"/repos/{REPO}/issues/{number}/labels", {"labels": labels})


def has_marker(number):
    comments = api("GET", f"/repos/{REPO}/issues/{number}/comments?per_page=100") or []
    return any(MARKER in (comment.get("body") or "") for comment in comments)


def triage_pull_requests():
    pulls = api("GET", f"/repos/{REPO}/pulls?state=open&per_page=100") or []
    counts = {"待审阅": 0, "待作者": 0}
    for pull in pulls:
        reviews = api("GET", f"/repos/{REPO}/pulls/{pull['number']}/reviews?per_page=100") or []
        latest = {}
        for review in reviews:
            state = review.get("state")
            user = (review.get("user") or {}).get("login")
            if user and state in {"APPROVED", "CHANGES_REQUESTED"}:
                latest[user] = state
        status = "待作者" if "CHANGES_REQUESTED" in latest.values() else "待审阅"
        add_labels(pull["number"], ["社区维护", status])
        counts[status] += 1
    return len(pulls), counts


def triage_issues():
    issues = api("GET", f"/repos/{REPO}/issues?state=open&per_page=100") or []
    count = 0
    for issue in issues:
        if "pull_request" in issue:
            continue
        labels = {label.get("name") for label in issue.get("labels", [])}
        add_labels(issue["number"], ["社区维护", "待分诊"])
        if not labels and not has_marker(issue["number"]):
            api("POST", f"/repos/{REPO}/issues/{issue['number']}/comments", {
                "body": f"{MARKER}\n感谢反馈。社区维护流程已登记此 Issue，维护者会在分诊后跟进。"
            })
        count += 1
    return count


def main():
    ensure_labels()
    pull_count, pull_status = triage_pull_requests()
    issue_count = triage_issues()
    print(
        "community maintenance: "
        f"open PRs={pull_count} (待审阅={pull_status['待审阅']}, "
        f"待作者={pull_status['待作者']}), open issues={issue_count}"
    )


if __name__ == "__main__":
    main()
