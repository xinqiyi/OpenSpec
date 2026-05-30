# 变更：添加带 JSON 输出的 Spec 命令

## 为什么

目前，OpenSpec spec 只能作为 Markdown 文件查看。这使得程序化访问变得困难，并阻止了与 CI/CD 流水线、外部工具和自动化处理的集成。

## 变更内容

- 添加新的 `openspec spec` 命令，包含三个子命令：`show`、`list` 和 `validate`
- 使用基于标题的解析实现 spec 的 JSON 输出功能
- 添加用于 spec 结构验证的 Zod schema
- 启用内容过滤选项（仅需求、无场景、特定需求）

## 影响

- **受影响的 spec**：无（新能力）
- **受影响的代码**：
 - src/cli/index.ts（注册新命令）
 - package.json（添加 zod 依赖）
