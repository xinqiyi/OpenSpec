## 为什么

在有了每次变更的模式元数据之后（参见 `add-per-change-schema-metadata`），agent 现在可以使用不同的工作流模式创建变更。然而，agent 技能仍然硬编码为 `spec-driven` 工件，并且不向用户提供模式选择。

## 变更内容

**范围：实验性工件工作流 agent 技能**

**依赖：** `add-per-change-schema-metadata`（必须首先实现）

- 更新 `openspec-new-change` 技能以提示用户选择模式
- 更新 `openspec-continue-change` 技能以适用于任何模式的工件
- 更新 `openspec-apply-change` 技能以处理模式特定的任务结构
- 添加模式描述以帮助用户选择适当的工作流

## 能力

### 修改的能力
- `cli-artifact-workflow`：Agent 技能支持动态模式选择

## 影响

- **受影响的代码**：`src/core/templates/skill-templates.ts`
- **用户体验**：用户可以在开始变更时选择 TDD、spec-driven 或未来的工作流
- **Agent 行为**：技能从模式中读取工件列表而非硬编码
- **向后兼容**：如果用户不选择，默认保持为 `spec-driven`
