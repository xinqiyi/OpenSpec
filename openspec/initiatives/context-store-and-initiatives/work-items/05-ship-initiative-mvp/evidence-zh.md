# 交付倡议 MVP 证据

## 研究摘要

- 倡议代码应位于 `src/core/collections/initiatives/` 目录下，在 `src/core/context-store/` 之外。
- 倡议 API 应消费来自事项 4 的挂载 `initiatives` 集合，而不是原始上下文存储根。
- 第一个编码切片应在挂载的创建/列出操作之前锁定元数据和 template。
- 对于新的共享倡议模型，优先使用可见的 `initiative.yaml`。
- 倡议 MVP 中不应存在 `links.yaml`。repository 变更连接是 workspace/本地协调的问题，留待以后处理。
- 读取/显示、更新和删除有额外的策略风险，因此创建/列出应在更广泛的生命周期行为之前实现。
- 第一个挂载操作切片应仅做创建/列出。完整的 `readInitiative` API 推迟到返回形状更加清晰时再实现。

## 决策

- 使用 `src/core/collections/initiatives/` 存放倡议领域代码。
- 不要将倡议语义放入 `src/core/context-store/`。
- 添加 `initiative.yaml` 严格解析/序列化辅助函数。
- 提前生成 Markdown 文件，但首次通过时仅验证存在性和 template，不验证 Markdown 内容。
- 推迟 workspace 打开、repository 解析、状态仪表板、同步、链接变更生命周期、`links.yaml`、`contracts/` 和 CLI 行为。
- 通过有效的 `initiative.yaml` 检测倡议：缺失意味着忽略，无效意味着大声失败，且 YAML 中的 `id` 必须与文件夹名称匹配。

## 建议的第一个编码切片

添加：

- `src/core/collections/initiatives/schema.ts`
- `src/core/collections/initiatives/templates.ts`
- `src/core/collections/initiatives/operations.ts`
- `src/core/collections/initiatives/index.ts`
- `test/core/collections/initiatives/` 下的聚焦测试

覆盖：

- 倡议文件名的常量
- `validateInitiativeId`
- 严格的 `initiative.yaml` 解析/序列化
- 通过挂载的 `initiatives` 集合的创建/列出操作
- `requirements.md`、`design.md`、`decisions.md`、`questions.md` 和 `tasks.md` 的 template 构建器
- 有效和无效元数据、无效 ID、未知 YAML 字段、必需的 `created` 以及生成的 template 名称/内容形状的测试

## 实施证据

- `src/core/collections/initiatives/schema.ts` 定义倡议常量、严格的持久化 `initiative.yaml` 解析/序列化、必需的 `created`、有界的 JSON 类元数据、状态和可移植的 kebab-case 倡议 ID。
- `src/core/collections/initiatives/templates.ts` 为需求、设计、决策、问题和任务定义确定性的默认 Markdown 文件构建器。
- `src/core/collections/initiatives/index.ts` 仅在倡议模块内部导出倡议架构/template 接口。
- `src/core/collections/initiatives/operations.ts` 使用有效的 `initiative.yaml` 检测规则创建 MVP 倡议文件夹并列出倡议状态。
- `src/core/collections/index.ts` 现在导出倡议模块，因为它有了挂载的操作 API。
- `test/core/collections/initiatives/schema.test.ts` 覆盖文件常量、无 `links.yaml`、ID 验证、严格 YAML 行为、必需的 `created`、默认所有者/元数据、元数据验证和序列化往返。
- `test/core/collections/initiatives/templates.test.ts` 覆盖生成的 Markdown 文件名、确定性排序、尾随换行符和预期的章节标题。
- `test/core/collections/initiatives/operations.test.ts` 覆盖创建、列出、重复保护、部分写入失败时的清理、缺失 `initiative.yaml` 被忽略、无效 `initiative.yaml` 失败以及文件夹/ID 不匹配失败。
- `src/core/context-store/registry.ts` 作为下一个集成使能器添加，在 CLI 连接之前。
- `src/commands/initiative.ts` 添加 `openspec initiative create/list` 作为上下文存储外观和挂载的倡议集合之上的薄 CLI 适配器。
- `src/cli/index.ts` 注册倡议命令。
- `src/core/completions/command-registry.ts` 注册 `initiative create/list/ls` 的静态补全元数据。
- `test/commands/initiative.test.ts` 覆盖 JSON 创建、`--store-path` 列表、人类输出、选择器错误、重复创建错误和补全注册表条目。

## 验证

- `pnpm exec vitest run test/core/collections/initiatives/schema.test.ts test/core/collections/initiatives/templates.test.ts`
- `pnpm exec vitest run test/core/collections/initiatives/operations.test.ts`
- `pnpm exec vitest run test/core/collections/initiatives/schema.test.ts test/core/collections/initiatives/templates.test.ts test/core/collections/initiatives/operations.test.ts test/core/collections/runtime.test.ts test/core/context-store/foundation.test.ts test/core/planning-home.test.ts`
- `pnpm exec vitest run test/commands/initiative.test.ts`
- `pnpm exec vitest run test/core/context-store/registry.test.ts test/core/collections/initiatives/operations.test.ts test/core/collections/initiatives/schema.test.ts test/core/collections/initiatives/templates.test.ts test/core/collections/runtime.test.ts`
- `pnpm exec vitest run test/commands/workspace.test.ts`
- `pnpm run build`
- `pnpm run lint`
- `git diff --check`
