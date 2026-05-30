# 实现任务

## 1. 更新 OpenCode 配置器
- [x] 1.1 在 OpenCode archive 前置元数据中添加 `$ARGUMENTS` 占位符（与 proposal schema 匹配）
- [x] 1.2 将其格式化为 `<ChangeId>\n $ARGUMENTS\n</ChangeId>` 或类似结构以保持清晰
- [x] 1.3 确保 `updateExisting` 重写 archive 前置元数据/主体，使 `$ARGUMENTS` 在 `openspec update` 后持续存在

## 2. 更新斜杠命令 template
- [x] 2.1 修改 archive 步骤，以在通过 `$ARGUMENTS` 提供时验证变更 ID 参数
- [x] 2.2 保持向后兼容性——如果未提供参数，允许从上下文中推断
- [x] 2.3 在 archive 前添加步骤，使用 `openspec list` 验证变更 ID 是否存在

## 3. 更新文档
- [x] 3.1 更新 AGENTS.md 中的 archive 示例以展示参数用法
- [x] 3.2 记录 OpenCode 现在支持 `/openspec:archive <change-id>`
