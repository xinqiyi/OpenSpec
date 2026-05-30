# Init 命令的实现任务

## 1. 核心基础设施
- [x] 1.1 创建具有目录/文件创建工具的 src/utils/file-system.ts
- [x] 1.2 创建用于模板管理的 src/core/templates/index.ts
- [x] 1.3 创建包含主要初始化逻辑的 src/core/init.ts
- [x] 1.4 创建用于配置管理的 src/core/config.ts

## 2. 模板文件
- [x] 2.1 创建包含 OpenSpec README 内容的 src/core/templates/readme-template.ts
- [x] 2.2 创建包含可定制 project.md 的 src/core/templates/project-template.ts
- [x] 2.3 创建包含标记的 CLAUDE.md 内容的 src/core/templates/claude-template.ts

## 3. AI 工具配置器
- [x] 3.1 创建具有 ToolConfigurator 接口的 src/core/configurators/base.ts
- [x] 3.2 创建用于 Claude Code 配置的 src/core/configurators/claude.ts
- [x] 3.3 创建用于工具注册的 src/core/configurators/registry.ts
- [x] 3.4 实现基于标记的文件更新，用于现有配置

## 4. Init 命令实现
- [x] 4.1 使用 Commander 在 src/cli/index.ts 中添加 init 命令
- [x] 4.2 使用多选提示实现 AI 工具选择（Claude Code 可用，其他"即将推出"）——至少需要选择一个
- [x] 4.3 为现有 OpenSpec 目录添加带帮助性错误消息的验证
- [x] 4.4 实现目录结构创建
- [x] 4.5 使用模板和标记实现文件生成

## 5. 用户体验
- [x] 5.1 添加彩色控制台输出以改善用户体验
- [x] 5.2 实现进度指示器（步骤 1/3、2/3、3/3）
- [x] 5.3 添加带有可操作后续步骤的成功消息（编辑 project.md、创建第一个变更）
- [x] 5.4 添加带有帮助信息的错误处理

## 6. 测试和文档
- [x] 6.1 为文件系统工具添加单元测试
- [x] 6.2 为基于标记的文件更新添加单元测试
- [x] 6.3 为 init 命令添加集成测试
- [x] 6.4 使用正确的 bin 配置更新 package.json
- [x] 6.5 端到端测试构建后的 CLI 命令
