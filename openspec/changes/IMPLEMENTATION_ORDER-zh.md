# 实现顺序和依赖关系

## 必需的实现顺序

由于依赖关系，以下变更必须按此特定顺序实现：

### 阶段 1：基础
**1. add-zod-validation**（无依赖）
- 创建所有核心模式（RequirementSchema、ScenarioSchema、SpecSchema、ChangeSchema、DeltaSchema）
- 实现 Markdown 解析器工具
- 实现验证基础设施和规则
- 建立所有命令使用的验证模式
- 必须首先完成

### 阶段 2：变更命令
**2. add-change-commands**（依赖：add-zod-validation）
- 从 zod 验证导入 ChangeSchema 和 DeltaSchema
- 重用 Markdown 解析工具
- 使用内置验证实现变更命令
- 使用验证基础设施进行变更验证子命令
- 在模式和验证存在之前无法开始

### 阶段 3：规范命令
**3. add-spec-commands**（依赖：add-zod-validation、add-change-commands）
- 从 zod 验证导入 RequirementSchema、ScenarioSchema、SpecSchema
- 重用 Markdown 解析工具
- 使用内置验证实现规范命令
- 使用验证基础设施进行规范验证子命令
- 建立在变更命令建立的模式之上

## 依赖图谱
```
add-zod-validation
    ↓
add-change-commands
    ↓
add-spec-commands
```

## 关键依赖关系

### 共享代码依赖
1. **模式**：所有模式在 add-zod-validation 中创建，被两个命令实现使用
2. **验证**：基础设施在 add-zod-validation 中创建，集成到两个命令中
3. **解析器**：Markdown 解析工具在 add-zod-validation 中创建，被两个命令使用

### 文件依赖
- `src/core/schemas/*.schema.ts`（由 add-zod-validation 创建）→ 被两个命令导入
- `src/core/validation/validator.ts`（由 add-zod-validation 创建）→ 被两个命令使用
- `src/core/parsers/markdown-parser.ts`（由 add-zod-validation 创建）→ 被两个命令使用

## 实现说明

### 对于开发者
1. 在进入下一阶段之前，完全完成每个阶段
2. 每个阶段后运行测试以确保稳定性
3. 旧的 `list` 命令在整个过程中保持功能正常

### 对于 CI/CD
1. 每个变更可以独立验证
2. 集成测试应在每个阶段后运行
3. 阶段 3 后需要完整的系统测试

### 并行工作机会
在每个阶段内，以下工作可以并行进行：
- **阶段 1**：模式设计、验证规则和解析器实现
- **阶段 2**：变更命令特性和旧版兼容性工作
- **阶段 3**：规范命令特性和最终集成
