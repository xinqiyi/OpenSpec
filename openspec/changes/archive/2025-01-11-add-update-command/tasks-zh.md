# 实施任务

## 1. 更新命令实现
- [x] 1.1 创建包含 `UpdateCommand` 类的 `src/core/update.ts`
- [x] 1.2 检查 `openspec` 目录是否存在（使用 `FileSystemUtils.directoryExists`）
- [x] 1.3 使用 `FileSystemUtils.writeFile` 将 `readmeTemplate` 写入 `openspec/README.md`
- [x] 1.4 通过 `FileSystemUtils.updateFileWithMarkers` 和 `TemplateManager.getClaudeTemplate()` 使用标记更新 `CLAUDE.md`
- [x] 1.5 显示 ASCII 安全成功消息：`已更新 OpenSpec 指令`

## 2. CLI 集成
- [x] 2.1 在 `src/cli/index.ts` 中注册 `update` 命令
- [x] 2.2 添加命令描述：`更新 OpenSpec 指令文件`
- [x] 2.3 使用 `ora().fail(...)` 和退出码 1 处理错误（缺失 `openspec` 目录、文件写入错误）

## 3. 测试
- [x] 3.1 验证 `openspec/README.md` 完全替换为最新 template
- [x] 3.2 验证 `CLAUDE.md` 的 OpenSpec 块更新而不更改标记外的用户内容
- [x] 3.3 验证幂等性（运行两次产生相同的文件，无重复标记）
- [x] 3.4 验证 `openspec` 目录缺失时的错误，附带友好消息
- [x] 3.5 验证成功消息在纯 ASCII 终端中正确显示
