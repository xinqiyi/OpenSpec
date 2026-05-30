## 先决条件

- [x] 0.1 首先实现 `add-per-change-schema-metadata` 变更

## 1. 模式发现

- [x] 1.1 添加 CLI 命令或辅助工具以列出带描述的模式（供 agent 使用）
- [x] 1.2 确保 `openspec templates --schema <name>` 为任何模式返回工件列表

## 2. 更新 New Change 技能

- [x] 2.1 使用 AskUserQuestion 工具添加模式选择提示
- [x] 2.2 展示可用模式及其描述（spec-driven、tdd 等）
- [x] 2.3 将选定的模式传递给 `openspec new change --schema <name>`
- [x] 2.4 更新输出以显示选择了哪个模式/工作流

## 3. 更新 Continue Change 技能

- [x] 3.1 移除硬编码的工件引用（proposal、specs、design、tasks）
- [x] 3.2 从 `openspec status --json` 动态读取工件列表
- [x] 3.3 调整工件创建指导以使其模式无关
- [x] 3.4 处理模式特定的工件类型（例如 TDD 的 `tests` 工件）

## 4. 更新 Apply Change 技能

- [x] 4.1 使任务检测适用于不同的模式结构
- [x] 4.2 调整上下文文件读取以支持模式特定的工件

## 5. 文档

- [x] 5.1 将模式描述添加到帮助文本或技能指令中
- [x] 5.2 记录何时使用每种模式（TDD 用于错误修复，spec-driven 用于功能等）
