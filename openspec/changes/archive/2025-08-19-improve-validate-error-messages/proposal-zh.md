# 改进验证错误消息

## 为什么

开发人员难以解决验证失败问题，因为当前错误缺少可操作的指导。常见问题包括：缺少增量、缺少必需部分以及被静默忽略的格式错误的场景。没有清晰的修复步骤，用户无法快速纠正结构或格式，导致挫折和返工。通过包含具体修复方案、文件/部分提示和建议命令来改进错误消息，将显著缩短修复时间，使 OpenSpec 更易上手。

## 变更内容

- 验证错误应包括具体的修复步骤（要更改什么以及在何处更改）。
- "未找到增量"错误应指导用户创建带有适当增量标题的 `specs/`，并建议调试命令。
- 缺少必需部分（Spec：Purpose/Requirements；Change：Why/What Changes）应包括预期的标题名称和最小的骨架示例。
- 可能格式错误的场景（带项目符号的 WHEN/THEN/AND）应发出有针对性的警告，解释 `#### Scenario:` 格式，并显示转换模板。
- 所有报告的问题应包括源文件路径和结构化位置（例如 `deltas[0].requirements[0]`）。
- 无效时，非 JSON 输出应以简短的"下一步"页脚结束。

## 影响

- 受影响的 CLI：validate
- 受影响的代码：
  - `src/commands/validate.ts`
  - `src/core/validation/validator.ts`
  - `src/core/validation/constants.ts`
  - `src/core/parsers/*`（使用更丰富的上下文包装抛出的错误）
