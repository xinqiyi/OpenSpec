# 上下文存储项目根与 Schema 驱动的倡议实证

## 手动 Beta 测试发现

- 一个全新 agent 风格的提示成功在已注册的 `team-context` 上下文存储中创建了 `agent-trace-hooks`。
- 当前的 CLI 创建了以下硬编码文件集：

```text
initiative.yaml
requirements.md
design.md
decisions.md
questions.md
tasks.md
```

- 生成的 Markdown template 以 `TBD` 占位符开头。
- agent 填充了这些文档，内容看似合理但未经审阅的 planning 内容。
- 我们手动将测试倡议缩减为精简形态：

```text
initiative.yaml
brief.md
```

- `openspec initiative show team-context/agent-trace-hooks --json` 和 `openspec initiative list --store team-context --json` 仍然能解析，这证明当前的标识/列表逻辑不要求六文件包。

## 代码观察

- 倡议文件名在 `src/core/collections/initiatives/schema.ts` 中硬编码。
- 倡议 Markdown template 在 `src/core/collections/initiatives/templates.ts` 中硬编码。
- `createInitiative` 在 `src/core/collections/initiatives/operations.ts` 中写入 `initiative.yaml`，然后写入所有默认 template 文件。
- `initiative create --json` 从 `src/commands/initiative.ts` 中的 `INITIATIVE_FILE_NAMES` 报告 `created_files`。
- 倡议列表/显示仅读取 `initiative.yaml`。
- 项目本地 schema 解析已经在 `src/core/artifact-graph/resolver.ts` 中使用 `<projectRoot>/openspec/schemas/<name>/schema.yaml`。
- 项目配置已经在 `src/core/project-config.ts` 中读取 `<projectRoot>/openspec/config.yaml`。
- 变更产物状态/指令通过 `src/core/artifact-graph/instruction-loader.ts` 与 repository 本地变更上下文耦合。
- planning 家园检测当前将包含 `openspec/` 的祖先视为可能的 repository planning 根，因此向上下文存储添加配置需要安全检查。

## UX/产品检查

推荐的用户含义：

```text
上下文存储 = 共享的 OpenSpec 上下文项目
倡议 = 迭代的高级 planning 对象
repository 变更 = 实现计划
workspace = 本地视图
```

文档应避免说倡议仅用于跨 repository 或跨团队工作。用户选择上下文存储可能仅仅是因为他们希望将 OpenSpec 产物放在实现 repository 之外。

`initiative create` 应创建最小可用的共享对象，然后通过状态/指令教会 agent 如何继续。它不应在审阅之前假装需求、决策和任务已经存在。

## 架构检查

可行的最小路径：

1. 将上下文存储根视为项目根，用于配置/schema 解析。
2. 在上下文存储设置期间创建 `openspec/config.yaml`。
3. 使用 `projectRoot = contextStoreRoot` 解析倡议 schema。
4. 使用产物图原语添加倡议特定的状态/指令辅助工具。
5. 更改倡议创建为写入精简外壳。

主要风险：

- 添加新的顶层 `schema` 字段时严格的 `initiative.yaml` 解析
- 当前断言六文件 MVP 契约的测试
- 当前告诉 agent 编辑五个生成的 Markdown 文件的文档和生成的 agent 指导
- 倡议 planning 产物与 repository 本地实现任务之间的歧义
- 上下文存储根在获得 `openspec/config.yaml` 后意外成为 repository planning 家园

## 子 agent/研究笔记

三次聚焦检查得出了相同的方向。

架构检查：

- 将上下文存储建模为 OpenSpec planning 根：

```text
context-store/
 .openspec-store/store.yaml
 openspec/config.yaml
 openspec/schemas/
 initiatives/
```

- 保留 `.openspec-store/store.yaml` 作为存储标识，`openspec/config.yaml` 作为行为/配置。
- 以上下文存储根为项目根，重用项目本地配置和 schema 解析。
- 添加倡议特定的产物上下文，而不是强制倡议通过 repository 本地变更上下文。
- 保护 planning 家园发现，使拥有 `openspec/config.yaml` 的上下文存储不会成为意外的实现 repository。

UX/产品检查：

- 将上下文存储描述为 OpenSpec 管理的 planning 家园。它可以用于跨 repository 协调，但也可以仅仅是为了将 OpenSpec 产物保留在实现 repository 之外。
- 使 `initiative create` 精简：`initiative.yaml` 加上一个种子产物如 `brief.md`。
- 添加状态/指令输出，使 agent 仅在存在已审阅内容需要捕获时才创建需求和设计产物。
- 停止将默认的倡议产物视为用户或 agent 应立即填写的文件。

发布风险评估：

- 保持旧的六文件 beta 倡议可读。
- 更新断言旧生成文件列表的测试。
- 在元数据版本化设计之前，避免对 `initiative.yaml` 进行严格的顶层添加。
- 将上下文存储托管的可执行变更推迟到可配置变更家园工作中，而不是将其打包到此切片中。
