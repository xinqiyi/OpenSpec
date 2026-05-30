## 为什么

用户和 agent 需要一种简单的方式直接从 CLI 提交关于 OpenSpec 的反馈。目前没有机制来收集用户反馈、功能请求或错误报告，以便能够进行后续对话。使用 GitHub Issues 使我们能够跟踪反馈、通过 GitHub 认证防止垃圾信息，并能联系用户。

## 变更内容

- 添加 `openspec feedback <message>` CLI 命令
- 利用 `gh` CLI 进行 GitHub 认证和问题创建
- 添加 `/feedback` skill，用于带上下文增强的 agent 辅助反馈
- 确保跨平台兼容性（macOS、Linux、Windows）

## 影响

- 受影响的 spec：新增 `cli-feedback` 能力
- 受影响的代码：
 - `src/cli/index.ts` - 注册 feedback 命令
 - `src/commands/feedback.ts` - 使用 `gh` CLI 的命令实现
 - `src/core/templates/skill-templates.ts` - 反馈 skill template
 - `src/core/completions/command-registry.ts` - Shell 补全
- 外部依赖：需要安装并认证 `gh` CLI
