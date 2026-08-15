[简体中文](README.md) · [**English**](README.en.md)

# Oh-My-DSH

> Aggregating the DeepSeek Harness plugin ecosystem into an authoritative, comprehensive and continuously updated directory, guided by the official philosophy "Everything is a Plugin."

[![Awesome](https://awesome.re/badge.svg)](https://github.com/like-study1/Oh-My-DSH)
![plugins](https://img.shields.io/badge/plugins-auto--synced-blue)
![sync](https://img.shields.io/badge/auto--maintained-every%208%20hours-green)
![license](https://img.shields.io/badge/license-MIT-blue)
![pages](https://img.shields.io/badge/community%20site-GitHub%20Pages-4d6bfe)

## 1. Project Overview

DeepSeek Harness (DSH) is an open-source AI agent framework developed by DeepSeek AI, whose core architectural philosophy is "Everything is a Plugin." As the ecosystem expands rapidly and the number of community plugins continues to grow, the cost of discovering, evaluating and selecting plugins has increased accordingly.

This repository sources data from the GitHub `dsh-plugin` topic, performs periodic automated monitoring of the full ecosystem, and applies human curation, classification and verification on top of the raw data, resulting in a plugin aggregation directory that is comprehensive, up-to-date and practical. The results are published simultaneously in three forms: a categorized catalog, machine-readable data files, and a searchable web directory.

## 2. Ecosystem Statistics

<!-- OMD:stats:START -->
As of 2026-08-15 09:42 (Beijing Time, UTC+8), this directory curates **909** plugins across **1000** ecosystem repositories, with **267,995** cumulative stars.

### Top 10 Curated Plugins

| # | Plugin | Stars | Type | Description |
|---|---|---|---|---|

### Category Breakdown

`Messaging 106` · `Vision & Multimodal 52` · `Browser & Web 54` · `Web UI Enhancement 215` · `Themes & Fun 73` · `Agent Capabilities 236` · `Coding & Development 70` · `Files & Data 32` · `Dev Tools & Tutorials 27` · `Collections & Distros 25` · `Ecosystem Projects 19`

<!-- OMD:stats:END -->

## 3. Capabilities

**01 Full-Scale Monitoring** — Automated snapshots of the entire GitHub `dsh-plugin` topic are taken every 8 hours, tracking the addition, renaming and archiving of ecosystem repositories in real time, covering the full set of topic repositories.

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

1. **Topic Registration** — Add the `dsh-plugin` topic to the plugin repository; automated sync completes pre-screening within 8 hours, and entries are admitted after human curation review.
2. **Direct Submission** — Register via [Issue](https://github.com/like-study1/Oh-My-DSH/issues), or modify [`data/curated.json`](data/curated.json) and submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 7. Disclaimer

This directory is built voluntarily by the community. Inclusion does not constitute endorsement by DSH. Listing status reflects public data only and does not imply compatibility; activity signals do not imply security. Before installing third-party plugins, users should verify the plugin's source code, permission scope, dependencies, license and recent update history.

## 8. Acknowledgments

The development of this repository has benefited from the following projects and organizations: deepseek-ai/deepseek-harness (the DSH core), AdamPlatin123/awesome-dsh-plugins (ecosystem radar and cross-reference source), 0xsline/awesome-deepseek-harness and awesome-dsh-plugin/awesome-dsh-plugin (ecosystem lists), can1357/oh-my-pi (layout reference), and NoWint/Oh-My-DSH (a sibling project with the same name, maintaining an hourly multi-source DSH ecosystem directory; cross-linked). Sincere thanks are extended to all.

## License

[MIT](LICENSE) © Oh-My-DSH contributors