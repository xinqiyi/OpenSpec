## 为什么
- GitHub Copilot 通过 `.github/prompts/<name>.prompt.md` 中的 Markdown 文件支持自定义斜杠命令。每个文件包含带有 `description` 标签的 YAML frontmatter，并使用 `$ARGUMENTS` 捕获用户输入。这种格式允许团队直接在 Copilot 的聊天界面中暴露策划的工作流。
- 团队已经依赖 OpenSpec 来管理 Claude Code、Cursor、OpenCode、Codex、Kilo Code 和 Windsurf 的斜杠命令配置。排除 GitHub Copilot 迫使开发者在 `.github/prompts/` 中手动维护 OpenSpec 提示，这会导致偏差并削弱 OpenSpec 的"单一事实源头"承诺。
- GitHub Copilot 从仓库的 `.github/prompts/` 目录发现提示，使其可以直接进行版本控制并在团队中共享。通过 `openspec init` 和 `openspec update` 添加自动生成和刷新功能，消除了手动同步，并使 OpenSpec 指令在所有 AI 助手中保持一致。

## 变更内容
- 在 `openspec init` 工具选择器中添加 GitHub Copilot，并带有类似其他编辑器的"已配置"检测，连接一个实现，将管理的 Markdown 提示文件写入 `.github/prompts/`，包含 OpenSpec 标记块。
- 生成三个 GitHub Copilot 提示文件——`openspec-proposal.prompt.md`、`openspec-apply.prompt.md` 和 `openspec-archive.prompt.md`——其内容镜像共享的斜杠命令模板，同时符合 Copilot 的 frontmatter 和 `$ARGUMENTS` 占位符约定。
- 记录 GitHub Copilot 基于仓库的发现方式，以及 OpenSpec 将提示写入 `.github/prompts/` 并带有管理块。
- 教导 `openspec update` 在原地刷新现有的 GitHub Copilot 提示（仅在它们已存在时），位于仓库的 `.github/prompts/` 目录中。
- 将 GitHub Copilot 支持与其他斜杠命令集成一起记录，并为 `.github/prompts/` 文件的 init/update 行为添加测试覆盖。

## 影响
- 规范：`cli-init`、`cli-update`
- 代码：`src/core/configurators/slash/github-copilot.ts`（新建）、`src/core/configurators/slash/registry.ts`、`src/core/templates/slash-command-templates.ts`、CLI 工具摘要、文档
- 测试：GitHub Copilot 提示搭建和刷新逻辑的集成覆盖
- 文档：README 和 CHANGELOG 条目宣布 GitHub Copilot 斜杠命令支持

## 当前规范参考
- `specs/cli-init/spec.md`
  - 需求涵盖 init UX、目录搭建、AI 工具配置以及 Claude Code、Cursor、OpenCode、Codex、Kilo Code 和 Windsurf 的现有斜杠命令支持。
  - 我们在 `changes/.../specs/cli-init/spec.md` 中的 `## MODIFIED` 增量将在附加新的 GitHub Copilot 场景之前复制完整的"斜杠命令配置"需求（标题、描述和所有场景），以便归档保留每个先前的场景。
- `specs/cli-update/spec.md`
  - 需求定义更新前提条件、模板刷新行为以及现有工具的斜杠命令刷新逻辑。
  - 相应的增量保留整个"斜杠命令更新"需求，同时添加 GitHub Copilot 刷新场景，确保归档工作流替换该块而不丢失现有场景或"缺少斜杠命令文件"的保护措施。
