# 添加上下文存储基础 - 证据

## 研究摘要

现有的 OpenSpec 模式指向一个小的显式基础：

- 全局数据使用来自 `getGlobalDataDir()` 的 XDG/平台位置。
- 工作区注册表是全局数据下的机器本地便捷索引。
- 工作区可移植状态使用版本化 YAML 和严格的 Zod 验证。
- 现有的读/写助手在写入前验证状态，并使用 `FileSystemUtils.writeFile()` 创建父目录。
- Schema/后端风格代码倾向于小型显式适配器和注册表，而不是重型框架抽象。

## 决策

- 第一个上下文存储后端仅是 Git/本地检出配置。
- OpenSpec 记录本地检出位置；它不决定默认在哪里克隆真实团队存储。
- 本地注册表不是事实来源。它是机器本地索引。
- 存储根元数据是同步存储的可移植身份来源。
- 倡议和集合是后来的消费者，不是存储基础的一部分。
- 一个薄外观层应在倡议 CLI 接线之前隐藏原始注册表/元数据写入。

## 实施证据

- `src/core/context-store/registry.ts` 注册 Git/本地上下文存储、列出本地注册表条目，并通过元数据 ID 验证解析已注册的存储。
- `src/core/context-store/index.ts` 导出外观层。
- `test/core/context-store/registry.test.ts` 覆盖注册、注册表合并/更新、元数据不匹配拒绝、列出、解析、缺失或不匹配的元数据，以及从解析的根挂载倡议集合。

## 验证

- `pnpm exec vitest run test/core/context-store/foundation.test.ts`
- `pnpm exec vitest run test/core/context-store/registry.test.ts`
- `pnpm run build`
- `pnpm run lint`
- `git diff --check`
