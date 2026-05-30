## 1. CLI 接线
- [x] 1.1 将 Kilo Code 添加到 `openspec init` 中可选 AI 工具列表，包括"已配置"检测和成功摘要。
- [x] 1.2 注册一个 `KiloCodeSlashCommandConfigurator`，与其他斜杠命令工具并列。

## 2. 工作流生成
- [x] 2.1 实现配置器，使其创建 `.kilocode/workflows/`（如果需要）并写入带有 OpenSpec 标记的 `openspec-{proposal,apply,archive}.md`。
- [x] 2.2 复用共享的斜杠命令主体，无需前置元数据；验证生成的文件保持纯 Markdown，无额外元数据。

## 3. 更新支持
- [x] 3.1 确保 `openspec update` 刷新现有的 Kilo Code 工作流，同时跳过不存在的那些。
- [x] 3.2 添加回归测试覆盖，确认标记内容在更新期间被替换（而非重复）。

## 4. 文档
- [x] 4.1 更新 README / 文档，注明 Kilo Code 工作流支持及路径（`.kilocode/workflows/`）。
- [x] 4.2 在 CHANGELOG 或发布说明中提及该集成（如适用）。
