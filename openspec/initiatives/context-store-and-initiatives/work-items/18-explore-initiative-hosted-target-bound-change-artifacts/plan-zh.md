# 探索倡议托管的目标绑定变更工件

## 状态

尚未开始。已添加为未来的探索性工作项。框架已从通用的"可配置变更家园"更新为更精确的问题：共享的倡议工件何时可以成为可执行的、目标绑定的 OpenSpec 变更。

## 事实源

从 `../../direction.md` 出发，特别是当前的边界：

```text
上下文存储同步事实。
集合塑造事实。
倡议协调工作。
Workspace 打开本地视图。
变更实现仓库拥有的切片。
```

## 为什么存在

当前倡议方向假设 OpenSpec 变更通常存在于拥有实现的本地仓库中。这使验证、归档和规范同步保持在将要更改的代码附近。

某些协调工作可能需要在拥有仓库明确之前有一个共享家园。团队可能想要倡议托管的规划工件，以后可能希望其中一些工件成为特定仓库或规范根目录的实现就绪计划。

这不仅仅是一个存储偏好。共享工件在具有显式可移植目标绑定以及验证、应用、归档、规范同步和冲突处理的生命周期规则之前，仅用于规划。

## 目标

决定 OpenSpec 是否应支持倡议托管的工件，这些工件只有在绑定到实现目标后才能升级为可执行变更。

仓库本地变更仍然是默认的可执行实现工件。第 18 项应决定上下文存储托管的工件是否、何时以及如何安全地被视为变更。

答案应保留三个边界：

- 倡议协调共享上下文。
- 变更描述可执行的实现计划。
- Workspace 打开本地视图且不得暗示编辑权限。

## 要探索的模型

```text
倡议工件
  -> 默认仅用于规划
  -> 以后可能成为目标绑定

仓库本地变更
  -> 家园：repo/openspec/changes/<id>/
  -> 目标：隐式的当前仓库/规范根目录
  -> 生命周期：validate/apply/archive/spec sync 为仓库本地

倡议托管的目标绑定变更
  -> 家园：context-store/initiatives/<initiative>/changes/<id>/
  -> 目标：显式的仓库/规范根目录身份
  -> 生命周期：在目标解析设计之前不受支持

代理输出
  -> 报告工作目标
  -> 报告工件存放位置
  -> 报告实现目标（如果有）
  -> 报告此机器的允许编辑根目录
```

保持"变更家园"作为内部解析器语言。面向用户和面向代理的输出应优先使用更清晰的短语，如"计划位于仓库本地 OpenSpec"、"计划随倡议存在"和"可编辑目标"。

## 核心不变性

- 存储位置不暗示所有权、编辑权限或生命周期。
- 工作身份、工件家园、执行目标和允许的编辑根目录是分离的决策。
- 共享的上下文存储文件不得存储机器本地的检出路径。
- 无目标的倡议工件是简报、工作项或提案，而不是实现就绪的 OpenSpec 变更。
- 上下文存储托管的工件只有在具有显式目标元数据和生命周期命令支持后才能被视为可执行。
- 第 8 项保持仓库本地：`new change <id> --initiative ...` 仅创建或链接一个仓库本地变更。

## 要回答的问题

- 倡议下存在哪些确切的工件类型：工作项、简报、目标绑定变更或其他？
- 在倡议托管工件可执行之前，需要哪些可移植目标元数据？
- 本地解析如何将目标仓库身份映射到检出路径、OpenSpec 根目录、分支和允许的编辑根目录？
- 中央目标绑定变更是否需要显式的选择加入，如 `--home initiative`，还是倡议/存储策略可以选择此行为？
- 如果存在配置，显式 CLI 标志、仓库配置、倡议偏好、上下文存储默认、用户默认和内置仓库本地行为之间的确定性优先级是什么？
- `openspec new change` 如何在 JSON 中报告工作目标、工件家园、实现目标、倡议链接、操作上下文和后续命令？
- 当工件位于上下文存储中但目标规范位于仓库中时，validate、apply、archive 和 spec sync 如何表现？
- 倡议托管的目标绑定变更的归档是集中归档、实现仓库本地的交接变更，还是拒绝直到仓库本地变更存在？
- 哪些命令和技能界面仍然硬编码 `openspec/changes/`、当前工作目录或仓库本地编辑假设？
- 什么兼容性行为保留现有的仓库本地和 workspace 本地变更？

## 代理优先输出契约

任何创建、读取或解析此工作的未来命令都应使代理的下一步操作显式：

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

如果 `allowedEditRoots` 为空，代理不应编辑实现文件。如果需要目标选择，命令应返回选项或后续命令，而不是创建模糊的实现计划。

## 明确排除在范围之外

- 在模型决定之前实现上下文存储托管可执行变更。
- 自动将现有仓库本地变更移入上下文存储。
- 使倡议默认拥有实现工件。
- 使 workspace 级别的变更成为新的共享规划模型。
- 跨仓库的 apply、archive 或 validation 编排。
- 在共享的上下文存储文件中存储机器本地检出路径。
- 添加可能使普通仓库本地命令意外写入共享工件的全局默认值。

## 通过/不通过标准

在 OpenSpec 拥有一个覆盖以下内容的目标解析模型之前，不要实现倡议托管可执行变更：

- create 和 link 输出
- status、show、list 和 instructions 输出
- validate、apply、archive 和 spec sync 行为
- workspace 注册表和本地仓库映射行为
- 生成的技能指导和命令示例
- 工作目标、工件家园、实现目标、编辑根目录、不支持的声明周期命令和后续命令的 JSON 输出
