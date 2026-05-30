# 工作项 01 任务

## 跟踪设置

- [x] 创建倡议级 `tasks.md`、`decisions.md` 和 `questions.md`。
- [x] 创建 `work-items/01-lock-the-direction/`。
- [x] 记录为什么路线图实施在倡议内部跟踪，而不是创建新的 OpenSpec 变更。

## 已捕获的方向锁定

- [x] 向 `roadmap.md` 添加已锁定的处置说明。
- [x] 向 `direction.md` 添加已锁定的产品边界。
- [x] 将 `openspec/changes/workspace-reimplementation-roadmap/START_HERE.md` 标记为历史参考。
- [x] 将 `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md` 标记为历史参考。
- [x] 将 `workspace-reimplementation-roadmap` 标记为历史参考。
- [x] 将 `workspace-apply-repo-slice` 标记为推迟。
- [x] 将 `workspace-verify-and-archive` 标记为推迟。

## 非 spec 方向传递

- [x] 保持 OpenSpec spec 不变，直到行为变更。
- [x] 审查倡议制品，确保有清晰的意图来源说明。
- [x] 审查历史 workspace 路线图制品，查找任何仍指示 agent 继续旧发布队列的语言。
- [x] 审查活跃的 workspace proposal 制品，查找任何仍将 workspace 应用、验证或 archive 呈现为下一步的语言。
- [x] 决定用户面向文档现在是否需要更改；默认为否，除非它们错误描述了当前行为。
- [x] 记录决策：spec 保持当前行为契约，而倡议文档承载未来产品意图。

## 活跃变更处置

- [x] 决定 `workspace-agent-guidance` 是否应重新定义、关闭或保留为本地视图指导项。
- [x] 决定无任务的推迟 workspace 变更应保持活跃、移至 archive，还是仅由倡议工作项代表。

## 验证

- [x] 运行 `git diff --check`。
- [x] 确认在此过程中未修改 OpenSpec spec。
- [x] 在 `evidence.md` 中记录证据。
