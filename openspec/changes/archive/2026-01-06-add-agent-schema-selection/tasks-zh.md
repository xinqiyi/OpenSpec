## 先决条件

- [x] 0.1 首先实现 `add-per-change-schema-metadata` 变更

## 1. schema 发现

- [x] 1.1 添加 CLI 命令或辅助工具以列出带描述的 schema（供 agent 使用）
- [x] 1.2 确保 `openspec templates --schema <name>` 为任何 schema 返回 artifact 列表

## 2. 更新 New Change skill

- [x] 2.1 使用 AskUserQuestion 工具添加 schema 选择提示
- [x] 2.2 展示可用 schema 及其描述（spec-driven、tdd 等）
- [x] 2.3 将选定的 schema 传递给 `openspec new change --schema <name>`
- [x] 2.4 更新输出以显示选择了哪个 schema/workflow

## 3. 更新 Continue Change skill

- [x] 3.1 移除硬编码的 artifact 引用（proposal、specs、design、tasks）
- [x] 3.2 从 `openspec status --json` 动态读取 artifact 列表
- [x] 3.3 调整 artifact 创建指导以使其 schema 无关
- [x] 3.4 处理 schema 特定的 artifact 类型（例如 TDD 的 `tests` artifact）

## 4. 更新 Apply Change skill

- [x] 4.1 使任务检测适用于不同的 schema 结构
- [x] 4.2 调整上下文文件读取以支持 schema 特定的 artifact

## 5. 文档

- [x] 5.1 将 schema 描述添加到帮助文本或 skill 指令中
- [x] 5.2 记录何时使用每种 schema（TDD 用于错误修复，spec-driven 用于功能等）
