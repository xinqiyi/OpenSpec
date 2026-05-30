## 1. 设置和命令结构

- [x] 1.1 使用 `registerSchemaCommand(program: Command)` 函数创建 `src/commands/schema.ts`
- [x] 1.2 在 `src/cli/index.ts` 中注册 schema 命令（导入并调用 `registerSchemaCommand`）
- [x] 1.3 添加带有描述"管理 workflow 架构"的 schema 命令组

## 2. Schema Which 命令

- [x] 2.1 添加带有 `--json` 和 `--all` 选项的 `schema which <name>` 子命令
- [x] 2.2 使用项目根目录的 `getSchemaDir()` 实现解析查找
- [x] 2.3 通过检查所有三个位置（项目、用户、包）实现影子检测
- [x] 2.4 添加文本输出：显示来源、路径和影子信息
- [x] 2.5 添加 JSON 输出：`{ name, source, path, shadows: [] }`
- [x] 2.6 添加 `--all` schema 以列出所有架构及其解析来源

## 3. Schema Validate 命令

- [x] 3.1 添加带有 `--json` 和 `--verbose` 选项的 `schema validate [name]` 子命令
- [x] 3.2 使用 `schema.ts` 中现有的 `parseSchema()` 实现单个架构验证
- [x] 3.3 为每个 artifact 的 template 文件添加 template 存在性检查
- [x] 3.4 添加依赖图循环检测（重用拓扑排序逻辑）
- [x] 3.5 当未提供名称时添加验证所有 schema（扫描 `openspec/schemas/`）
- [x] 3.6 添加带有通过/失败指示器和错误消息的文本输出
- [x] 3.7 添加匹配现有 `openspec validate` 格式的 JSON 输出：`{ valid, issues: [] }`
- [x] 3.8 添加显示每个验证步骤的详细 schema

## 4. Schema Fork 命令

- [x] 4.1 添加带有 `--json` 和 `--force` 选项的 `schema fork <source> [name]` 子命令
- [x] 4.2 使用项目根目录的 `getSchemaDir()` 实现来源解析
- [x] 4.3 实现默认目标命名：`<source>-custom`
- [x] 4.4 实现带有递归文件复制的目录复制
- [x] 4.5 更新复制的 `schema.yaml` 中的 `name` 字段
- [x] 4.6 添加覆盖保护：检查目标是否存在，需要 `--force` 或确认
- [x] 4.7 添加带有来源/目标路径的文本输出
- [x] 4.8 添加 JSON 输出：`{ forked, source, destination, sourceLocation }`

## 5. Schema Init 命令

- [x] 5.1 添加带有 `--json`、`--description`、`--artifacts`、`--default`、`--no-default`、`--force` 选项的 `schema init <name>` 子命令
- [x] 5.2 实现架构名称验证（kebab-case，无空格）
- [x] 5.3 使用 `@inquirer/prompts` 实现描述的交互式提示
- [x] 5.4 实现带有描述的交互式 artifact 选择（多选）
- [x] 5.5 创建架构目录和带有所选配置的 `schema.yaml`
- [x] 5.6 为所选 artifact 创建默认 template 文件
- [x] 5.7 添加 `--default` 标志以将新架构更新为 `openspec/config.yaml` 中的默认架构
- [x] 5.8 添加覆盖保护：检查架构是否存在，需要 `--force`
- [x] 5.9 添加带有创建路径和后续步骤的文本输出
- [x] 5.10 添加 JSON 输出：`{ created, path, schema }`
- [x] 5.11 添加带有 `--description` 和 `--artifacts` 标志的非交互 schema

## 6. 测试

- [x] 6.1 在 `test/commands/schema.test.ts` 中为 `schema which` 命令添加单元测试
- [x] 6.2 为 `schema validate` 命令添加单元测试
- [x] 6.3 为 `schema fork` 命令添加单元测试
- [x] 6.4 为 `schema init` 命令添加单元测试
- [x] 6.5 使用 `@inquirer/prompts` 模拟测试交互 schema
- [x] 6.6 测试所有命令的 JSON 输出格式
- [x] 6.7 测试错误情况：无效名称、未找到、已存在、循环检测

## 7. 文档和优化

- [x] 7.1 为所有 schema 子命令添加 CLI 帮助文本
- [x] 7.2 更新 shell 补全以包含 schema 命令
- [x] 7.3 运行 lint 并修复任何问题（`npm run lint`）
- [x] 7.4 运行完整测试套件（`npm test`）
