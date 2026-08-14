# -*- coding: utf-8 -*-
"""Oh-My-DSH plugin index sync script.

Fetches the `dsh-plugin` topic from GitHub, applies the human curation in
data/curated.json, and regenerates:
  - data/snapshot.json      full ecosystem snapshot (all topic repos)
  - data/plugins.json       curated plugin index (machine readable)
  - PLUGINS.md              categorized catalog (bilingual)
  - docs/index.html         community landing site (GitHub Pages)
  - README.md               stats + top-N block (between OMD markers)
  - CHANGELOG.md            one entry per meaningful change

Run locally:  python scripts/sync_plugins.py
Requires GH_TOKEN (or `gh auth token`) for API access.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
UA = "oh-my-dsh-sync"

CATEGORIES = [
    ("channel",   "??", "????",       "Telegram / ?? / QQ / ?????????????"),
    ("vision",    "???", "??????",   "???VLM?OCR?????? UI ??"),
    ("browser",   "??", "??????",   "????????????????"),
    ("webui",     "??", "Web UI ??",    "???????????????? Web ????"),
    ("skin",      "??", "?????",     "??????????????????"),
    ("agent",     "??", "Agent ??",     "???????????????????????"),
    ("code",      "??", "????",       "???Git??? / TUI???????"),
    ("data",      "???", "?????",     "??????????????????"),
    ("devtools",  "???", "???????", "?????????????????"),
    ("collection","??", "????????", "?????????????"),
    ("eco",       "??", "????",       "?? / ?? DSH ??????????"),
]
CAT_EMOJI = {c: e for c, e, _, _ in CATEGORIES}

# keyword rules: (category, [patterns]) — first match wins
RULES = [
    ("channel", ["telegram", "wechat", "weixin", "wecom", "feishu", "qqbot", "qq2006",
                 "notify", "notification", "relay", "share", "webbridge", "channel",
                 "interconnect", "webhook", "lan", "语音", "聊天"]),
    ("vision", ["vision", "vlm", "visual", "ocr", "image", "看图", "视觉", "多模态",
                "modlens", "her-eyes", "multimodal", "ui4a"]),
    ("browser", ["browser", "websearch", "web-search", "search", "crawl", "crawler",
                 "browser-bridge", "modsearch", "argo", "webcraw", "scrape"]),
    ("skin", ["skin", "theme", "pet", "whale", "game", "minigame", "ads", "emoji",
              "sticker", "gomoku", "tavern", "xiaohei", "deep-whale", "wallpaper",
              "壁纸", "皮肤", "宠物", "贴纸", "小游戏"]),
    ("webui", ["webui", "web-ui", "panel", "sidebar", "composer", "status-label",
               "progress", "focus-chat", "annotation", "width", "drag", "paste",
               "input-history", "navbar", "milestone", "diff-viewer", "genui",
               "visualize", "at-file", "recall", "message-edit", "turn-navigator",
               "split-panes", "question-collapse", "live-stats", "tps",
               "task-status", "web-review", "selection", "custom-css", "deepcel",
               "island", "side-panel", "workflow-visualizer", "fabric", "ramify"]),
    ("agent", ["memory", "context", "session", "agent", "subagent", "workflow",
               "skill", "plan", "budget", "checkpoint", "rewind", "evolve", "sleep",
               "prompt", "loop", "automation", "fallback", "orchestr", "distill",
               "track", "sentinel", "companion", "turbo", "cost-tracker", "work",
               "recall", "mnemon", "engram", "a2a", "alphasolve", "scout", "explain",
               "inspect", "inject", "superpowers", "session-hub", "teleport",
               "falsify", "deep-research", "billion-context", "agent-teams",
               "mstar", "teamwork", "context-doctor", "llm", "fallback", "rp",
               "wake", "guard", "activity", "mega"]),
    ("code", ["git", "tui", "terminal", "vscode", "ide", "diff", "build", "latex",
              "office", "debug", "trace", "blame", "commit", "interpreter",
              "tianshu", "grok-tui", "cc-connect", "pty", "shell", "gh-bridge",
              "code-map", "leantoken", "grok", "codex-bridge", "open-in-vscode",
              "cc-tui", "tui-front", "claude-move", "dsh-code", "interpreters",
              "test-runner", "billion"]),
    ("data", ["file", "json", "database", "sql", "persistence", "chatlog",
              "artifact", "encoding", "hash", "doc", "pdf", "kb", "rag", "zotero",
              "mineru", "notebook", "import", "export", "craw", "data-agent",
              "tool-json", "tool-encoding", "tool-search", "tool-stat",
              "tool-calculator", "tool-time", "session-health", "recording",
              "multimedia", "wave", "openpencil", "custom-tool"]),
    ("devtools", ["plugin-dev", "installer", "launcher", "desktop", "tutorial",
                  "handbook", "教程", "开发", "make-dsh", "registry", "security",
                  "hello-dsh", "find-plugins", "profile-bundle", "docker",
                  "distro", "plugin-registry", "plugin-installer", "sdk",
                  "spec-kit", "radar", "suit"]),
    ("collection", ["awesome", "collection", "合集", "发行版", "distribution",
                    "suite", "pluGins导航", "目录", "nagivation", "directory",
                    "web-ui", "oh-my-dsh", "oh-dsh"]),
]
ECO_NAMES = {"colleague-skill", "ipollowork", "openbiliclaw", "deeptide", "mobius",
             "axern", "open-managed-agents", "rea", "abucowork", "claude-paper",
             "harmony-next.skills", "phi", "openguardrails", "open-record-replay",
             "jacobian", "flameox", "internalcot", "mcp-for-stata", "agent-vision-toolkit",
             "leantoken", "allinluna", "illusion-agent", "mobius", "fabric"}

def log(msg):
    print(msg, flush=True)

def api_get(url, token, retries=3):
    for i in range(retries):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}", "User-Agent": UA,
            "Accept": "application/vnd.github+json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                time.sleep(5 * (i + 1)); continue
            if e.code == 404:
                return None
            raise
        except Exception:
            time.sleep(3 * (i + 1))
    return None

def fetch_snapshot(token):
    items, seen = [], set()
    for page in range(1, 11):
        url = (f"{API}/search/repositories?q=topic:dsh-plugin&sort=stars"
               f"&order=desc&per_page=100&page={page}")
        data = api_get(url, token)
        if not data or not data.get("items"):
            break
        for it in data["items"]:
            if it["full_name"] in seen:
                continue
            seen.add(it["full_name"])
            items.append({
                "full_name": it["full_name"], "url": it["html_url"],
                "description": (it.get("description") or "").strip(),
                "stars": it.get("stargazers_count", 0), "forks": it.get("forks_count", 0),
                "language": it.get("language"), "topics": it.get("topics", []),
                "archived": it.get("archived", False), "fork": it.get("fork", False),
                "pushed_at": it.get("pushed_at", ""), "created_at": it.get("created_at", ""),
                "license": (it.get("license") or {}).get("spdx_id"),
                "owner": it["owner"]["login"], "homepage": it.get("homepage") or "",
            })
        log(f"  page {page}: cumulative {len(items)}")
        if len(items) >= data.get("total_count", 0):
            break
    return items

def repo_entry(data):
    return {
        "full_name": data["full_name"], "url": data["html_url"],
        "description": (data.get("description") or "").strip(),
        "stars": data.get("stargazers_count", 0), "forks": data.get("forks_count", 0),
        "language": data.get("language"), "topics": data.get("topics", []),
        "archived": data.get("archived", False), "fork": data.get("fork", False),
        "pushed_at": data.get("pushed_at", ""), "created_at": data.get("created_at", ""),
        "license": (data.get("license") or {}).get("spdx_id"),
        "owner": data["owner"]["login"], "homepage": data.get("homepage") or "",
    }

def classify(name, desc):
    hay = f"{name} {desc}".lower()
    for cat, pats in RULES:
        if any(p in hay for p in pats):
            return cat
    nm = name.lower()
    for eco in ECO_NAMES:
        if eco in nm:
            return "eco"
    return "webui"

def activity(pushed_at, now):
    try:
        days = (now - datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))).days
    except Exception:
        return "—"
    if days <= 14: return "🟢 活跃"
    if days <= 60: return "🟡 关注"
    if days <= 180: return "🟠 放缓"
    return "⚫ 停更"

def typify(entry):
    name = entry["full_name"].lower()
    cat = entry["category"]
    if cat == "channel": return "渠道"
    if cat == "collection": return "合集"
    if cat == "eco": return "项目"
    if "skill" in name: return "技能"
    if cat == "devtools":
        if any(k in name for k in ("desktop", "launcher", "installer", "docker", "registry")):
            return "工具"
        if any(k in entry["description"].lower() for k in ("教程", "手册", "tutorial", "handbook", "从零开始")):
            return "教程"
    return "插件"

def load_curated():
    return json.loads((ROOT / "data" / "curated.json").read_text(encoding="utf-8"))

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        import subprocess
        token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    if not token:
        sys.exit("GH_TOKEN required")
    now = datetime.now(timezone.utc)
    curated_cfg = load_curated()
    min_stars = curated_cfg.get("min_stars", 3)
    overrides = curated_cfg.get("overrides", {})
    manual = curated_cfg.get("manual", [])

    log("== fetching topic snapshot ==")
    snapshot = fetch_snapshot(token)
    log(f"snapshot: {len(snapshot)} repos")
    snap_by_name = {}
    for _i in snapshot:
        _n = _i["full_name"].split("/")[1].lower()
        if _n not in snap_by_name or _i["stars"] > snap_by_name[_n]["stars"]:
            snap_by_name[_n] = _i
    snap_by_full = {i["full_name"].lower(): i for i in snapshot}
    (ROOT / "data" / "snapshot.json").write_text(json.dumps(
        {"fetched_at": now.isoformat(), "total": len(snapshot), "items": snapshot},
        ensure_ascii=False, indent=1), encoding="utf-8")

    log("== resolving curated entries ==")
    entries = {}
    dropped = []
    # 1) overrides that live in the snapshot
    for name, ov in overrides.items():
        ent = snap_by_full.get(ov.get("repo", "").lower()) or snap_by_name.get(name.lower())
        if ent:
            entries[ent["full_name"]] = {**ent, "category": ov.get("category"), "note": ov.get("note") or "", "source": "topic"}
    # 2) overrides / manual entries outside the snapshot -> repo API
    for name, ov in overrides.items():
        if snap_by_full.get(ov.get("repo", "").lower()) or name.lower() in snap_by_name:
            continue
        data = api_get(f"{API}/repos/{ov['repo']}", token)
        if not data or data.get("archived"):
            dropped.append(ov["repo"]); continue
        ent = repo_entry(data)
        entries[ent["full_name"]] = {**ent, "category": ov.get("category"), "note": ov.get("note") or "", "source": "curated"}
        log(f"  + {ent['full_name']} ({ent['stars']}★)")
    for m in manual:
        data = api_get(f"{API}/repos/{m['repo']}", token)
        if not data or data.get("archived"):
            dropped.append(m["repo"]); continue
        ent = repo_entry(data)
        entries[ent["full_name"]] = {**ent, "category": m.get("category"), "note": m.get("note") or "", "source": "curated"}
        log(f"  + {ent['full_name']} ({ent['stars']}★)")
    # 3) remaining snapshot repos above the star bar (auto-catalog)
    for ent in snapshot:
        if ent["full_name"] in entries or ent["archived"] or ent["fork"]:
            continue
        if ent["stars"] >= min_stars and ent["full_name"] != "deepseek-ai/deepseek-harness":
            entries[ent["full_name"]] = {**ent, "category": None, "note": "", "source": "auto"}
    # official core always in 生态项目
    core = snap_by_name.get("deepseek-harness")
    if core:
        entries[core["full_name"]] = {**core, "category": "eco", "note": "DeepSeek Harness 官方仓库：Everything is a Plugin.", "source": "core"}

    log(f"dropped (private/archived): {len(dropped)}")
    if dropped: log("  " + ", ".join(dropped[:20]))

    # categorize + decorate
    for ent in entries.values():
        ent["category"] = ent.get("category") or classify(ent["full_name"], ent["description"])
        ent["activity"] = activity(ent["pushed_at"], now)
        ent["type"] = typify(ent)
    curated = sorted(entries.values(), key=lambda e: (-e["stars"], e["full_name"].lower()))
    log(f"curated entries: {len(curated)} (total stars {sum(e['stars'] for e in curated)})")

    (ROOT / "data" / "plugins.json").write_text(json.dumps(
        {"generated_at": now.isoformat(), "count": len(curated), "items": curated},
        ensure_ascii=False, indent=1), encoding="utf-8")

    log("== generating PLUGINS.md ==")
    generate_plugins_md(curated, len(snapshot), now)
    log("== generating site ==")
    generate_site(curated, len(snapshot), now)
    log("== updating README stats ==")
    generate_readme_stats(curated, len(snapshot), now)
    log("== updating CHANGELOG ==")
    changed = update_changelog(curated, len(snapshot), now)

    log("done. changes: " + ("yes" if changed else "no"))

def generate_plugins_md(curated, total, now):
    lines = []
    lines.append("# 📦 Oh-My-DSH 插件目录 · PLUGINS.md")
    lines.append("")
    lines.append(f"> 由 [`scripts/sync_plugins.py`](scripts/sync_plugins.py) 自动生成 · 更新于 {now.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append(f"精选条目 **{len(curated)}** · 生态快照 **{total}** 个 `dsh-plugin` 仓库 · 总 Star **{sum(e['stars'] for e in curated)}**")
    lines.append("")
    lines.append("| 插件 | 类型 | 活跃 | 语言 | ⭐ | 说明 |")
    lines.append("|---|---|---|---|---|---|")
    for cat, emoji, short, desc in CATEGORIES:
        group = [e for e in curated if e["category"] == cat]
        if not group:
            continue
        lines.append("")
        lines.append(f"## {emoji} {desc}（{len(group)}）")
        lines.append("")
        lines.append("| 插件 | 类型 | 活跃 | 语言 | ⭐ | 说明 |")
        lines.append("|---|---|---|---|---|---|")
        for e in sorted(group, key=lambda x: (-x["stars"], x["full_name"].lower())):
            name = e["full_name"].split("/")[1]
            note = (e.get("note") or e["description"] or "—").replace("|", "\\|").strip()
            if len(note) > 100:
                note = note[:97] + "…"
            lang = e["language"] or "—"
            lines.append(f"| [{name}]({e['url']}) | {e['type']} | {e['activity']} | {lang} | {e['stars']} | {note} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> [!NOTE]")
    lines.append("> 收录不等于兼容：安装第三方插件前，请检查插件源码、权限、依赖、许可证及最近更新时间。")
    lines.append("> 本目录自动聚合 GitHub `dsh-plugin` topic 数据，不代表 DSH 官方背书。")
    lines.append("> 完整生态快照见 [`data/snapshot.json`](data/snapshot.json)，机器可读精选索引见 [`data/plugins.json`](data/plugins.json)。")
    (ROOT / "PLUGINS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def generate_readme_stats(curated, total, now):
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    top = sorted(curated, key=lambda e: -e["stars"])[:10]
    top_lines = ["| # | 插件 | ⭐ | 类型 | 说明 |", "|---|---|---|---|---|"]
    for i, e in enumerate(top, 1):
        note = (e.get("note") or e["description"] or "—").replace("|", "\\|").strip()
        if len(note) > 70:
            note = note[:67] + "…"
        top_lines.append(f"| {i} | [{e['full_name']}]({e['url']}) | {e['stars']} | {e['type']} | {note} |")
    cats = []
    for cat, emoji, short, desc in CATEGORIES:
        n = sum(1 for e in curated if e["category"] == cat)
        if n:
            cats.append(f"`{emoji} {short} {n}`")
    block = [
        "<!-- OMD:stats:START -->",
        f"**{len(curated)}** 个精选插件 · **{total}** 个生态仓库 · **{sum(e['stars'] for e in curated)}** ⭐ 总 Star · 更新于 {now.strftime('%Y-%m-%d %H:%M')} UTC",
        "",
        "### 🏆 精选 Top 10",
        "",
        *top_lines,
        "",
        "### 📊 分类分布",
        "",
        " · ".join(cats),
        "",
        "<!-- OMD:stats:END -->",
    ]
    new_block = "\n".join(block)
    if "<!-- OMD:stats:START -->" in text:
        text = re.sub(r"<!-- OMD:stats:START -->.*?<!-- OMD:stats:END -->", new_block, text, flags=re.S)
    else:
        text = text + "\n\n" + new_block
    path.write_text(text, encoding="utf-8")

def update_changelog(curated, total, now):
    path = ROOT / "CHANGELOG.md"
    names = {e["full_name"] for e in curated}
    text = path.read_text(encoding="utf-8") if path.exists() else "# 📝 CHANGELOG\n\n> 每次自动同步产生的变化记录（由 GitHub Actions 维护）\n\n"
    last = None
    for m in re.finditer(r"## (\d{4}-\d{2}-\d{2})", text):
        last = m.group(1)
    if last == now.strftime("%Y-%m-%d"):
        return False  # already logged today
    entry = [
        f"## {now.strftime('%Y-%m-%d')}",
        "",
        f"- 自动同步完成：生态快照 **{total}** 个仓库，精选 **{len(curated)}** 个插件。",
        f"- 全部精选插件总 Star：**{sum(e['stars'] for e in curated)}**。",
        "",
    ]
    text = text.rstrip() + "\n\n" + "\n".join(entry)
    path.write_text(text, encoding="utf-8")

SITE_TPL = None
def load_site_template():
    global SITE_TPL
    if SITE_TPL is None:
        SITE_TPL = (ROOT / "scripts" / "site_template.html").read_text(encoding="utf-8")
    return SITE_TPL

def act_cls(e):
    return {"??": "active", "??": "watch", "??": "slow", "?": "stale"}.get(e["activity"][:1], "none")

def generate_site(curated, total, now):
    tpl = load_site_template()
    cards = []
    for e in sorted(curated, key=lambda x: (-x["stars"], x["full_name"].lower())):
        note = (e.get("note") or e["description"] or "").replace('"', "&quot;").strip()
        lang = e["language"] or "—"
        cards.append(f"""
      <a class="card" href="{e['url']}" target="_blank" rel="noopener" data-cat="{e['category']}" data-q="{(e['full_name'] + ' ' + note).lower()}">
        <div class="card-top">
          <span class="name">{e['full_name']}</span>
          <span class="stars">★ {e['stars']}</span>
        </div>
        <div class="card-meta">
          <span class="tag tag-{e['category']}">{CAT_EMOJI.get(e['category'], '🔌')} {e['type']}</span>
          <span class="lang">{lang}</span>
          <span class="act act-{e['activity'].split(' ')[0] if e['activity'] != '—' else 'none'}" title="最近更新 {e['pushed_at'][:10]}">{e['activity']}</span>
        </div>
        <p class="desc">{note}</p>
      </a>""")
    cats_html = "\n".join(
        f'<button class="chip" data-cat="{c}" onclick="filterCat(\'{c}\')">{e} {short} {sum(1 for x in curated if x["category"] == c)}</button>'
        for c, e, short, _ in CATEGORIES if any(x["category"] == c for x in curated))
    html = (tpl
        .replace("{{OMD_CARDS}}", "\n".join(cards))
        .replace("{{OMD_CATS}}", cats_html)
        .replace("{{OMD_COUNT}}", str(len(curated)))
        .replace("{{OMD_TOTAL}}", str(total))
        .replace("{{OMD_STARS}}", str(sum(e["stars"] for e in curated)))
        .replace("{{OMD_UPDATED}}", now.strftime("%Y-%m-%d %H:%M UTC")))
    out = ROOT / "docs" / "index.html"
    out.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
