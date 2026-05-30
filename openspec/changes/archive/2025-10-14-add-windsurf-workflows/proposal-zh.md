## 动机
- Windsurf 将"workflow"作为类似斜杠命令自动化的载体：保存在 `.windsurf/workflows/` 下的 Markdown 文件，Cascade 会在整个 workspace 中（包括子目录并向上到 git 根目录）发现它们，然后在用户输入 `/workflow-name` 时执行。这些文件可以由团队编写，必须保持在 12000 字符以下，并且可以调用其他 workflow，使其成为向 Windsurf 用户发布 OpenSpec 指导的自然位置。
 ([Windsurf workflow 文档](https://docs.windsurf.com/windsurf/cascade/workflows))
- Wave 12 变更日志重申 workflow 通过斜杠命令调用，且 Windsurf 将其存储在 `.windsurf/workflows` 中，因此 OpenSpec CLI 只需在此处生成 Markdown 即可参与 Windsurf 的命令面板。
 ("自定义 workflow"部分，[Windsurf 变更日志](https://windsurf.com/changelog))
- OpenSpec 已经为 proposal/apply/archive 提供了共享的命令主体，并使用标记保持命令更新。将相同的 template 扩展到 Windsurf 可使行为与 Claude、Cursor 和 OpenCode 保持一致，而无需创建新的内容流程。

## 变更内容
- 将 Windsurf 添加到 CLI 工具选择器（`openspec init`）和斜杠命令注册表中，选择后即可搭建 `.windsurf/workflows/openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`，并带有标记管理的主体。
- 为每个 Windsurf workflow 设置简短标题/描述，加上包裹在标记中的现有 OpenSpec 护栏/步骤，确保总内容远低于 12000 字符限制。
- 确保 `openspec update` 就地刷新现有的 Windsurf workflow（仅刷新已存在的那些），反映当前对其他编辑器的行为。
- 扩展 init/update 的单元测试以覆盖 Windsurf 的生成和更新，并更新 README/工具文档以宣传 Windsurf 支持。

## 影响范围
- spec：`cli-init`、`cli-update`
- 代码：`src/core/configurators/slash/*`、`src/core/templates/slash-command-templates.ts`、CLI 提示、README
- 测试：针对 Windsurf workflow 的 init/update 集成测试覆盖
