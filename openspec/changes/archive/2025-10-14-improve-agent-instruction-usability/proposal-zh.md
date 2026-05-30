## 动机
代理在提案格式化方面容易出错，因为基本的 Markdown 模板和格式化规则埋在文档中间。重新组织 `openspec/AGENTS.md`，加入显眼的快速参考和嵌入式示例，将帮助助手无需猜测即可遵循流程。

## 变更内容
- 重构 `openspec/AGENTS.md`，使文件格式和脚手架模板出现在工作流正文之前的顶层快速参考部分。
- 在工作流步骤中嵌入 `proposal.md`、`tasks.md`、`design.md` 和 spec 增量的复制/粘贴模板，以及内联示例。
- 添加预验证检查清单，在运行 `openspec validate` 之前突出最常见的格式陷阱。
- 将内容分为初级和高级部分，逐步揭示复杂度，同时保持高级指导的可访问性。

## 影响范围
- 受影响的规范：`specs/docs-agent-instructions`
- 受影响的代码：`openspec/AGENTS.md`、`docs/`
