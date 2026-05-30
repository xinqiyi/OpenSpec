# 上下文存储与计划方案问题

## 开放

- 面向用户的命令词汇应该用 `context`、`store`，还是更面向产品的名称？
- 一旦计划方案存在，现有的工作空间 planning 变更应该获得什么样的迁移或兼容性路径？
- 链接的 repository 变更应如何向计划方案报告进度而不变成 Jira 克隆？
- monorepo 应如何映射能力、文件夹和 repository 本地变更？
- OpenSpec 是否应支持跨上下文存储和本地 OpenSpec repository 的可配置变更归属，以及什么样的所有权规则能使该模型安全？

## 已解决

- 工作空间不应是持久的共享 planning 对象。
- 计划方案路线图实现应在计划方案内部跟踪，直到需要 repository 拥有的实现变更。
- 第一个具体的上下文存储命令界面是 `context-store setup`、`context-store register`、`context-store list`/`ls` 和 `context-store doctor`。同步、push/pull、远程 repository 和冲突处理是未来的工作。
