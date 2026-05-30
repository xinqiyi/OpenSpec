## 1. 核心配置系统

- [x] 1.1 使用 Zod 创建 `src/core/project-config.ts` 及 `ProjectConfigSchema`（用于文档和类型推断）
- [x] 1.2 实现 `readProjectConfig()`，使用 Zod 的 `safeParse()` 进行弹性的逐字段解析
- [x] 1.3 支持 .yaml 和 .yml 两种扩展名（优先使用 .yaml）
- [x] 1.4 添加上下文字段 50KB 硬限制，包含大小检查和警告
- [x] 1.5 实现 `validateConfigRules()`，验证 artifact ID 是否与 schema 匹配（在指令加载时调用）
- [x] 1.6 实现 `suggestSchemas()`，使用 Levenshtein 距离模糊匹配提供友好的错误消息
- [x] 1.7 为弹性解析添加单元测试（部分配置、字段级错误与 Zod safeParse）
- [x] 1.8 添加上下文大小限制强制执行的单元测试
- [x] 1.9 添加 .yml/.yaml 优先级的单元测试
- [x] 1.10 添加带拼写错误的模糊 schema 匹配的单元测试

## 2. schema 解析集成

- [x] 2.1 更新 `src/utils/change-metadata.ts` 中的 `resolveSchemaForChange()`，检查项目配置（优先级第三）
- [x] 2.2 更新 `src/utils/change-utils.ts` 中的 `createNewChange()`，使用配置 schema 作为默认值
- [x] 2.3 为 schema 解析优先级添加集成测试（CLI → change 元数据 → 配置 → 默认值）
- [x] 2.4 添加配置中项目本地 schema 名称的测试
- [x] 2.5 添加不存在的 schema 错误处理及建议的测试

## 3. 上下文和规则注入

- [x] 3.1 更新 `src/core/artifact-graph/instruction-loader.ts` 中的 `loadInstructions()`，为所有 artifact 注入上下文
- [x] 3.2 添加仅对匹配 artifact 使用 XML 标签和项目符号格式的规则注入逻辑
- [x] 3.3 在指令加载期间添加验证调用，检查规则中的 artifact ID
- [x] 3.4 实现会话级警告缓存，避免重复显示相同的验证警告
- [x] 3.5 实现正确的排序：`<context>` → `<rules>` → `<template>`
- [x] 3.6 保留多行字符串和特殊字符，不进行转义
- [x] 3.7 添加上下文注入的单元测试（存在、不存在、多行、特殊字符）
- [x] 3.8 添加规则注入的单元测试（匹配 artifact、不匹配、空数组、多个 artifact）
- [x] 3.9 添加验证时机的单元测试（指令加载时警告，非配置加载时）
- [x] 3.10 添加警告去重的单元测试（相同警告每会话只显示一次）
- [x] 3.11 添加集成测试，验证包含上下文 + 规则 + template 的完整指令输出

## 4. 交互式配置创建

- [x] 4.1 在 package.json 中添加 @inquirer/prompts 依赖
- [x] 4.2 创建 `src/core/config-prompts.ts`，包含 ConfigPromptResult 接口
- [x] 4.3 实现 `promptForConfig()` 函数，包含 schema 选择提示
- [x] 4.4 添加多行上下文输入提示，包含示例和跳过选项
- [x] 4.5 添加每个 artifact 的规则提示，包含复选框选择和逐行输入
- [x] 4.6 实现 YAML 序列化，包含正确的多行字符串格式
- [x] 4.7 为提示错误添加验证和重试逻辑

## 5. 实验性设置集成

- [x] 5.1 更新 `src/commands/artifact-workflow.ts` 中的 `artifactExperimentalSetupCommand()`，检查现有配置
- [x] 5.2 在 skill/命令创建之后添加配置创建部分，包含标题和描述
- [x] 5.3 集成 `promptForConfig()` 调用，包含正确的流程控制
- [x] 5.4 添加 Ctrl+C（ExitPromptError）处理——记录取消消息，继续执行设置（非致命）
- [x] 5.5 使用 YAML stringify 将创建的配置写入 `openspec/config.yaml`
- [x] 5.6 显示成功摘要，包含路径、schema、上下文行数、规则数量
- [x] 5.7 显示使用示例和 git 提交建议
- [x] 5.8 处理配置已存在的情况，显示跳过消息和手动更新说明
- [x] 5.9 为文件写入失败添加错误处理，包含回退建议
- [x] 5.10 添加取消行为的测试（skill/命令保留，配置未创建）

## 6. 测试和文档

- [x] 6.1 添加端到端测试：运行实验性设置 → 创建配置 → 创建 change → 验证使用的 schema
- [x] 6.2 添加端到端测试：创建配置 → 获取指令 → 验证上下文和规则已注入
- [x] 6.3 测试向后兼容性：现有 change 在没有配置的情况下正常工作
- [x] 6.4 测试配置变更立即生效（无过期缓存）
- [x] 6.5 添加性能基准测试：测量典型配置（1KB 上下文）的配置读取时间
- [x] 6.6 添加性能基准测试：测量大型配置（50KB 上下文）的配置读取时间
- [x] 6.7 添加性能基准测试：测量单条命令内的重复读取
- [x] 6.8 记录基准测试结果并决定是否需要缓存（目标：典型 <10ms，可接受 <50ms）
- [x] 6.9 如果基准测试不达标：实现基于 mtime 的缓存，支持缓存失效
- [x] 6.10 使用配置功能示例和 schema 更新 README 或文档
- [x] 6.11 记录不同 schema 的常见 artifact ID
- [x] 6.12 为配置验证错误添加故障排除部分
