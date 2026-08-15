[简体中文](README.md) · [**English**](README.en.md)

# Oh-My-DSH

> Aggregating the DeepSeek Harness plugin ecosystem into an authoritative, comprehensive and continuously updated directory, guided by the official philosophy "Everything is a Plugin."

[![Awesome](https://awesome.re/badge.svg)](https://github.com/like-study1/Oh-My-DSH)
![plugins](https://img.shields.io/badge/plugins-auto--synced-blue)
![sync](https://img.shields.io/badge/auto--maintained-every%204%20hours-green)
![license](https://img.shields.io/badge/license-MIT-blue)
![pages](https://img.shields.io/badge/community%20site-GitHub%20Pages-4d6bfe)

## 1. Project Overview

DeepSeek Harness (DSH) is an open-source AI agent framework developed by DeepSeek AI, whose core architectural philosophy is "Everything is a Plugin." As the ecosystem expands rapidly and the number of community plugins continues to grow, the cost of discovering, evaluating and selecting plugins has increased accordingly.

This repository sources data from the GitHub `dsh-plugin` topic, performs periodic automated monitoring of the full ecosystem, and applies human curation, classification and verification on top of the raw data, resulting in a plugin aggregation directory that is comprehensive, up-to-date and practical. The results are published simultaneously in three forms: a categorized catalog, machine-readable data files, and a searchable web directory.

## 2. Ecosystem Statistics

<!-- OMD:stats:START -->
As of 2026-08-15 10:07 (Beijing Time, UTC+8), this directory curates **917** plugins across **1000** ecosystem repositories, with **268,795** cumulative stars.

### Top 10 Curated Plugins

| # | Plugin | Stars | Type | Description |
|---|---|---|---|---|
| 1 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 97128 | Project | DeepSeek Harness 官方仓库：Everything is a Plugin. |
| 2 | [nexu-io/open-design](https://github.com/nexu-io/open-design) | 86365 | Channel | 🎨 The open-source Claude Design alternative. 🖥️ Local-first desktop… |
| 3 | [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill) | 22067 | Project | 「同事」Skill：将离别化为温暖的数字生命 1.0 |
| 4 | [tt-a1i/archify](https://github.com/tt-a1i/archify) | 12579 | Plugin | Agent skill for beautiful, verifiable architecture, workflow, seque… |
| 5 | [Devin-AXIS/iPolloWork](https://github.com/Devin-AXIS/iPolloWork) | 4018 | Project | 下一代开源 AI 工作台：自进化 Agent 运行时，集成 DSH 子代理 |
| 6 | [crafter-station/petdex](https://github.com/crafter-station/petdex) | 3793 | Plugin | A public gallery of animated pets for Codex, Claude Code, DeepSeek … |
| 7 | [strukto-ai/mirage](https://github.com/strukto-ai/mirage) | 3414 | Plugin | The World's First Unified Virtual Filesystem For AI Agents |
| 8 | [imsai-sh/zhuzhiliao](https://github.com/imsai-sh/zhuzhiliao) | 2776 | Plugin | 竹知了 —— 一转就哇哇叫的传统玩具，Web 模拟版。零依赖单文件，真实录音采样，移动端优先。 |
| 9 | [foryourhealth111-pixel/Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) | 2765 | Skill | VibeSkills is a general-purpose Skill that automatically routes loc… |
| 10 | [whiteguo233/OpenBiliClaw](https://github.com/whiteguo233/OpenBiliClaw) | 2376 | Project | 本地优先的跨平台 AI 内容发现 Agent：B站、小红书、抖音、YouTube、X、知乎、Reddit |

### Category Breakdown

`Messaging 109` · `Vision & Multimodal 53` · `Browser & Web 54` · `Web UI Enhancement 216` · `Themes & Fun 74` · `Agent Capabilities 236` · `Coding & Development 71` · `Files & Data 32` · `Dev Tools & Tutorials 28` · `Collections & Distros 25` · `Ecosystem Projects 19`

<!-- OMD:stats:END -->

## 3. Capabilities

**01 Full-Scale Monitoring** — Automated snapshots of the entire GitHub `dsh-plugin` topic are taken every 4 hours, tracking the addition, renaming and archiving of ecosystem repositories in real time, covering the full set of topic repositories.

**02 Human Curation** — On top of automated collection, candidate plugins are individually reviewed, assigned to precise categories and described in concise entries, ensuring the directory is accurate and well organized.

**03 Categorized Catalog** — Entries are organized into eleven functional categories, covering Web UI enhancement, agent capabilities, coding & development, messaging, vision & multimodality, themes & fun, collections & distros, among others, with bilingual descriptions where applicable.

**04 Activity Signals** — Each entry carries an activity signal — active, watch, slow, stale — derived from the repository's latest commit, helping users assess maintenance status and update cadence.

**05 Community Web Directory** — A GitHub Pages–based web directory supports keyword search and category filtering for rapid discovery.

**06 Automated Maintenance** — Sync scripts and continuous integration run in concert; the catalog, data files, web directory and changelog are updated together without manual intervention.

## 4. Navigation

| Category | Entry | Description |
|---|---|---|
| Catalog | [PLUGINS.md](PLUGINS.md) | Categorized listing of curated entries |
| Plugin Community | [Oh-My-DSH Plugin Community](https://like-study1.github.io/Oh-My-DSH/) | Searchable and filterable web directory |

## 5. Quick Start

```bash
# Launch the DeepSeek Harness Web UI (official developer preview)
npx @deepseek-ai/dsh web    # default: http://127.0.0.1:3080

# Plugin installation: follow each plugin's README or the official plugin marketplace
```

## 6. Contributing

Plugin authors may apply for inclusion in either of the following ways:

1. **Topic Registration** — Add the `dsh-plugin` topic to the plugin repository; automated sync completes pre-screening within 4 hours, and entries are admitted after human curation review.
2. **Direct Submission** — Register via [Issue](https://github.com/like-study1/Oh-My-DSH/issues), or modify [`data/curated.json`](data/curated.json) and submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 7. Disclaimer

This directory is built voluntarily by the community. Inclusion does not constitute endorsement by DSH. Listing status reflects public data only and does not imply compatibility; activity signals do not imply security. Before installing third-party plugins, users should verify the plugin's source code, permission scope, dependencies, license and recent update history.

## 8. Acknowledgments

The development of this repository has benefited from the following projects and organizations: deepseek-ai/deepseek-harness (the DSH core), AdamPlatin123/awesome-dsh-plugins (ecosystem radar and cross-reference source), 0xsline/awesome-deepseek-harness and awesome-dsh-plugin/awesome-dsh-plugin (ecosystem lists), can1357/oh-my-pi (layout reference), and NoWint/Oh-My-DSH (a sibling project with the same name, maintaining an hourly multi-source DSH ecosystem directory; cross-linked). Sincere thanks are extended to all.

## License

[MIT](LICENSE) © Oh-My-DSH contributors