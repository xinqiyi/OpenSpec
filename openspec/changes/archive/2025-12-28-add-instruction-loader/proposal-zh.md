## 为什么

切片 1（artifact-graph）提供了图操作和状态检测。切片 2（change-utils）提供了变更创建功能。现在我们还需要能够加载 artifact 的 template，并用变更特定的上下文丰富 template，以便用户/agent 知道接下来要创建什么。

## 变更内容

- 添加从 schema 目录解析 template 的功能（使用 `restructure-schema-directories` 的结构）
- 添加上下文丰富功能，将变更上下文注入 template
- 添加用于 CLI 输出的状态格式化功能
- 新的 `instruction-loader` 能力

## 依赖关系

- 需要先实现 `restructure-schema-directories`（schema 作为带有同位置 template 的目录）

## 影响

- 受影响的 spec：新的 `instruction-loader` spec
- 受影响的代码：`src/core/artifact-graph/`（新文件）
- 构建于：`artifact-graph`（切片 1），使用 `ArtifactGraph`、`detectCompleted`、`resolveSchema`
