## 1. 防范回归
- [x] 1.1 添加一个单元测试，将 CRLF 换行符的变更文档输入 `MarkdownParser.parseChange`，并断言 `Why`/`What Changes` 被检测到。
- [x] 1.2 添加一个 CLI 生成/e2e 测试，写入一个 CRLF 换行符的变更，运行 `openspec validate`，并期望成功。

## 2. 规范化解析
- [x] 2.1 在构造 `MarkdownParser` 时规范化换行符，使标题和内容比较忽略 `\r`。
- [x] 2.2 确保所有 CLI 入口点（validate、view、spec 转换）都复用规范化的解析器路径。

## 3. 文档与验证
- [x] 3.1 更新 `cli-validate` 规范，添加一个覆盖 CRLF 换行符的场景。
- [x] 3.2 运行解析器和 CLI 测试套件（`pnpm test`、相关的 spawn 测试），确认修复有效。
