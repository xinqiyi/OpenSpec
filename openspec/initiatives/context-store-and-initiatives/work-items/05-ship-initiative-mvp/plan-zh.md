# 交付倡议 MVP

## 状态

创建/列出操作和 CLI 适配器切片已完成。完整的读取/显示、更新和删除策略推迟到后续的 agent 优先发现和生命周期工作。

## 唯一真实来源

从 `../../direction.md` 开始。

相关模型为：

```text
上下文存储同步真相。
集合塑造真相。
倡议协调工作。
workspace 打开本地视图。
变更实现 repository 拥有的切片。
```

## 目标

为协调工作提供一个持久、共享、agent 可消费的家园，位于 `initiatives/` 集合内。

## 路线图形状

默认倡议形状：

```text
initiatives/<id>/
 initiative.yaml
 requirements.md
 design.md
 decisions.md
 questions.md
 tasks.md
```

方向文档也为后续的 `contracts/` 内容留出空间：

```text
initiatives/<id>/
 contracts/
```

## 初始边界

- 倡议代码应位于 `src/core/context-store/` 之外。
- 上下文存储核心不应了解倡议语义。
- 倡议 API 应消费来自事项 4 的挂载 `initiatives` 集合。
- repository 本地 OpenSpec 变更仍然是实施构件；倡议协调意图、决策、问题和任务。
- 在此事项中不实现 workspace 打开、repository 解析、状态仪表板、同步或链接变更生命周期。

## 已锁定的方向

- 将倡议代码放在 `src/core/collections/initiatives/` 下。
- 在存在真正的 API 之前，不从 `src/core/index.ts` 导出倡议。
- 对运行时上下文存储倡议模型使用可见的 `initiative.yaml`，而不是隐藏的 `.initiative.yaml`。现有的路线图文件夹可能仍然携带遗留的 `.initiative.yaml` 进度元数据，直到该跟踪器被迁移或退役。
- 使用严格的 YAML 解析和验证，遵循现有的基础架构 schema。
- 不在倡议 MVP 中创建 `links.yaml`。repository 变更连接属于后续的 workspace/本地协调工作。
- 保持 Markdown 验证轻量；生成有用的结构，但暂不验证散文内容。
- 在挂载集合操作之前，从倡议架构和 template 辅助函数开始实施。
- 对于第一个挂载操作切片，仅添加创建和列出。避免广泛的 `readInitiative` API，直到"完整倡议"的形状更加清晰。
- 仅当子文件夹包含有效的 `initiative.yaml` 时才将其视为倡议。缺失 `initiative.yaml` 意味着"不是倡议"；无效的 `initiative.yaml` 意味着共享状态损坏，应大声失败。

## 从事项 5 推迟

- 完整的倡议显示/读取行为属于 agent 优先的倡议发现，等待返回形状更加清晰。
- 元数据更新和受保护删除属于后续的生命周期工作，等待创建/列出使用塑造策略。

## 初始 `initiative.yaml`

推荐的形状：

```yaml
version: 1
id: launch-billing-flow
title: 启动计费流程
summary: >
 协调产品、API 和客户端界面的计费启动。
status: exploring
created: "2026-05-21"
owners: []
metadata: {}
```

必需字段：

- `version`
- `id`
- `title`
- `summary`
- `status`
- `created`

默认或可选字段：

- `owners`
- `metadata`

初始状态：

- `exploring`（探索中）
- `active`（活跃）
- `complete`（完成）
- `archived`（已 archive）

## 初始 Markdown template

预先创建这些文件：

- `requirements.md`：产品意图、已接受的需求、范围之外。
- `design.md`：上下文、方法、受影响区域、依赖、风险。
- `decisions.md`：已接受的决策，包含日期/标题/决策/原因/影响。
- `questions.md`：开放和已解决的问题。
- `tasks.md`：仅协调任务，非 repository 实施任务。

推迟 `contracts/`、`README.md`、里程碑、依赖图、外部问题链接、workspace 路径映射、状态仪表板、`links.yaml` 和 Markdown 内容验证。

## 可能的 repository 切片

