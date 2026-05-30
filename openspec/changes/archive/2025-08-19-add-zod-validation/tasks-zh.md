# 实现任务（基础阶段）

## 1. 核心 Schemas
- [x] 1.1 在 package.json 中添加 zod 依赖
- [x] 1.2 创建包含 ScenarioSchema 和 RequirementSchema 的 src/core/schemas/base.schema.ts
- [x] 1.3 创建包含 SpecSchema 的 src/core/schemas/spec.schema.ts
- [x] 1.4 创建包含 DeltaSchema 和 ChangeSchema 的 src/core/schemas/change.schema.ts
- [x] 1.5 创建 src/core/schemas/index.ts 导出所有 schemas

## 2. 解析器实现
- [x] 2.1 创建 src/core/parsers/markdown-parser.ts
- [x] 2.2 实现标题提取（##、###、####）
- [x] 2.3 实现标题之间的内容捕获
- [x] 2.4 为解析器边界情况添加测试

## 3. 验证基础设施
- [x] 3.1 创建包含 ValidationLevel、ValidationIssue、ValidationReport 类型的 src/core/validation/types.ts
- [x] 3.2 创建包含验证规则和阈值的 src/core/validation/constants.ts
- [x] 3.3 创建包含 SpecValidator 和 ChangeValidator 类的 src/core/validation/validator.ts

## 4. 增强验证规则
- [x] 4.1 添加 RequirementValidation 细化（必须有场景、必须包含 SHALL）
- [x] 4.2 添加 SpecValidation 细化（必须有需求）
- [x] 4.3 添加 ChangeValidation 细化（必须有差异、why 部分长度）
- [x] 4.4 为每个规则实现自定义错误消息

## 5. JSON 转换器
- [x] 5.1 创建 src/core/converters/json-converter.ts
- [x] 5.2 实现 spec 到 JSON 的转换
- [x] 5.3 实现变更到 JSON 的转换
- [x] 5.4 添加元数据字段（版本、格式、源路径）

## 6. Archive 命令增强
- [x] 6.1 使用新的验证器添加 archive 前验证检查
- [x] 6.2 添加带必需确认提示和警告消息的 --no-validate 标志："⚠️ WARNING: Skipping validation may archive invalid specs. Continue? (y/N)"
- [x] 6.3 在终止前显示验证错误
- [x] 6.4 将所有 --no-validate 用法记录到控制台，包含时间戳和受影响的文件
- [x] 6.5 为验证场景添加测试，包括 --no-validate 确认流程

## 7. Diff 命令增强
- [x] 7.1 在使用新验证器进行差异前添加验证检查
- [x] 7.2 显示验证警告（非阻塞）
- [x] 7.3 即使存在警告也继续执行差异

## 8. 测试
- [x] 8.1 所有 schemas 的单元测试
- [x] 8.2 解析器的单元测试
- [x] 8.3 验证规则的单元测试
- [x] 8.4 验证报告的集成测试
- [x] 8.5 测试各种无效的 spec/变更格式
- [x] 8.6 测试严格 schema 行为
- [x] 8.7 测试 archive 前验证
- [x] 8.8 测试验证报告 JSON 输出

## 9. 文档
- [x] 9.1 记录 schema 结构和验证规则（openspec/VALIDATION.md）
- [x] 9.2 更新 archive 的 CLI 帮助（记录 --no-validate 标志及其警告）
- [x] 9.3 更新 diff 的 CLI 帮助（记录验证警告行为）
- [x] 9.4 创建未来命令集成的迁移指南（openspec/MIGRATION.md）
