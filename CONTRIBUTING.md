# 🤝 贡献指南 · CONTRIBUTING

感谢你愿意让 Oh-My-DSH 变得更好！这里有两种贡献方式：

## 1. 登记你的插件（推荐）

给插件仓库添加 `dsh-plugin` topic，自动同步会在 **8 小时内**完成收录：

- Star ≥ 3：自动进入分类目录（`PLUGINS.md`）
- Star < 3：通过下方 PR 方式人工收录

## 2. 通过 Issue / PR 登记

在 [Issues](https://github.com/like-study1/Oh-My-DSH/issues/new) 提交，或直接修改 `data/curated.json` 提交 PR：

```jsonc
{
  "overrides": {
    "your-plugin-name": {
      "repo": "your-name/your-plugin",
      "category": "webui",   // 可选：channel / vision / browser / webui / skin / agent / code / data / devtools / collection / eco
      "note": "一句话中文简介",
      "keep": true             // 可选：强制收录（低 Star 也保留）
    }
  }
}
```

> 注意：仓库必须是 **public** 且未被归档，否则同步脚本会跳过。

## 目录结构

```text
README.md                 # 首页 + 自动统计
PLUGINS.md                # 分类目录（自动生成）
CHANGELOG.md              # 变更记录（自动生成）
data/curated.json         # 人工策展配置（唯一需要手改的文件）
data/plugins.json         # 机器可读精选索引（自动生成）
data/snapshot.json        # 生态全量快照（自动生成）
docs/index.html           # 社区站点（自动生成）
scripts/sync_plugins.py   # 同步脚本
scripts/generate_curated.py  # 策展数据生成脚本
```

## 本地运行同步

```bash
export GH_TOKEN=ghp_xxx   # 或登录 gh CLI
python scripts/sync_plugins.py
```

## 审核标准

- 插件仓库公开、未归档、有真实可用的代码
- 描述清晰，能一句话说明解决什么问题
- 涉及权限、网络、系统级操作的插件会标注提醒