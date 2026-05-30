## 前置条件

- [x] 0.1 先实现 `add-per-change-schema-metadata`（用于自动检测 schema）

## 1. Schema 格式

- [x] 1.1 在 `src/core/artifact-graph/types.ts` 中添加 `ApplyPhaseSchema` Zod schema
- [x] 1.2 更新 `SchemaYamlSchema` 以包含可选的 `apply` 字段
- [x] 1.3 导出 `ApplyPhase` 类型

## 2. 更新现有 Schema

- [x] 2.1 在 `schemas/spec-driven/schema.yaml` 中添加 `apply` 块
- [x] 2.2 在 `schemas/tdd/schema.yaml` 中添加 `apply` 块

## 3. 重构 generateApplyInstructions

- [x] 3.1 通过 `resolveSchema(schemaName)` 加载 schema
- [x] 3.2 读取 `apply.requires` 以确定必需的工件
- [x] 3.3 动态检查工件的存在性（而非硬编码路径）
- [x] 3.4 使用 `apply.tracks` 进行进度跟踪（如果为 null 则跳过）
- [x] 3.5 使用 `apply.instruction` 作为指令文本
- [x] 3.6 从 schema 中的所有现有工件构建 `contextFiles`

## 4. 处理回退

- [x] 4.1 如果 schema 没有 `apply` 块，要求所有工件都存在
- [x] 4.2 默认指令："所有工件已完成。请继续进行实现。"

## 5. 测试

- [x] 5.1 使用 spec-driven schema 测试 apply 指令
- [x] 5.2 使用 tdd schema 测试 apply 指令
- [x] 5.3 测试 schema 没有 apply 块时的回退
- [x] 5.4 测试缺少必需工件时的阻塞状态
