## 为什么
OpenSpec 目前仅在团队在 `openspec init` 期间明确选择"AGENTS.md 标准"工具时才会创建根级 `AGENTS.md` 存根。跳过该复选框的项目永远不会获得托管存根，因此非原生助手（Copilot、Codeium 等）没有入口点，而后续的 `openspec update` 运行会在没有任何上下文的情况下静默创建该文件。我们需要将存根内置到初始化中，明确工具选择体验，并使更新 workflow 保持一致，以便每个团队成员从第一天起就能找到正确的指令。

## 变更内容
- 更新 `openspec init`，使根级 `AGENTS.md` 存根始终生成（首次运行和扩展 schema），并通过共享工具函数刷新，而不是与工具选择绑定。
- 重新设计 AI 工具选择向导，将选项分为"原生支持"（Claude、Cursor、OpenCode 等）和一个信息性的"其他工具"部分，解释始终开启的 `AGENTS.md` 交办说明。
- 调整 CLI spec、提示和成功消息以反映新的分类，同时保持扩展 schema 行为一致。
- 更新自动化测试和测试夹具以覆盖无条件的存根创建和重新设计的提示流程。
- 刷新文档和上手片段，使其不再将存根描述为可选项，而是指出新的分组方式。
- 确保 `openspec update` 继续协调 `openspec/AGENTS.md` 和根级存根，记录预期行为以便不匹配的配置能够自我修复。

## 影响范围
- 受影响的 spec：`cli-init`、`cli-update`
- 受影响的代码：`src/core/init.ts`、`src/core/config.ts`、`src/core/configurators/agents.ts`、`src/core/templates/agents-root-stub.ts`、`src/core/update.ts`、`test/core/` 下的相关测试
- 文档与资源：README、CHANGELOG、以及任何引用选择"AGENTS.md 标准"选项的设置指南
