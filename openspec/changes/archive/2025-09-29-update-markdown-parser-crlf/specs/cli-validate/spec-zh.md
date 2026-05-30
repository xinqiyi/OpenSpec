## 新增需求
### 需求：解析器应处理跨平台换行符
Markdown 解析器应能正确识别章节，无论换行符格式如何（LF、CRLF、CR）。

#### 场景：使用 CRLF 换行符解析所需章节
- **GIVEN** 使用 CRLF 换行符保存的变更 proposal Markdown 文件
- **AND** 文档包含 `## Why` 和 `## What Changes`
- **WHEN** 运行 `openspec validate <change-id>`
- **THEN** 验证应识别这些章节且不引发解析错误
