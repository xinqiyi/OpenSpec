## 为什么
在 OpenSpec 中添加对 Crush AI 助手的支持，使开发者能够利用 Crush 增强的能力进行 spec 驱动开发 workflow。

## 变更内容
- 为 proposal、apply 和 archive 操作添加 Crush 斜杠命令配置器
- 添加 Crush 特定的 AGENTS.md 配置 template
- 更新工具注册表以包含 Crush 配置器
- **破坏性变更**：无——这是一个附加功能

## 影响
- 受影响的 spec：cli-init（新的工具选项）
- 受影响的代码：src/core/configurators/slash/crush.ts、registry.ts
- 新文件：.crush/commands/openspec/（proposal.md、apply.md、archive.md）
