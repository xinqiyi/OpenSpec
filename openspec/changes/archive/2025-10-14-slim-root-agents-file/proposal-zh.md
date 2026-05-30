## 为什么
项目根目录当前会收到 OpenSpec agent 指令的完整副本，与 `openspec/AGENTS.md` 中的内容重复。当团队修改了一处而未修改另一处时，文件就会发生漂移，导致新手上手的助手看到相互矛盾的指南。

## 变更内容
- 在 `openspec init` 和后续更新期间，继续在 `openspec/AGENTS.md` 中生成完整 template。
- 将根级文件（`AGENTS.md` 或 `CLAUDE.md`，取决于工具选择）替换为简短的交办说明，解释该项目使用了 OpenSpec 并直接指向 `openspec/AGENTS.md`。
- 添加专用的存根 template，使 init 和 update 流程都能复用相同的最小副本指令。
- 更新 CLI 测试和文档以反映新的根级消息，并确保 OpenSpec 标记块仍能保护未来的更新。

## 影响范围
- 受影响的 spec：`cli-init`、`cli-update`
- 受影响的代码：`src/core/init.ts`、`src/core/update.ts`、`src/core/templates/agents-template.ts`
- 更新提及根目录 `AGENTS.md` 内容的资源文件和自述文件，以引用新的存根消息。
