# 工作项 01 证据

## 2026-05-20 初始方向锁定

在此工作项文件夹创建之前已完成：

- 向 `roadmap.md` 添加了已锁定的处置说明。
- 向 `direction.md` 添加了已锁定的产品边界。
- 将 `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md` 标记为历史参考。
- 将 `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md` 标记为历史参考。
- 将 `openspec/changes/workspace-reimplementation-roadmap/` 标记为历史参考。
- 将 `workspace-apply-repo-slice` 和 `workspace-verify-and-archive` 标记为推迟，直到与倡议关联的仓库本地变更存在。

研究发现：

- 当前的工作区设置、链接、重新链接、列出、打开、更新和诊断行为是有用的 beta 本地视图基础设施，应保留。
- 实时规范描述当前的工作区规划行为。在初始方向锁定期间不应重写它们；在行为变更之前，倡议制品应承载未来的产品意图。
- 现有的运行时行为应在倡议和关联的仓库本地变更能够取代工作区级规划之前保持不变。

验证：

- 初始方向锁定编辑后，`git diff --check` 通过。
- `openspec validate workspace-reimplementation-roadmap --no-interactive`、`openspec validate workspace-apply-repo-slice --no-interactive` 和 `openspec validate workspace-verify-and-archive --no-interactive` 失败，因为这些现有的活跃变更没有规范差异。这早于处置说明的措辞，被记录为活跃变更清理问题。

## 2026-05-21 倡议入口点

添加了 `README.md` 作为倡议入口点，并从 `.initiative.yaml` 链接到它。

README 解释了：

- 此倡议是产品意图的来源
- 方向、路线图、任务、决策、问题和工作项的阅读顺序
- 规范仍然是代码背后的当前行为契约
- 在行为变更之前，不应为未来意图重写规范

更新了 `work-items/01-lock-the-direction/tasks.md` 以标记倡议意图来源审查完成。

## 2026-05-21 历史工作区路线图审查

审查了历史工作区重新实现的入口点：

- `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md`
- `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md`
- `openspec/changes/workspace-reimplementation-roadmap/README.md`
- `openspec/changes/workspace-reimplementation-roadmap/proposal.md`
- `openspec/changes/workspace-reimplementation-roadmap/POC_REFERENCE_GUIDE.md`

在 `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md` 顶部附近添加了防护说明，指出其余部分为历史 POC 后续方向，不应视为活跃的实施指导。

路线图 README 和交接提示已引导代理首先查看倡议方向，并警告除非后续与倡议关联的仓库变更设计重新激活，否则不要继续旧的扁平同级队列。

## 2026-05-21 活跃工作区提案审查

审查了活跃的工作区提案制品：

- `workspace-reimplementation-roadmap`
- `workspace-agent-guidance`
- `workspace-apply-repo-slice`
- `workspace-verify-and-archive`

向 `workspace-apply-repo-slice` 和 `workspace-verify-and-archive` 添加了简短说明，澄清其余提案部分是为了以后参考而保留，而非丢弃，并应在倡议和与倡议关联的仓库本地变更存在后重新变得相关。

未改动 `workspace-agent-guidance`，因为它已有不相关的工作树编辑，应作为单独的活跃变更处置决策处理。

## 2026-05-21 用户面向文档决策

决策：除非当前用户面向行为描述有误，否则不在初始方向锁定期间更新 `docs/cli.md`。

理由：

- 方向锁定面向贡献者和决定下一步构建什么的代理。
- 用户面向文档应描述当前的 CLI 行为，而非未来的倡议意图。
- 倡议尚无 CLI 界面，因此在用户文档中宣布转向会在用户能够采取行动之前吸引对内部产品方向的关注。

当倡议或上下文存储命令存在时，或当前文档承诺了不可用的工作区应用、验证或归档行为时，重新审视用户面向文档。

验证：

- `git diff --check` 通过。
- 在此过程中未修改 `openspec/specs/` 或 `schemas/workspace-planning/` 下的文件。

## 2026-05-21 活跃变更处置

决策：将活跃的工作区变更保留为推迟的参考占位符。

理由：

- 工作区代理指导、应用、验证和归档在倡议基础设施建立后仍预期发挥重要作用。
- 当前的关注点应是上下文存储、倡议和与倡议关联的仓库本地变更。
- 保留这些提案保留了研究和连续性，而不会使其成为下一个实施队列。

后续：

- 在与倡议关联的仓库本地变更定义了持久的交接模型后，重新审视推迟的工作区变更。

## 最终项目 1 状态

项目 1 已完成。

已锁定的内容：

- 倡议制品是上下文存储、集合、倡议、工作区和仓库本地变更的产品意图来源。
- 规范和模式仍然是当前的行为契约，未因未来意图而编辑。
- 历史工作区路线图制品保留作为参考，而非活跃的发布队列。
- 推迟的工作区变更保留为活跃的参考占位符，因为其领域在倡议基础设施建立后预计仍将重要。
- 用户面向文档有意保持不变，除非它们错误描述了当前行为。

剩余风险：

- `openspec list` 仍将推迟的工作区变更为显示为活跃的无任务变更。目前这是有意的，但可能在视觉上显得杂乱。
- `workspace-agent-guidance` 有无关的工作树编辑，在未来的提交或归档决策前应谨慎处理。
- 未来的代理仍需先阅读倡议 README；历史工作区文档现在更安全了，但仍包含文件深处有用的旧生命周期细节。
