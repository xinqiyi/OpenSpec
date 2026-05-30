## 1. 实现

- [x] 1.1 在 `shared.ts` 中提取 `getAvailableChanges`，并在 `statusCommand` 中使用它来在调用 `validateChangeExists` 之前检查是否有变更
- [x] 1.2 在文本模式下：打印 `没有活跃变更。使用以下命令创建一个：openspec new change <name>` 并返回（退出码 0）
- [x] 1.3 在 JSON 模式下：输出 `{"changes":[],"message":"没有活跃变更。"}` 并返回（退出码 0）

## 2. 测试

- [x] 2.1 添加测试：`openspec status` 无变更时以友好消息优雅退出（文本模式）
- [x] 2.2 添加测试：`openspec status --json` 无变更时返回包含空变更数组的有效 JSON
- [x] 2.3 验证现有行为：存在变更时 `openspec status` 不带 `--change` 仍会抛出缺少选项错误
- [x] 2.4 验证跨平台：测试使用 `path.join()` 进行任何路径断言

## 3. 发布

- [x] 3.1 添加描述此修复的 changeset
