## 原因

目前，架构（工作流类型）必须在每个实验性工作流命令中通过 `--schema` 标志传递。这很重复且容易出错。代理无法知道变更使用哪个架构，因此它们默认使用 `spec-driven`，无法利用像 `tdd` 这样的替代工作流。

## 变更内容

**范围：仅实验性工件工作流**（`openspec new change`、`openspec status`、`openspec instructions`、`openspec templates`）

- 通过 `openspec new change` 创建变更时，将架构选择存储在 `.openspec.yaml` 元数据文件中
- 在实验性工作流命令中从元数据自动检测架构
- 使 `--schema` 标志变为可选（仅用于覆盖，元数据优先）
- 向 `openspec new change` 命令添加 `--schema` 选项

**不受影响**：遗留命令（`openspec validate`、`openspec archive`、`openspec list`、`openspec show`）

## 能力

### 新能力
- `change-metadata`：读取/写入每个变更的元数据文件

### 修改的能力
- `cli-artifact-workflow`：命令从变更元数据自动检测架构

## 影响

- **受影响的代码**：`src/utils/change-utils.ts`、`src/core/artifact-graph/instruction-loader.ts`、`src/commands/artifact-workflow.ts`
- **代理技能**：可以简化——不再需要显式传递架构
- **向后兼容**：没有 `.openspec.yaml` 的变更回退到 `spec-driven` 默认值
- **隔离**：所有变更都包含在实验性工作流代码中；遗留命令不受影响
