# 拟议倡议下一步 / Agent 交接用户体验证据

## 来源

此讨论项来自 GSD workspace 比较。

GSD 的有用经验不是其存储模型。而是其简单的用户循环：
创建上下文，推进到下一个具体步骤，防止 Agent 猜测自己在 workflow 中的位置。

OpenSpec 应保持当前的边界：

```text
上下文存储同步事实。
倡议协调工作。
workspace 打开本地视图。
变更实现 repository 拥有的切片。
```

可能存在的差距是 `initiative show`、repository 本地变更链接和 workspace 打开可能仍然需要 Agent 手动拼接下一步操作。

## 当前建议

将此保留为讨论草稿，直到 workspace 倡议打开更加清晰。如果被接受，第一个版本应该是一个小型交接/就绪命令，而不是状态、进度、仪表板或 workspace 编排。

## 手动 Beta 测试补充

2026-05-28 的手动 Beta 测试发现，命令级别的交接并不是唯一缺失的层。一个新 Agent 还需要一个小的、工具可读的指南，来了解如何整体使用 OpenSpec：

- 在猜测之前检查上下文存储、倡议、workspace 和 repository 本地变更；
- 理解上下文存储可以是实现 repository 之外的产物存放位置，而不仅仅是跨团队协调空间；
- 理解当用户希望产物放在 repository 中时，repository 本地变更拥有实施 planning 的所有权；
- 将 workspace 视为本地视图，而不是持久的 planning 空间；
- 在可用时路由到更狭窄的 OpenSpec workflow skill。

作为临时的 Beta 辅助工具，在 `.codex/skills/use-openspec/` 创建了一个手动 Codex skill，其中包含共享上下文和产物放置的参考信息。这尚未在配置器中产品化。
