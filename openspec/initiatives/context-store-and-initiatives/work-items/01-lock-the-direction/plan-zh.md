# 工作项 01：锁定方向

## 目标

使工作区到倡议的转变足够明确，以至于未来的代理和贡献者不会继续实现旧的"工作区拥有计划"模型。

锁定的模型是：

```text
上下文存储同步真理。
集合塑造真理。
倡议协调工作。
工作区打开本地视图。
变更实现仓库拥有的切片。*
```

## 方向

此工作项是非规范的方向传递，而非运行时移除。

规范应继续描述代码背后的当前行为契约。产品意图、路线图决策和未来方向应存在于倡议制品中，直到后续的实施变更有意更新行为及其规范。

保留：

- 工作区设置、链接、重新链接、列出、打开、更新和诊断
- 链接的仓库和文件夹作为本地规划上下文
- 工作区本地技能作为本地代理指导
- "工作区可见性不等于变更承诺"

标记为过渡性：

- 工作区级 `changes/` 规划
- `workspace-planning` 模式
- 工作区范围的状态/指令兼容性

推迟：

- 工作区应用、验证和归档作为一等生命周期命令
- 分支/工作树编排
- 强跨仓库验证
- 依赖图执行

取代：

- 工作区作为持久的共享规划家园
- 工作区级规划制品作为规范的跨仓库计划
- 工作区变更规划作为长期权威来源

## 现在需要审查的文件

- `openspec/initiatives/context-store-and-initiatives/*.md`
- `openspec/initiatives/context-store-and-initiatives/work-items/**/*.md`
- `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md`
- `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md`
- `openspec/changes/workspace-reimplementation-roadmap/*`
- 活跃的 `openspec/changes/workspace-*` 提案
- `docs/cli.md`

## 现在保持不动的文件

- `openspec/specs/**/*.md`
- `schemas/workspace-planning/**`

这些文件应仅在我们有意更改行为或创建更新相关行为契约的仓库所有实施变更时更改。

## 非目标

- 不要移除当前的工作区规划运行时行为。
- 不要删除 `workspace-planning` 模式。
- 在倡议替代品存在之前，不要添加 CLI 弃用警告。
- 不要在此工作项中实现上下文存储。
- 不要作为初始方向锁定的一部分编辑 OpenSpec 规范。

## 完成条件

- 倡议制品清晰承载产品意图和路线图决策。
- 历史工作区路线图制品不再读起来像是活跃的发布队列。
- 用户面向文档将当前工作区描述为本地视图，只要这不与当前行为矛盾。
- 现有的工作区规划行为在倡议和路线图制品中被清晰视为当前行为，而非未来的产品模型。
- 工作区应用、验证和归档被清晰标记为推迟。
- 新代理能够识别倡议方向为权威来源。
