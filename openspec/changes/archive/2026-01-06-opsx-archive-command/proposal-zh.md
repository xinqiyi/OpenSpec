## 为什么

实验性 workflow（OPSX）提供了一种基于 schema、逐构件的方式，通过 `/opsx:new`、`/opsx:continue`、`/opsx:ff`、`/opsx:apply` 和 `/opsx:sync` 来创建变更。然而，缺少相应的 archive 命令来完成并 archive 已完成的变更。用户当前必须回退到常规的 `openspec archive` 命令，但这与 OPSX 的 agent 人驱动 spec 同步和 schema 感知构件追踪理念不一致。

## 变更内容

- 添加 `/opsx:archive` 斜杠命令，用于在实验性 workflow 中 archive 变更
- 使用构件图检查完成状态（schema 感知），而不仅仅是验证 proposal 和 spec
- 在 archive 前提示运行 `/opsx:sync`，而不是以编程方式应用 spec
- 在移动到 archive 时保留 `.openspec.yaml` schema 元数据
- 与现有 OPSX 命令集成，形成连贯的 workflow

## 能力

### 新能力

- `opsx-archive-skill`：用于在实验性 workflow 中 archive 已完成变更的斜杠命令和 skill。通过构件图检查构件完成情况，验证任务完成情况，可选地通过 `/opsx:sync` 同步 spec，并将变更移动到 `archive/YYYY-MM-DD-<name>/`。

### 修改的能力

（无——这是一个新 skill，不修改现有 spec）

## 影响范围

- 新文件：`.claude/commands/opsx/archive.md`
- 新的 skill 定义（通过 `openspec artifact-experimental-setup` 生成）
- 不更改现有 archive 命令或其他 OPSX 命令
- 完善了 OPSX 命令套件，实现完整的生命周期管理
