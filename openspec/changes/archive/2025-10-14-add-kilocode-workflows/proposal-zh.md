## 动机
- Kilo Code 通过从 `.kilocode/workflows/`（或全局 `~/.kilocode/workflows/`）加载 Markdown workflow 来执行"斜杠命令"，当用户输入 `/workflow-name.md` 时运行这些 workflow，使得项目本地 workflow 文件相当于我们已为其他工具提供的斜杠命令文件。
 ([workflow | Kilo Code 文档](https://kilocode.ai/docs/features/slash-commands/workflows))
- 这些 workflow 是纯 Markdown 格式，包含逐步说明，可以调用内置工具和 MCP 集成，因此复用 OpenSpec 共享的 proposal/apply/archive 主体可以在各助手之间保持行为一致，而无需创建新内容。
- OpenSpec 已能检测已配置的工具并在 `init`/`update` 过程中刷新标记包裹的文件；将相同机制扩展到 `.kilocode/workflows/openspec-*.md` 可确保 Kilo Code 与单一事实来源保持同步。

## 变更内容
- 将 Kilo Code 添加到 `openspec init` 工具选择器中，支持"已配置"检测，包括扩展 schema 的连接，以便团队可以刷新 Kilo Code 资源。
- 实现一个 `KiloCodeSlashCommandConfigurator`，创建 `.kilocode/workflows/openspec-{proposal,apply,archive}.md`，确保 workflow 目录存在，并将共享内容包裹在 OpenSpec 标记中（无需前置元数据）。
- 教会 `openspec update` 使用共享的斜杠命令 template 刷新现有的 Kilo Code workflow（仅刷新已存在的那些）。
- 更新文档、发布说明和集成测试，使新的 workflow 支持与 Claude、Cursor、OpenCode 和 Windsurf 一同覆盖。

## 影响范围
- spec：`cli-init`、`cli-update`
- 代码：`src/core/config.ts`、`src/core/configurators/(registry|slash/*)`、`src/core/templates/slash-command-templates.ts`、CLI 工具摘要的接线
- 测试：init/update workflow 覆盖、`.kilocode/workflows/` 中标记保留的回归测试
- 文档：README / CHANGELOG 更新，宣传 Kilo Code workflow 支持
