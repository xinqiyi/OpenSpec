## 实现任务

- [x] 创建 `src/core/configurators/slash/github-copilot.ts`，实现 `SlashCommandConfigurator` 基类
  - 实现 `getRelativePath()` 返回 `.github/prompts/openspec-{proposal,apply,archive}.prompt.md`
  - 实现 `getFrontmatter()` 生成带有 `description` 字段的 YAML frontmatter，并包含 `$ARGUMENTS` 占位符
  - 实现 `generateAll()` 创建 `.github/prompts/` 目录并写入三个提示文件，包含 frontmatter、标记和共享模板主体
  - 实现 `updateExisting()` 仅刷新标记之间的管理块，同时保留 frontmatter
  - 设置 `toolId = "github-copilot"` 和 `isAvailable = true`

- [x] 在 `src/core/configurators/slash/registry.ts` 中注册 GitHub Copilot 配置器
  - 导入 `GitHubCopilotSlashCommandConfigurator`
  - 添加到 `SLASH_COMMAND_CONFIGURATORS` 数组
  - 更新工具选择器显示名称为"GitHub Copilot"

- [x] 更新 `src/core/init.ts` 以在 AI 工具选择提示中包含 GitHub Copilot
  - 将 GitHub Copilot 添加到可用工具列表，并检测现有的 `.github/prompts/openspec-*.prompt.md` 文件
  - 当提示文件存在时显示"（已配置）"

- [x] 更新 `src/core/update.ts` 以在存在时刷新 GitHub Copilot 提示
  - 当 `.github/prompts/` 包含 OpenSpec 提示文件时，调用 GitHub Copilot 配置器的 `updateExisting()`

- [x] 为 GitHub Copilot 斜杠命令生成添加集成测试
  - 测试 `generateAll()` 创建三个具有正确结构（frontmatter + 标记 + 主体）的提示文件
  - 测试 `updateExisting()` 保留 frontmatter 并仅更新管理块
  - 测试更新期间不创建缺失的提示文件

- [x] 更新文档
  - 在 README 的斜杠命令支持表中添加 GitHub Copilot
  - 记录 `.github/prompts/` 作为发现位置
  - 为 GitHub Copilot 支持添加 CHANGELOG 条目
