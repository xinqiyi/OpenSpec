## 1. 实现
- [x] 1.1 重构 `openspec init`，使其始终通过共享辅助逻辑生成根级 `AGENTS.md` 存根（首次运行和扩展 schema）。
- [x] 1.2 重新设计 AI 工具选择向导，展示"原生支持"与"其他工具"分组，并使存根成为非可选项。
- [x] 1.3 更新 CLI 消息、template 和配置器，使新流程在 init 和 update 命令之间保持同步。
- [x] 1.4 刷新单元/集成测试以覆盖无条件的存根创建和重新分组后的提示布局。
- [x] 1.5 更新提及可选 `AGENTS.md` 体验的文档、README 片段和 CHANGELOG 条目。

## 2. 验证
- [x] 2.1 运行针对 CLI init/update 套件的 `pnpm test`。
- [x] 2.2 执行 `openspec validate update-cli-init-root-agents --strict`。
- [x] 2.3 执行手动冒烟测试：在临时目录中运行 `openspec init`，确认存根和分组提示，然后在扩展 schema 下再次运行。
