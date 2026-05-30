# 探索倡议托管的目标绑定变更 artifact

## 状态

尚未开始。已添加为未来的探索性工作项。框架已从通用的"可配置变更家园"更新为更精确的问题：共享的倡议 artifact 何时可以成为可执行的、目标绑定的 OpenSpec 变更。

## 事实源

从 `../../direction.md` 出发，特别是当前的边界：

```text
上下文存储同步事实。
集合塑造事实。
倡议协调工作。
Workspace 打开本地视图。
变更实现 repository 拥有的切片。
```

## 为什么存在

当前倡议方向假设 OpenSpec 变更通常存在于拥有实现的本地 repository 中。这使验证、archive 和 spec 同步保持在将要更改的代码附近。

某些协调工作可能需要在拥有 repository 明确之前有一个共享家园。团队可能想要倡议托管的 planning artifact，以后可能希望其中一些 artifact 成为特定 repository 或 spec 根目录的实现就绪计划。

这不仅仅是一个存储偏好。共享 artifact 在具有显式可移植目标绑定以及验证、应用、archive、spec 同步和冲突处理的生命周期规则之前，仅用于 planning。

## 目标

决定 OpenSpec 是否应支持倡议托管的 artifact，这些 artifact 只有在绑定到实现目标后才能升级为可执行变更。

repository 本地变更仍然是默认的可执行实现 artifact。第 18 项应决定上下文存储托管的 artifact 是否、何时以及如何安全地被视为变更。

答案应保留三个边界：

- 倡议协调共享上下文。
- 变更描述可执行的实现计划。
- Workspace 打开本地视图且不得暗示编辑权限。

## 要探索的模型

```text
倡议 artifact
 -> 默认仅用于 planning
 -> 以后可能成为目标绑定

repository 本地变更
 -> 家园：repo/openspec/changes/<id>/
 -> 目标：隐式的当前 repository/spec 根目录
 -> 生命周期：validate/apply/archive/spec sync 为 repository 本地

倡议托管的目标绑定变更
 -> 家园：context-store/initiatives/<initiative>/changes/<id>/
 -> 目标：显式的 repository/spec 根目录身份
 -> 生命周期：在目标解析设计之前不受支持

agent 输出
 -> 报告工作目标
 -> 报告 artifact 存放位置
 -> 报告实现目标（如果有）
 -> 报告此机器的允许编辑根目录
```

保持"变更家园"作为内部解析器语言。面向用户和面向 agent 的输出应优先使用更清晰的短语，如"计划位于 repository 本地 OpenSpec"、"计划随倡议存在"和"可编辑目标"。

## 核心不变性

- 存储位置不暗示所有权、编辑权限或生命周期。
- 工作身份、artifact 家园、执行目标和允许的编辑根目录是分离的决策。
- 共享的上下文存储文件不得存储机器本地的检出路径。
- 无目标的倡议 artifact 是简报、工作项或 proposal，而不是实现就绪的 OpenSpec 变更。
- 上下文存储托管的 artifact 只有在具有显式目标元数据和生命周期命令支持后才能被视为可执行。
- 第 8 项保持 repository 本地：`new change <id> --initiative ...` 仅创建或链接一个 repository 本地变更。

## 要回答的问题

- 倡议下存在哪些确切的 artifact 类型：工作项、简报、目标绑定变更或其他？
- 在倡议托管 artifact 可执行之前，需要哪些可移植目标元数据？
- 本地解析如何将目标 repository 身份映射到检出路径、OpenSpec 根目录、分支和允许的编辑根目录？
- 中央目标绑定变更是否需要显式的选择加入，如 `--home initiative`，还是倡议/存储策略可以选择此行为？
- 如果存在配置，显式 CLI 标志、repository 配置、倡议偏好、上下文存储默认、用户默认和内置 repository 本地行为之间的确定性优先级是什么？
- `openspec new change` 如何在 JSON 中报告工作目标、artifact 家园、实现目标、倡议链接、操作上下文和后续命令？
- 当 artifact 位于上下文存储中但目标 spec 位于 repository 中时，validate、apply、archive 和 spec sync 如何表现？
- 倡议托管的目标绑定变更的 archive 是集中 archive、实现 repository 本地的交接变更，还是拒绝直到 repository 本地变更存在？
- 哪些命令和 skill 界面仍然硬编码 `openspec/changes/`、当前工作目录或 repository 本地编辑假设？
- 什么兼容性行为保留现有的 repository 本地和 workspace 本地变更？

## agent 优先输出契约

任何创建、读取或解析此工作的未来命令都应使 agent 的下一步操作显式：

```json
{
 "workTarget": {
 "kind": "repo-change | initiative-work-item | initiative-hosted-change",
 "id": "add-billing-api",
 "root": "/absolute/path/reported/by/cli"
 },
 "initiativeLink": {
 "store": "platform",
 "id": "billing-launch"
 },
 "implementationTarget": {
 "kind": "repo",
 "id": "billing-api",
 "specRoot": "openspec"
 },
 "actionContext": {
 "mode": "implementation-ready | planning-only | target-selection-required | unsupported",
 "sourceOfTruth": "repo | context-store | workspace-local",
 "allowedEditRoots": [],
 "constraints": [
 "Use CLI-reported paths.",
 "Do not infer editable repos from the current working directory."
 ]
 },
 "nextCommands": {}
}
```

如果 `allowedEditRoots` 为空，agent 不应编辑实现文件。如果需要目标选择，命令应返回选项或后续命令，而不是创建模糊的实现计划。

## 明确排除在范围之外

- 在模型决定之前实现上下文存储托管可执行变更。
- 自动将现有 repository 本地变更移入上下文存储。
- 使倡议默认拥有实现 artifact。
- 使 workspace 级别的变更成为新的共享 planning 模型。
- 跨 repository 的 apply、archive 或 validation 编排。
- 在共享的上下文存储文件中存储机器本地检出路径。
- 添加可能使普通 repository 本地命令意外写入共享 artifact 的全局默认值。

## 通过/不通过标准

在 OpenSpec 拥有一个覆盖以下内容的目标解析模型之前，不要实现倡议托管可执行变更：

- create 和 link 输出
- status、show、list 和 instructions 输出
- validate、apply、archive 和 spec sync 行为
- workspace 注册表和本地 repository 映射行为
- 生成的 skill 指导和命令示例
- 工作目标、artifact 家园、实现目标、编辑根目录、不支持的声明周期命令和后续命令的 JSON 输出
