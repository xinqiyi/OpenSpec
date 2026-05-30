## 为什么
- Codex（原名 Codeium Chat 的 VS Code 扩展）通过从 `~/.codex/prompts/` 读取 Markdown 提示文件来公开"斜杠命令"。每个文件名成为用户可以运行的 `/command`，带有 YAML frontmatter（`description`、`argument-hint`）和 `$ARGUMENTS` 来捕获用户输入。Kevin Kern 分享的工作流截图（"Codex 问题分析器"）显示 OpenSpec 应该针对的格式，以便团队可以直接从聊天面板调用精心策划的工作流。
- 团队已经依赖 OpenSpec 来管理 Claude、Cursor、OpenCode、Kilo Code 和 Windsurf 的斜杠命令表面积。排除 Codex 迫使他们手动将 OpenSpec 护栏复制粘贴到 `~/.codex/prompts/*.md`，这很快会漂移，并破坏了 CLI 的"单一事实来源"承诺。
- Codex 命令位于仓库外部（在用户的主目录下），因此提供一个自动配置器来搭建提示并通过 `openspec update` 保持刷新，消除了容易出错的手动步骤，并使 OpenSpec 指令在多个助手间保持同步。

## 变更内容
- 将 Codex 添加到 `openspec init` 工具选择器，使用与其他编辑器相同的"已配置"检测，连接一个实现，直接将受管 Markdown 提示写入 Codex 的全局目录（`~/.codex/prompts` 或 `$CODEX_HOME/prompts`），带有 OpenSpec 标记块。
- 生成三个 Codex 提示文件 — `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` — 其内容镜像共享斜杠命令模板，同时使用 YAML frontmatter（`description` 和 `argument-hint` 字段）和 `$ARGUMENTS` 将所有参数捕获为单个字符串（匹配 GitHub Copilot 模式和官方 Codex 规范）。
- 记录 Codex 的仅全局发现以及 OpenSpec 将提示直接写入 `~/.codex/prompts`（或 `$CODEX_HOME/prompts`）。
- 让 `openspec update` 在全局目录中原位刷新现有的 Codex 提示（且仅当它们已存在时），同时更新 frontmatter 和正文。
- 与其他斜杠命令集成一起记录 Codex 支持，并通过 `CODEX_HOME` 针对临时全局提示目录添加回归覆盖，以执行 init/update 行为。

## 影响
- 规范：`cli-init`、`cli-update`
- 代码：`src/core/config.ts`、`src/core/configurators/slash/*`、`src/core/templates/slash-command-templates.ts`、CLI 工具总结、文档
- 测试：Codex 提示搭建和刷新逻辑的集成覆盖
- 文档：宣布 Codex 斜杠命令支持的 README 和 CHANGELOG 条目

## 当前规范参考
- `specs/cli-init/spec.md`
  - 需求涵盖 init UX、目录脚手架、AI 工具配置以及 Claude Code、Cursor 和 OpenCode 的现有斜杠命令支持。
  - 我们在 `changes/.../specs/cli-init/spec.md` 中的 `## 修改后的需求` 增量在附加新的 Codex 场景之前复制完整的"斜杠命令配置"需求（标题、描述和所有场景），以便归档将保留每个先前的场景。
- `specs/cli-update/spec.md`
  - 需求定义了更新前置条件、模板刷新行为以及 Claude Code、Cursor 和 OpenCode 的斜杠命令刷新逻辑。
  - 相应的增量在添加 Codex 刷新场景的同时保留完整的"斜杠命令更新"需求，确保归档工作流在不丢失现有场景或"缺少斜杠命令文件"护栏的情况下替换该块。
