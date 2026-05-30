## 1. 扩展 AIToolOption 接口

- [x] 1.1 在 `src/core/config.ts` 的 `AIToolOption` 接口中添加 `skillsDir?: string` 字段

## 2. 向 AI_TOOLS 添加 skillsDir

- [x] 2.1 为 Claude Code 工具条目添加 `skillsDir: '.claude'`
- [x] 2.2 为 Cursor 工具条目添加 `skillsDir: '.cursor'`
- [x] 2.3 为 Windsurf 工具条目添加 `skillsDir: '.windsurf'`
- [x] 2.4 为其他支持 Agent Skills spec 的已知工具添加 skillsDir（codex、opencode、roocode、kilocode、gemini、factory、github-copilot）

## 3. 创建命令生成类型

- [x] 3.1 使用 `CommandContent` 接口创建 `src/core/command-generation/types.ts`
- [x] 3.2 在 types.ts 中添加 `ToolCommandAdapter` 接口
- [x] 3.3 从模块索引导出类型

## 4. 实现工具命令适配器

- [x] 4.1 使用 Claude frontmatter 格式创建 `src/core/command-generation/adapters/claude.ts`
- [x] 4.2 使用 Cursor frontmatter 格式创建 `src/core/command-generation/adapters/cursor.ts`
- [x] 4.3 使用 Windsurf frontmatter 格式创建 `src/core/command-generation/adapters/windsurf.ts`
- [x] 4.4 创建基础适配器或工具，用于共享的 YAML 格式化逻辑（如适用）

## 5. 创建命令适配器注册表

- [x] 5.1 使用 `CommandAdapterRegistry` 类创建 `src/core/command-generation/registry.ts`
- [x] 5.2 在静态初始化器中注册 Claude、Cursor、Windsurf 适配器
- [x] 5.3 添加 `get(toolId)` 和 `getAll()` 方法

## 6. 创建命令生成器

- [x] 6.1 使用 `generateCommand()` 函数创建 `src/core/command-generation/generator.ts`
- [x] 6.2 添加 `generateCommands()` 函数用于批量生成
- [x] 6.3 创建导出公共 API 的模块索引 `src/core/command-generation/index.ts`

## 7. 更新 artifact-experimental-setup 命令

- [x] 7.1 在 `src/commands/artifact-workflow.ts` 的命令中添加 `--tool <tool-id>` 选项（必需）
- [x] 7.2 添加验证：`--tool` 标志是必需的（如果缺少则报错，显示有效工具列表）
- [x] 7.3 添加验证：工具存在于 AI_TOOLS 中
- [x] 7.4 添加验证：工具已配置 skillsDir
- [x] 7.5 用 `tool.skillsDir` 替换硬编码的 `.claude` skill 路径
- [x] 7.6 用 `CommandAdapterRegistry.get()` + `generateCommands()` 替换硬编码的命令生成
- [x] 7.7 优雅处理缺少适配器的情况（跳过命令并显示消息）
- [x] 7.8 更新输出消息以显示目标工具名称和路径

## 8. 测试

- [x] 8.1 为 `CommandContent` 和 `ToolCommandAdapter` 契约添加单元测试
- [x] 8.2 为 Claude 适配器添加单元测试（路径 + frontmatter 格式）
- [x] 8.3 为 Cursor 适配器添加单元测试（路径 + frontmatter 格式）
- [x] 8.4 为 `CommandAdapterRegistry.get()` 和缺少适配器的情况添加单元测试
- [x] 8.5 为 `--tool` 标志验证添加集成测试
- [x] 8.6 验证跨平台路径处理使用 `path.join()`
