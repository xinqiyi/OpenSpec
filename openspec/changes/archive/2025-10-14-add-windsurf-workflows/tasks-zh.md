## 1. CLI 接线
- [x] 1.1 将 Windsurf 添加到 `openspec init` 中可选 AI 工具列表，包括"已配置"检测。
- [x] 1.2 注册一个 `WindsurfSlashCommandConfigurator`，将 workflow 写入 `.windsurf/workflows/`，并确保目录存在。
- [x] 1.3 确保 `openspec update` 在选择 Windsurf 时拉取 Windsurf 配置器，并在文件不存在时跳过创建。

## 2. workflow template
- [x] 2.1 复用共享的 proposal/apply/archive 主体，在 OpenSpec 标记之前添加 Windsurf 特定的标题/描述。
- [x] 2.2 确认生成的 Markdown（每个文件）远低于 Windsurf 文档中注明的 12k 字符上限。

## 3. 测试与保障
- [x] 3.1 扩展 init 测试，断言选择 Windsurf 时创建 `.windsurf/workflows/openspec-*.md`。
- [x] 3.2 扩展 update 测试，断言现有的 Windsurf workflow 被刷新，不存在的文件被忽略。
- [x] 3.3 添加 Windsurf workflow 文件中标记保留的回归覆盖。

## 4. 文档
- [x] 4.1 更新 README（及任何面向用户的文档），在原生斜杠/workflow 集成下列出 Windsurf。
- [x] 4.2 在发布说明或 CHANGELOG 中提及 Windsurf workflow 支持（如适用）。
