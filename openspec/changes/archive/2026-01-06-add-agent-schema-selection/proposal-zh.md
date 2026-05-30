## 为什么

在有了每次变更的 schema 元数据之后（参见 `add-per-change-schema-metadata`），agent 现在可以使用不同的 workflow schema 创建变更。然而，agent skill 仍然硬编码为 `spec-driven` artifact，并且不向用户提供 schema 选择。

## 变更内容

**范围：实验性 artifact workflow agent skill**

**依赖：** `add-per-change-schema-metadata`（必须首先实现）

- 更新 `openspec-new-change` skill 以提示用户选择 schema
- 更新 `openspec-continue-change` skill 以适用于任何 schema 的 artifact
- 更新 `openspec-apply-change` skill 以处理 schema 特定的任务结构
- 添加 schema 描述以帮助用户选择适当的 workflow

## 能力

### 修改的能力
- `cli-artifact-workflow`：Agent skill 支持动态 schema 选择

## 影响

- **受影响的代码**：`src/core/templates/skill-templates.ts`
- **用户体验**：用户可以在开始变更时选择 TDD、spec-driven 或未来的 workflow
- **Agent 行为**：skill 从 schema 中读取 artifact 列表而非硬编码
- **向后兼容**：如果用户不选择，默认保持为 `spec-driven`
