## 为什么

状态：已被上下文存储和倡议方向推迟。apply 即实现的原则仍然有用，但持久化的交接应围绕链接到 repository 本地 OpenSpec 变更的倡议来设计，而不是围绕 workspace 拥有的跨 repository 计划。在此链接存在之前，不要将其作为一等公民的 workspace 生命周期命令实现。

剩余部分保留了原始的 workspace apply 方向以供后续参考。在倡议和与倡议链接的 repository 本地变更存在后，这项工作仍预计会发挥作用；它不是当前立即关注的重点。

在 workspace proposal 存在之后，用户需要一种实用的方式来一次实现一个 repository 切片。

在适当的 workspace 模型中，apply 意味着实现：

```text
获取选定的 workspace 变更。
获取选定的 repository 切片。
打开或使用正确的检出。
实现该切片，同时保留 workspace 计划。
```

它不应意味着将 planning 文件复制或物化到每个 repository 中作为用户面对的 workflow。

## 变更内容

添加 workspace 变更的 repository 切片 apply workflow：

- 选择一个 workspace 变更
- 选择一个目标 repository 别名
- 解析该别名的本地检出
- 向 agent 提供 workspace 计划和 repository 特定的实现上下文
- 跟踪进度，不使 workspace 失去对计划的所有权

该 workflow 应支持跨不同分支或会话的实现，同时保持 workspace proposal 作为连续性层。

planning 依赖：

- 依赖于 `workspace-change-planning`。

## 能力

### 新能力

- `workspace-repo-slice-apply`：将 workspace 变更的一个 repository 切片作为实现 workflow 应用。

### 修改的能力

- `cli-artifact-workflow`：将 workspace apply 定义为实现而非物化。
- `context-injection`：从 workspace 变更提供 repository 特定的实现上下文。

## 影响

- workspace apply 命令行为。
- 用于 repository 切片实现的 agent 交接文本。
- 本地检出解析和分支/工作树假设。
- 测试 apply 操作在一个目标 repository 切片上运行，并且不需要复制 workspace planning artifact 作为主要用户契约。
