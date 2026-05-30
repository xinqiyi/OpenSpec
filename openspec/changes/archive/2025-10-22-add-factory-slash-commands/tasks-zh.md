## 1. Factory 工具注册
- [x] 1.1 将 Factory/Droid 元数据添加到 init/update 使用的原生工具注册表中（ID、显示名称、命令路径、可用性标志）。
- [x] 1.2 在交互式提示和非交互式 `--tools` 解析中与现有斜杠命令集成一起展示 Factory。

## 2. 斜杠命令模板
- [x] 2.1 为 Factory 的 `openspec-proposal`、`openspec-apply` 和 `openspec-archive` 自定义命令创建共享模板，遵循 Factory 的 CLI 格式。
- [x] 2.2 将模板接入 init/update，使创建时生成，刷新时遵循 OpenSpec 标记。

## 3. 验证
- [x] 3.1 更新或添加自动化测试覆盖，确保 Factory 命令文件正确搭建和刷新。
- [x] 3.2 如有规范要求，在任何面向用户的文案（帮助文本、README 片段）中记录新选项。
