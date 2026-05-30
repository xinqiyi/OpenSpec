# 添加以代理为先的倡议发现证据

## 对话决策

- `initiative show <id>` 应作为代理的定位/发现命令。
- 该命令应回答用户指的是哪个倡议、权威上下文在哪里、以及倡议元数据在哪里。
- 该命令不应拼接 markdown、总结倡议内容、计算工作进度、解析本地仓库、列出关联变更或打开工作区。
- 默认查找应搜索所有已注册的上下文存储。
- `--store <id>` 应消除歧义或过滤到某个已注册的存储。
- `--store-path <path>` 应保留作为显式本地路径的应急出口。
- 跨存储的重复倡议 ID 应报歧义错误。
- 当任何已注册的存储不可读时，默认的全存储查找应失败，因为唯一性不可知。
- 显式 `--store` 和 `--store-path` 查找只关心所选存储。
- `initiative.status` 应从 v1 输出投影中省略。
- `owners` 应从 v1 输出投影中省略。
- 任意 `metadata` 应从 v1 输出投影中省略。
- `version` 和 `created` 应保留在 v1 倡议投影中。
- `files` 应从 v1 中省略。
- `initiative.metadata_path` 应指向已验证的 `initiative.yaml`。
- `initiative.root` 足以让代理使用常规文件系统工具检查文件夹。
- 顶级 `matches` 应省略。歧义和不完全查找的候选者应放在需要它们的诊断信息下，例如 `status[0].details.matches`。
- `context_store.source` 应从 `initiative show` v1 中省略，因为它是选择器来源而非上下文存储身份。
- 顶级 `resolution` 字段在 v1 中不需要。
- 现有的 `initiative create/list` 输出可以暂时保留 `context_store.source`；本项目不应重构旧的输出形状。
- `readInitiative` 在确切的倡议不存在时应返回 `null`，在 `initiative.yaml` 存在但无效或 ID 错误时应抛出异常。
- 在默认全存储查找中，任何不可读的已注册存储都应将主要错误设为 `initiative_lookup_incomplete`，即使可读存储中有部分匹配。
- 如果 `initiatives/<id>/initiative.yaml` 存在但无效或 ID 错误，`initiative show` 应将其视为损坏的倡议状态而非该存储未找到。
- 成功时的人类可读输出应是紧凑的定位器视图：标题、ID、摘要、上下文存储、位置和规范文件名。
- 人类可读的歧义和不完全查找错误应内联显示匹配或部分匹配的存储，然后指向下一个命令。
- 应为 `initiative show` 提供静态 shell 补全元数据。
- 存储 ID 和倡议 ID 的动态补全应继续推迟。

## 研究笔记

- 当前的倡议 create/list 输出散布了完整的解析后 `initiative.yaml` 状态，这对 MVP 有用但对于第一个 `show` 合约来说过于宽泛。
- 优先实现专注的按倡议读取操作，而不是通过 `listInitiatives` 来实现 `show`，因为精确查找不应因不相关的格式错误的倡议文件夹而失败。
- 其他倡议文件是模式/配置相关的，不应硬编码到 `show` 中。
- 将候选者放在诊断细节内部遵循与 GraphQL 风格响应相同的一般形状：成功数据保持干净，而特定于错误的上下文随错误一起传递。
- 如果以后需要选择器来源，添加一个单独的显式字段如 `resolution`，而不是将来源放在 `context_store` 内部。
- 人类可读输出应保持紧凑：标题、ID、摘要、上下文存储、位置和元数据路径。

## 实施证据

- `src/core/collections/initiatives/operations.ts` 添加了用于精确倡议查找的 `readInitiative`。
- `src/commands/initiative.ts` 添加了 `initiative show <id>`，支持全存储默认查找、`--store`、`--store-path`、JSON 输出、紧凑人类输出、歧义诊断和不完全查找诊断。
- `src/core/completions/command-registry.ts` 为 `initiative show` 添加了静态补全元数据。
- `test/core/collections/initiatives/operations.test.ts` 覆盖了精确读取、倡议不存在、无效精确倡议、ID 不匹配和不相关的无效文件夹。
- `test/commands/initiative.test.ts` 覆盖了 `initiative show` 成功、`--store-path`、人类输出、歧义、不完全查找、未找到、无效精确倡议状态、无 `context_store.source`、无 `files`、无顶级 `matches` 和静态补全。

## 验证

- `pnpm run build`
- `pnpm exec vitest run test/core/collections/initiatives/operations.test.ts`
- `pnpm exec vitest run test/commands/initiative.test.ts`
- `pnpm exec vitest run test/commands/context-store.test.ts test/commands/initiative.test.ts test/core/context-store/foundation.test.ts test/core/context-store/registry.test.ts test/core/collections/initiatives/operations.test.ts`
- `pnpm run lint`
- `git diff --check`
- 对倡议路线图、任务跟踪器和项目 7 工作项说明进行 Markdown 行长度检查。