- 添加 `src/core/collections/initiatives/schema.ts`。
- 添加 `src/core/collections/initiatives/templates.ts`。
- 添加 `src/core/collections/initiatives/index.ts`。
- 在 `test/core/collections/initiatives/` 下添加聚焦测试。
- 添加类型、常量、ID 验证、严格的 `initiative.yaml` 解析/序列化辅助函数和默认 template 构建器。
- 在架构和 template 锁定后，添加创建/列出挂载集合操作。
- 保持上下文存储集合 API 不变，除非发现真正的集成缺口。

## 已实现的切片

- 添加了 `src/core/collections/initiatives/schema.ts`。
- 添加了 `src/core/collections/initiatives/templates.ts`。
- 添加了 `src/core/collections/initiatives/index.ts`。
- 在 `test/core/collections/initiatives/` 下添加了聚焦测试。
- 现在通过 `src/core/collections/index.ts` 导出倡议，因为已存在挂载的操作 API。
- 将 `links.yaml` 保留在倡议 MVP 文件合约之外。

## 操作切片方向

- 添加 `src/core/collections/initiatives/operations.ts`。
- 现在通过 `src/core/collections/index.ts` 导出倡议，因为已存在挂载的操作 API。
- `createInitiative` 应创建确切的 MVP 文件形状：`initiative.yaml`、`requirements.md`、`design.md`、`decisions.md`、`questions.md` 和 `tasks.md`。
- `createInitiative` 应通过可注入的日期提供者生成 `created`，如果倡议文件夹已存在则失败，并在写入失败时清理部分创建的文件夹。
- `listInitiatives` 应检查挂载的 `initiatives` 集合下的直接子目录，忽略没有 `initiative.yaml` 的文件夹，解析并验证带有 `initiative.yaml` 的文件夹，要求 `initiative.yaml.id` 与文件夹名称匹配，并按 id 排序返回倡议状态。

## 已实现的操作切片

- 添加了 `src/core/collections/initiatives/operations.ts`。
- 添加了 `createInitiative` 用于通过挂载的 `initiatives` 集合创建 MVP 文件夹形状。
- 添加了 `listInitiatives`，使用有效的 `initiative.yaml` 检测规则。
- 通过 `src/core/collections/index.ts` 导出倡议。
- 在 `test/core/collections/initiatives/operations.test.ts` 下添加了聚焦操作测试。

## 下一个集成使能器

在添加 `openspec initiative create/list` 之前，添加上下文存储注册/解析外观，使 CLI 代码能够解析命名存储并挂载倡议集合，而无需暴露原始注册表或元数据 YAML。

## CLI 适配器方向

将第一个倡议 CLI 接口添加为挂载集合操作之上的薄适配器：

```bash
openspec initiative create <id> --store <store-id> --title <title> --summary <summary>
openspec initiative create <id> --store-path <path> --title <title> --summary <summary>
openspec initiative list --store <store-id>
openspec initiative list --store-path <path>
```

使用 `initiative create/list` 作为有意的名词命名空间，类似于 `workspace` 和 `schema`，尽管较新的 OpenSpec 惯例通常偏好动词优先的顶层命令。更严格的选择会将倡议行为分散到 `new initiative` 和全局 `list` 标志上，这对于此切片来说表面更大，因为倡议命令必须解析上下文存储。

在第一个 CLI 切片中保持存储选择显式。要求使用 `--store <id>` 或 `--store-path <path>`，拒绝同时使用两者，暂不添加当前目录发现、单存储自动选择、交互式选择器、全局默认存储或 workspace 选定存储状态。

由于 shell 补全是手动注册的，添加运行时命令还需要将 `initiative create/list/ls` 添加到 `COMMAND_REGISTRY`。目前保持补全支持为静态：仅命令名称和标志，不进行动态存储 ID 或倡议 ID 补全。

## 已实现的 CLI 适配器切片

- 添加了 `src/commands/initiative.ts`。
- 从顶层 CLI 注册了 `openspec initiative create` 和 `openspec initiative list`。
- 添加了 `openspec initiative ls` 作为 list 的别名。
- 要求通过 `--store <id>` 或 `--store-path <path>` 进行显式上下文存储选择。
- 拒绝了冲突的 `--store` 和 `--store-path` 选择器。
- 返回 workspace 风格的 JSON 负载，带有顶层的 `status` 诊断数组。
- 为 `initiative create/list/ls` 添加了静态 shell 补全元数据。
- 在 `test/commands/initiative.test.ts` 下添加了聚焦命令测试。
