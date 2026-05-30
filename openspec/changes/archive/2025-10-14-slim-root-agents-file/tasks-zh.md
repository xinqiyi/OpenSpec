## 1. template
- [x] 1.1 添加一个共享的存根 template，用于渲染根级 agent 指令交办消息。
- [x] 1.2 确保存根同时覆盖 `AGENTS.md` 和 `CLAUDE.md` 两种变体。

## 2. 初始化流程
- [x] 2.1 更新 `createInitArtifacts`，使其向项目根目录写入存根而非完整指令。
- [x] 2.2 保留托管块标记，以便将来的更新可以安全地覆盖存根。

## 3. 更新流程
- [x] 3.1 使更新命令刷新根级存根而非完整指令。
- [x] 3.2 确认更新日志输出仍反映已更改的文件。

## 4. 测试与文档
- [x] 4.1 调整 CLI/init 测试以匹配新的根级内容。
- [x] 4.2 在 `openspec/specs/cli-init` 和 `openspec/specs/cli-update`（以及任何相关的 README 片段）中记录存根消息。
