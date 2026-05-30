## 原因

我们希望将 `spec-driven` 重命名为 `openspec-default`，以更好地反映它是标准/默认工作流。然而，直接重命名会破坏现有项目中在 `openspec/config.yaml` 中设置了 `schema: spec-driven` 的项目。添加别名支持允许两个名称互换使用，从而实现平滑过渡，不会产生破坏性变更。

## 变更内容

- 在模式解析器中添加模式别名解析功能
- `openspec-default` 和 `spec-driven` 都将解析为同一模式
- 物理目录保持为 `schemas/spec-driven/`（或者可以重命名为 `schemas/openspec-default/`，并将 `spec-driven` 作为别名）
- 所有 CLI 命令和配置文件都接受任一名称
- 现有用户配置无需更改

## 能力

### 新能力

- `schema-aliases`：支持模式名称别名，使多个名称可以解析到同一模式目录

### 修改的能力

<!-- 没有现有的规格级别行为发生变化——这纯粹是新增功能 -->

## 影响范围

- `src/core/artifact-graph/resolver.ts` - 添加别名解析逻辑
- `schemas/` 目录 - 可能将 `spec-driven` 重命名为 `openspec-default`
- 文档 - 更新以优先使用 `openspec-default`，同时注明 `spec-driven` 仍然可用
- 默认模式常量 - 将 `DEFAULT_SCHEMA` 更新为 `openspec-default`
