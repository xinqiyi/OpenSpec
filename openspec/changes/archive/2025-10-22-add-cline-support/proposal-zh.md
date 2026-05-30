## 为什么
在 OpenSpec 中添加对 Cline（VS Code 扩展）的支持，使开发者能够使用 Cline 的 AI 驱动编码能力进行 spec 驱动开发 workflow。

## 变更内容
- 添加 Cline 斜杠命令配置器，用于 proposal、应用和 archive 操作
- 添加 Cline 根级 CLINE.md 配置器，用于项目级指令
- 添加 Cline template 导出
- 更新工具和斜杠命令注册表以包含 Cline
- 添加全面的测试覆盖
- **破坏性变更**：无——这是附加功能

## 影响范围
- 受影响的 spec：cli-init（新的工具选项）
- 受影响的代码：`src/core/configurators/slash/cline.ts`、`src/core/configurators/cline.ts`、注册表文件
- 新文件：`.clinerules/openspec-*.md`、`CLINE.md`
