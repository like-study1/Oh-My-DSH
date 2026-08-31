[**简体中文**](README.md) · [English](README.en.md)

# Oh-My-DSH

> 汇聚 DeepSeek Harness 生态插件，构建权威、完整、可持续更新的聚合目录。以官方理念“万物皆可插件”（Everything is a Plugin）为指引，服务全球开发者。

[![Awesome](https://awesome.re/badge.svg)](https://github.com/like-study1/Oh-My-DSH)
![plugins](https://img.shields.io/badge/插件-自动同步-blue)
![sync](https://img.shields.io/badge/自动维护-每4小时-green)
![license](https://img.shields.io/badge/license-MIT-blue)
![pages](https://img.shields.io/badge/社区站点-GitHub%20Pages-4d6bfe)

## 一、项目定位

DeepSeek Harness（以下简称 DSH）是由深度求索（DeepSeek AI）开源的人工智能 Agent 框架，其核心架构理念为“万物皆可插件”。随着生态体系快速扩展，社区插件数量持续增长，开发者在检索、甄别与选用插件方面的成本随之上升。

本仓库以 GitHub `dsh-plugin` 主题为数据源，对生态全量插件实施周期性自动监测，并在此基础上开展人工遴选、分类编目与信息核验，形成集完整性、时效性与可用性于一体的插件聚合目录。收录结果以分类目录、数据文件与检索站点三种形态同步发布。

## 二、内容导航

| 类别 | 入口 | 说明 |
|---|---|---|
| 分类目录 | [PLUGINS.md](PLUGINS.md) | 精选条目的分类明细 |
| 插件聚合社区 | [Oh-My-DSH 插件聚合社区](https://like-study1.github.io/Oh-My-DSH/) | 支持检索与筛选的网页目录 |

## 三、生态统计

<!-- OMD:stats:START -->
截至 2026-09-01 05:28（北京时间），本目录收录精选插件 **2100** 个，监测生态仓库 **1989** 个，累计获得 Star **936453**。

### 精选插件十强

| 序号 | 插件 | Star | 类型 | 说明 |
|---|---|---|---|---|
| 1 | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 206375 | 项目 | DeepSeek Harness 官方仓库：Everything is a Plugin. |
| 2 | [nexu-io/open-design](https://github.com/nexu-io/open-design) | 93054 | 渠道 | 🎨 Best DeepSeek Harness Design Plugin. The open-source Claude Desig… |
| 3 | [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 69997 | 插件 | 🌊 The original agent meta-harness. Deploy intelligent multi-player … |
| 4 | [amruthpillai/reactive-resume](https://github.com/amruthpillai/reactive-resume) | 42011 | 插件 | A one-of-a-kind resume builder that keeps your privacy in mind. Com… |
| 5 | [tt-a1i/archify](https://github.com/tt-a1i/archify) | 38382 | 插件 | Agent skill for beautiful, verifiable architecture, workflow, seque… |
| 6 | [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | 35296 | 插件 | DeepSeek-native AI coding agent for your terminal. Engineered aroun… |
| 7 | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | 34684 | 插件 | Self-evolving Context Database for AI Agents. Unify Agent Memory, K… |
| 8 | [Molunerfinn/PicGo](https://github.com/Molunerfinn/PicGo) | 27104 | 插件 | :rocket: The Ultimate Image Uploader for Efficient Creators. Suppor… |
| 9 | [freestylefly/awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) | 26327 | 插件 | Prompt as Code \| GPT-Image2 工业级提示词引擎与模板库，530+ 个案例逆向工程，20+ 套工业级模板，并… |
| 10 | [titanwings/distilly](https://github.com/titanwings/distilly) | 24207 | 项目 | 「同事」Skill：将离别化为温暖的数字生命 1.0 |

### 分类构成

`消息通讯 242` · `视觉与多模态 122` · `浏览器与网络 134` · `Web UI 增强 503` · `皮肤与娱乐 167` · `Agent 能力 578` · `编码开发 154` · `文件与数据 59` · `开发工具与教程 81` · `精选合集与发行版 32` · `生态项目 28`

<!-- OMD:stats:END -->

## 四、功能体系

**01 全量监测** — 每 4 小时自动抓取 GitHub `dsh-plugin` 主题全量快照，实时跟踪生态内仓库的新增、更名与归档状态，监测范围覆盖全部主题仓库。

**02 人工策展** — 在自动采集的基础上，对候选插件逐项核验，明确类型归属，撰写条目简介，确保目录信息准确、层次分明。

**03 分类编目** — 按功能领域划分十一大类，涵盖 Web UI 增强、Agent 能力、编码开发、消息通讯、视觉与多模态、皮肤与娱乐、合集与发行版等，条目兼容中英双语说明。

**04 活跃度信号** — 依据仓库最近提交时间，标注“活跃、关注、放缓、停更”四级信号，辅助研判插件维护状态与更新节奏。

**05 社区站点** — 依托 GitHub Pages 部署检索站点，支持关键词检索与分类筛选，便于快速定位目标插件。

**06 自动维护** — 同步脚本与持续集成流程协同运行，目录、数据、站点及变更记录同步更新，全过程无需人工干预。

## 五、快速使用

```bash
# 启动 DeepSeek Harness Web UI（官方开发者预览版）
npx @deepseek-ai/dsh web    # 默认地址 http://127.0.0.1:3080

# 插件安装：通过官方插件市场或各插件仓库说明执行
```

## 六、参与贡献

插件作者可通过以下任一方式申请收录：

1. **主题登记** — 为插件仓库添加 `dsh-plugin` 主题标签，自动同步将在 4 小时内完成初筛，经人工策展核验后择优收录。
2. **提交申请** — 通过 [Issue](https://github.com/like-study1/Oh-My-DSH/issues) 登记，或修改 [`data/curated.json`](data/curated.json) 后提交 Pull Request，具体流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 七、责任声明

本目录系社区自发建设，收录行为不代表 DSH 官方背书。收录状态仅反映公开数据，不构成兼容性承诺；活跃度信号不等同于安全性结论。使用者安装第三方插件前，应自行核验插件源码、权限范围、依赖关系、开源许可及最近更新时间。

## 八、致谢

本仓库的建设得到以下项目与组织的支持：deepseek-ai/deepseek-harness（DSH 本体）、AdamPlatin123/awesome-dsh-plugins（生态雷达，交叉参考来源）、0xsline/awesome-deepseek-harness 与 awesome-dsh-plugin/awesome-dsh-plugin（生态清单）、can1357/oh-my-pi（版式参考）、NoWint/Oh-My-DSH（同名兄弟项目，每小时多源扫描的 DSH 生态目录，已交叉链接）。谨致谢忱。

## 开源许可

[MIT](LICENSE) © Oh-My-DSH contributors