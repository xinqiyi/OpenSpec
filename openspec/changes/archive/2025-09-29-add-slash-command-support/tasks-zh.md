# 实施任务

## 1. template 和配置器
- [x] 1.1 为 proposal、应用和 archive 命令创建共享 template，包含来自 `openspec/README.md` 的每个 workflow 阶段说明。
- [x] 1.2 实现 `SlashCommandConfigurator` 基础类和针对 Claude Code 和 Cursor 的特定工具配置器。

## 2. Claude Code 集成
- [x] 2.1 在 `openspec init` 期间使用共享 template 生成 `.claude/commands/openspec/{proposal,apply,archive}.md`。
- [x] 2.2 在 `openspec update` 期间更新现有的 `.claude/commands/openspec/*` 文件。

## 3. Cursor 集成
- [x] 3.1 在 `openspec init` 期间使用共享 template 生成 `.cursor/commands/{openspec-proposal,openspec-apply,openspec-archive}.md`。
- [x] 3.2 在 `openspec update` 期间更新现有的 `.cursor/commands/*` 文件。

## 4. 验证
- [x] 4.1 添加测试验证斜杠命令文件被正确创建和更新。

## 5. OpenCode 集成
- [x] 5.1 在 `openspec init` 期间使用共享 template 生成 `.opencode/commands/{openspec-proposal,openspec-apply,openspec-archive}.md`。
- [x] 5.2 在 `openspec update` 期间更新现有的 `.opencode/commands/*` 文件。
