# -*- coding: utf-8 -*-
"""Curator: normalizes data/curated.json (overrides + radar-derived manual entries).

Overrides are keyed by repo name (org-agnostic). This script resolves each to a
real full_name (topic snapshot -> radar catalog), merges radar-only plugins with
compat status 兼容/关注 into the manual list, and writes the final curated.json
that sync_plugins.py consumes. Human curation lives in the `overrides` dict below.
"""
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
snapshot = json.load(open(os.path.join(os.environ["TEMP"], "plugins_clean.json"), encoding="utf-8"))
radar_rows = json.load(open(os.path.join(os.environ["TEMP"], "radar_rows.json"), encoding="utf-8"))
snap_by_name = {}
for _i in snapshot:
    _n = _i["full_name"].split("/")[1].lower()
    if _n not in snap_by_name or _i["stars"] > snap_by_name[_n]["stars"]:
        snap_by_name[_n] = _i
radar_by_name = {r["name"].lower(): r["repo"] for r in radar_rows}

cur = json.loads((ROOT / "data" / "curated.json").read_text(encoding="utf-8"))
raw_overrides = cur.get("overrides", {})

NOISE = {"issues","group-chat-diary","hub","marisa","zephyr","onboarding",
    "dsh-hub-private-archive","dsh-public-repo-monitor","dsh-plugin-radar",
    "repo-visibility-guard","__perm_probe__","dsh-STAGE","dsh-STAR",
    "deepseek-harness-distro","oh-my-dsh-distribution","dsh-cordis-examples",
    "dsh-cordis-rocks","savemoneybenchmark","tonghuashun-harness","dsh-edu",
    "dsh-dzcf","dsh-d399","dsh-hmz","dsh-fkin-vibe","dsh-lazyfish",
    "dsh-serenity-plugin","dsh-sfw","dsh-spur","dsh-sonar","dsh-deeptag",
    "dsh-meme","dsh-travel-plugin","dsh-plus","dsh-remote","dsh-save-intp",
    "dsh-web","dsh-chat","dsh_ide","dsh-build","dsh-spec-kit","dsh-tui",
    "dsh-ui-webview","dsh-coding-receipt","dsh-mobileweb-adapter",
    "dsh-android","dsh-ohos-patch","dsh-win-port","dsh-acp",
    "dsh-context7","dsh-desktop-mac","dsh-desktop-tools","dsh-pet-rs",
    "deepseek-harness-desktop","dsh-opencode-server","dsh-web-terminal",
    "dsh-web-ui-approval-notify","dshx-update-check","dsh-security",
    "oh-my-deepseek","oh-dsh-desktop","review-panel","dsh-profile-bundle-example",
    "my-plugin","dsh-plugin","dsh-skeleton","dsh-example","dsh-boilerplate","dsh-template"}

def resolve(key):
    name = key.split("/")[-1].lower()
    if name in snap_by_name:
        return snap_by_name[name]["full_name"]
    if name in radar_by_name:
        return radar_by_name[name]
    return None

normalized, unresolved = {}, []
for key, val in raw_overrides.items():
    real = resolve(key)
    name = key.split("/")[-1].lower()
    if name in normalized:
        continue
    if real is None:
        unresolved.append(key)
        continue
    normalized[name] = {**val, "repo": real}
    if real.split("/")[0].lower() not in ("deepseek-ai",) and name not in snap_by_name:
        unresolved.append(real)

manual, used = [], set()
for row in radar_rows:
    name, repo = row["name"].lower(), row["repo"]
    if row["compat"] not in ("兼容", "关注") or name in NOISE or repo in used:
        continue
    if name in snap_by_name or name in normalized:
        continue
    used.add(repo)
    manual.append({"repo": repo, "category": None, "note": row["desc"]})

print("normalized overrides:", len(normalized), "| manual radar entries:", len(manual))
print("unresolved (dropped):", unresolved if unresolved else "none")
out = {"min_stars": cur.get("min_stars", 3), "overrides": normalized, "manual": manual}
(ROOT / "data" / "curated.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("written data/curated.json")
