## 为什么
Google 正在推出 Antigravity，这是一个源自 Windsurf 的 IDE，可从 `.agent/workflows/*.md` 中发现工作流。目前 OpenSpec 只能为 Windsurf 目录搭建斜杠命令，因此 Antigravity 用户无法从 IDE 中运行提案/应用/归档流程。

## 变更内容
- 在 `openspec init` 中添加 Antigravity 作为可选的原生工具，使其创建 `.agent/workflows/openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`，带有仅包含 `description` 字段的 YAML 前置元数据以及标准的 OpenSpec 托管主体。
- 确保 `openspec update` 刷新 `.agent/workflows/` 中任何现有 Antigravity 工作流的主体，而不创建缺失的文件，与 Windsurf 行为保持一致。
- 共享 e2e/模板测试覆盖，确认生成器写入正确的目录、文件名大小写和前置元数据格式，以便 Antigravity 能够识别这些工作流。

## 影响范围
- 受影响的规范：`specs/cli-init`、`specs/cli-update`
- 预期代码：CLI init/update 工具注册表、斜杠命令模板、相关测试
