# 任务：统一变更状态模型

## 阶段 1：修复制品 workflow 发现

- [x] 更新 `artifact-workflow.ts` 中的 `validateChangeExists()`，改为检查目录是否存在而非使用 `getActiveChangeIds()`
- [x] 更新错误消息以列出所有变更目录（不仅限于包含 proposal.md 的目录）
- [x] 为 `openspec status --change <scaffolded-change>` 添加测试
- [x] 为 `openspec next --change <scaffolded-change>` 添加测试
- [x] 为 `openspec instructions proposal --change <scaffolded-change>` 添加测试

## 阶段 2：修复 View 命令

- [x] 更新 `view.ts` 中的 `getChangesData()`，返回三个类别：草稿、活跃、已完成
- [x] 修复完成逻辑：`total === 0` → 草稿，而非已完成
- [x] 在仪表板渲染中添加"草稿变更"部分
- [x] 更新摘要以包含草稿计数
- [x] 为草稿变更在视图中正确显示添加测试

## 阶段 3：清理和验证

- [x] 清理测试变更（`test-workflow`、`test-workflow-2`）
- [x] 运行完整测试套件
- [x] 手动测试：`openspec new change foo && openspec status --change foo`
- [x] 手动测试：`openspec new change foo && openspec view` 显示 foo 在草稿中
- [x] 使用 `openspec validate unify-change-state-model --strict` 验证
