## 动机
当前的 `openspec init` 流程假定只选择一个助手，并且在 OpenSpec 结构已存在时停止。这使得入门体验显得僵化：团队无法在一次操作中配置多个工具，用户无法了解哪些文件被刷新，而且成功提示文案始终引用 Claude，即使涉及其他助手时也是如此。

## 变更内容
- 允许在 `openspec init` 过程中选择多个助手，包括在单次运行中刷新现有配置。
- 提供更丰富的入门提示文案，总结哪些工具文件被创建或刷新，并引导用户了解每个助手的后续步骤。
- 统一 AI 指令内容和规范，使 CLAUDE.md 和 AGENTS.md 共享相同的 OpenSpec 指南。
- 更新规范和测试，以覆盖多选提示、改进的摘要以及扩展模式协调。

## 影响范围
- 规范：`cli-init`
- 代码：`src/core/init.ts`、`src/core/config.ts`、`src/core/templates/*`、`src/core/configurators/*`
- 测试：`test/core/init.test.ts`、`test/core/update.test.ts`
