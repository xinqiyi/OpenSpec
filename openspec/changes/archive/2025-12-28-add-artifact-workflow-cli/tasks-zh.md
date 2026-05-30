## 1. 核心命令实现

- [x] 1.1 创建包含所有命令的 `src/commands/artifact-workflow.ts`
- [x] 1.2 使用文本输出实现 `status` 命令
- [x] 1.3 使用文本输出实现 `next` 命令
- [x] 1.4 使用文本输出实现 `instructions` 命令
- [x] 1.5 使用文本输出实现 `templates` 命令
- [x] 1.6 使用 createChange() 实现 `new change` 子命令

## 2. CLI 注册

- [x] 2.1 在 `src/cli/index.ts` 中注册 `status` 命令
- [x] 2.2 在 `src/cli/index.ts` 中注册 `next` 命令
- [x] 2.3 在 `src/cli/index.ts` 中注册 `instructions` 命令
- [x] 2.4 在 `src/cli/index.ts` 中注册 `templates` 命令
- [x] 2.5 注册包含 `change` 子命令的 `new` 命令组

## 3. 输出格式化

- [x] 3.1 为所有命令添加 `--json` 标志支持
- [x] 3.2 添加颜色编码的状态指示器（done/ready/blocked）
- [x] 3.3 为加载操作添加进度旋转器
- [x] 3.4 支持 `--no-color` 标志

## 4. 错误处理

- [x] 4.1 处理缺失的 `--change` 参数并显示有帮助的错误
- [x] 4.2 处理未知的变更名称并显示可用变更列表
- [x] 4.3 处理未知的 artifact 名称并显示有效选项
- [x] 4.4 处理 schema 解析错误

## 5. 选项和标志

- [x] 5.1 添加 `--schema` 选项用于自定义 schema 选择
- [x] 5.2 为 `new change` 命令添加 `--description` 选项
- [x] 5.3 确保选项遵循现有的 CLI schema

## 6. 测试

- [x] 6.1 为每个命令添加冒烟测试
- [x] 6.2 测试错误情况（缺失变更、未知 artifact）
- [x] 6.3 测试 JSON 输出格式
- [x] 6.4 使用不同的 schema 进行测试

## 7. 文档

- [x] 7.1 为所有命令添加标记为"实验性"的帮助文本
- [ ] 7.2 使用新命令更新 AGENTS.md（archive 后）
