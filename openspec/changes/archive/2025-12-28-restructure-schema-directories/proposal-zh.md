## 为什么

目前，内置 schema 作为 TypeScript 对象嵌入在 `builtin-schemas.ts` 中。这对 schema 本身可行，但不支持同位置 template。为了实现自包含的 schema 包（schema + template 一起），我们需要将 schema 重构为目录结构。

## 变更内容

- **破坏性变更（内部）：** 将内置 schema 从嵌入的 TS 对象迁移到实际的目录结构
- Schema 变为包含 `schema.yaml` + `templates/` 的目录
- 更新 `resolveSchema()` 以从目录结构加载
- 移除 `builtin-schemas.ts`（由基于文件的 schema 替代）
- 更新解析逻辑，按用户目录 → 包目录的顺序检查

## 影响

- 受影响的 spec：`artifact-graph`（schema 解析变更）
- 受影响的代码：
 - 移除 `src/core/artifact-graph/builtin-schemas.ts`
 - 更新 `src/core/artifact-graph/resolver.ts`
 - 在包根目录添加 `schemas/` 目录
- 无外部 API 变更（解析仍返回 `SchemaYaml`）
