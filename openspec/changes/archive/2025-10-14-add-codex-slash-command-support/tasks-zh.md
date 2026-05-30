## 1. CLI 集成
- [x] 1.1 在 init 工具选择器中添加 Codex，显示文本说明提示位于全局 `.codex/prompts/` 目录，并通过检查受管 Codex 提示文件实现"已配置"检测。
- [x] 1.2 实现 `CodexSlashCommandConfigurator`，写入 `.codex/prompts/openspec-{proposal,apply,archive}.md`，确保提示目录存在并将内容包裹在 OpenSpec 标记中。
// （不需要辅助命令）
- [x] 1.3 在斜杠命令注册表中注册配置器，并将 Codex 包含在 init/update 连接中，使两个命令在适当时调用新配置器。

## 2. 提示模板
- [x] 2.1 扩展共享斜杠命令模板（或添加 Codex 特定包装器），在 Codex 期望用户提供参数的地方注入编号占位符（`$1`、`$2`……）。
- [x] 2.2 验证生成的 Markdown 符合 Codex 的格式期望（无 front matter，标题优先布局），并与参考截图中显示的问题分析器风格匹配。

## 3. 更新支持与测试
- [x] 3.1 更新 `openspec update` 流程，刷新现有的 Codex 提示，但当文件缺失时不创建新文件。
- [x] 3.2 通过设置 `CODEX_HOME` 添加集成覆盖，针对临时全局 Codex 提示目录执行 init/update，断言标记保留和幂等更新。
- [x] 3.3 在 README 和 CHANGELOG 中记录 Codex 的仅全局发现和自动安装。
- [x] 3.3 确认当 CLI 无法写入 Codex 提示目录（权限问题、缺少 home 目录等）时，错误处理提供清晰的路径。

## 4. 文档
- [x] 4.1 在 README 和 changelog 中与其他助手集成一起记录 Codex 斜杠命令支持。
- [x] 4.2 添加发行说明片段，将 Codex 用户指向生成的 `/openspec-proposal`、`/openspec-apply` 和 `/openspec-archive` 命令。
