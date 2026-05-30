# 工作项 01：锁定方向

## 目标

使 workspace 到倡议的转变足够明确，以至于未来的 agent 和贡献者不会继续实现旧的"workspace 拥有计划"模型。

锁定的模型是：

```text
上下文存储同步真理。
集合塑造真理。
倡议协调工作。
workspace 打开本地视图。
变更实现 repository 拥有的切片。*
```

## 方向

此工作项是非 spec 的方向传递，而非运行时移除。

spec 应继续描述代码背后的当前行为契约。产品意图、路线图决策和未来方向应存在于倡议制品中，直到后续的实施变更有意更新行为及其 spec。

保留：

- workspace 设置、链接、重新链接、列出、打开、更新和诊断
- 链接的 repository 和文件夹作为本地 planning 上下文
- workspace 本地 skill 作为本地 agent 指导
- "workspace 可见性不等于变更承诺"

标记为过渡性：

- workspace 级 `changes/` planning
- `workspace-planning` schema
- workspace 范围的状态/指令兼容性

推迟：

- workspace 应用、验证和 archive 作为一等生命周期命令
- 分支/工作树编排
- 强跨 repository 验证
- 依赖图执行

取代：

- workspace 作为持久的共享 planning 家园
- workspace 级 planning 制品作为 spec 的跨 repository 计划
- workspace 变更 planning 作为长期权威来源

## 现在需要审查的文件

- `openspec/initiatives/context-store-and-initiatives/*.md`
- `openspec/initiatives/context-store-and-initiatives/work-items/**/*.md`
- `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md`
- `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md`
- `openspec/changes/workspace-reimplementation-roadmap/*`
- 活跃的 `openspec/changes/workspace-*` proposal
- `docs/cli.md`

## 现在保持不动的文件

- `openspec/specs/**/*.md`
- `schemas/workspace-planning/**`

这些文件应仅在我们有意更改行为或创建更新相关行为契约的 repository 所有实施变更时更改。

## 非目标

- 不要移除当前的 workspace planning 运行时行为。
- 不要删除 `workspace-planning` schema。
- 在倡议替代品存在之前，不要添加 CLI 弃用警告。
- 不要在此工作项中实现上下文存储。
- 不要作为初始方向锁定的一部分编辑 OpenSpec spec。

## 完成条件

- 倡议制品清晰承载产品意图和路线图决策。
- 历史 workspace 路线图制品不再读起来像是活跃的发布队列。
- 用户面向文档将当前 workspace 描述为本地视图，只要这不与当前行为矛盾。
- 现有的 workspace planning 行为在倡议和路线图制品中被清晰视为当前行为，而非未来的产品模型。
- workspace 应用、验证和 archive 被清晰标记为推迟。
- 新 agent 能够识别倡议方向为权威来源。
