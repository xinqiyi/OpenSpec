# cli-validate spec

## 目的
定义 `openspec validate` 的行为，用于验证变更和 spec，并提供可操作的修复指导和结构化输出。

## 需求
### 需求：验证应提供可操作的修复步骤
验证输出应包含修复每个错误的特定指导，包括预期结构、示例标题和建议用于验证修复的命令。

#### 场景：变更中未找到 delta
- **WHEN** 验证一个解析出零个 delta 的变更时
- **THEN** 显示错误"未找到 delta"，并附带指导：
 - 说明变更 spec 必须包含 `## ADDED Requirements`、`## MODIFIED Requirements`、`## REMOVED Requirements` 或 `## RENAMED Requirements`
 - 提醒作者文件必须位于 `openspec/changes/{id}/specs/<capability>/spec.md` 下
 - 包含明确说明："spec delta 文件不能在操作标题之前以标题开头"
 - 建议运行 `openspec change show {id} --json --deltas-only` 进行调试

#### 场景：缺少必需的部分
- **WHEN** 缺少必需的部分时
- **THEN** 包括预期的标题名称和最小骨架：
 - 对于 spec：`## Purpose`、`## Requirements`
 - 对于变更：`## Why`、`## What Changes`
 - 提供缺失部分的示例片段，并附上可复制的占位散文
 - 提到 `openspec/AGENTS.md` 中的快速参考部分作为权威 template

#### 场景：缺少需求描述文本
- **WHEN** 需求标题在场景之前缺少描述文本时
- **THEN** 发出错误，说明 `### Requirement:` 行必须后跟叙述文本，然后才能有任何 `#### Scenario:` 标题
 - 展示合规示例："### Requirement: Foo" 后跟 "系统应..."
 - 建议在列出场景之前添加 1-2 句描述 spec 性行为的句子
 - 引用 `openspec/AGENTS.md` 中的验证前检查清单

### 需求：验证器应检测可能格式错误的场景并给出修复警告
验证器应识别看起来像场景的项目符号行（例如，以 WHEN/THEN/AND 开头的行），并发出带有转换示例的针对性警告，使用 `#### Scenario:`。

#### 场景：需求下的项目符号 WHEN/THEN
- **WHEN** 在没有任何 `#### Scenario:` 标题的需求下找到以 WHEN/THEN/AND 开头的项目符号时
- **THEN** 发出警告："场景必须使用 '#### Scenario:' 标题"，并显示转换 template：
```
#### 场景：简短名称
- **WHEN** ...
- **THEN** ...
- **AND** ...
```

### 需求：所有问题应包含文件路径和结构化位置
错误、警告和信息消息应包含：
- 源文件路径（`openspec/changes/{id}/proposal.md`、`.../specs/{cap}/spec.md`）
- 结构化路径（例如 `deltas[0].requirements[0].scenarios`）

#### 场景：Zod 验证错误
- **WHEN** 架构验证失败时
- **THEN** 消息应包含 `file`、`path` 和修复提示（如适用）

### 需求：无效结果应在人类可读输出中包含"后续步骤"页脚
当项目无效且未使用 `--json` 时，CLI 应附加"后续步骤"页脚，包括：
- 包含计数的摘要行
- 前 3 条指导要点（与最常见或阻塞性错误相关）
- 建议使用 `--json` 和/或调试命令重新运行

#### 场景：变更无效摘要
- **WHEN** 变更验证失败时
- **THEN** 打印"后续步骤"，附带 2-3 条针对性要点，并建议使用 `openspec change show <id> --json --deltas-only`

### 需求：顶层 validate 命令

CLI 应提供顶层的 `validate` 命令，用于验证变更和 spec，并具有灵活的选择选项。

#### 场景：交互式验证选择

- **WHEN** 不带参数执行 `openspec validate` 时
- **THEN** 提示用户选择要验证的内容（全部、变更、spec 或特定项目）
- **AND** 根据选择执行验证
- **AND** 以适当的格式显示结果

#### 场景：非交互式环境不提示

- **GIVEN** 标准输入不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **WHEN** 不带参数执行 `openspec validate` 时
- **THEN** 不进行交互式提示
- **AND** 打印有用的提示，列出可用的命令/标志，并以代码 1 退出

#### 场景：直接项目验证

- **WHEN** 执行 `openspec validate <item-name>` 时
- **THEN** 自动检测项目是变更还是 spec
- **AND** 验证指定的项目
- **AND** 显示验证结果

### 需求：批量验证和过滤验证

validate 命令应支持批量验证（`--all`）和按类型过滤验证（`--changes`、`--specs`）的标志。

#### 场景：验证所有内容

- **WHEN** 执行 `openspec validate --all` 时
- **THEN** 验证 `openspec/changes/` 中所有变更（排除 archive）
- **AND** 验证 `openspec/specs/` 中所有 spec
- **AND** 显示显示通过/失败项目的摘要
- **AND** 如果任何验证失败，以代码 1 退出

#### 场景：批量验证的范围

- **WHEN** 使用 `--all` 或 `--changes` 验证时
- **THEN** 包括 `openspec/changes/` 下所有变更 proposal
- **AND** 排除 `openspec/changes/archive/` 目录

- **WHEN** 使用 `--specs` 验证时
- **THEN** 包括 `openspec/specs/<id>/spec.md` 下所有具有 `spec.md` 的 spec

#### 场景：验证所有变更

- **WHEN** 执行 `openspec validate --changes` 时
- **THEN** 验证 `openspec/changes/` 中所有变更（排除 archive）
- **AND** 显示每个变更的结果
- **AND** 显示摘要统计信息

#### 场景：验证所有 spec

- **WHEN** 执行 `openspec validate --specs` 时
- **THEN** 验证 `openspec/specs/` 中所有 spec
- **AND** 显示每个 spec 的结果
- **AND** 显示摘要统计信息

### 需求：验证选项和进度指示

validate 命令应支持标准验证选项（`--strict`、`--json`），并在批量操作期间显示进度。

#### 场景：严格验证

- **WHEN** 执行 `openspec validate --all --strict` 时
- **THEN** 对所有项目应用严格验证
- **AND** 将警告视为错误
- **AND** 如果任何项目有警告或错误则失败

#### 场景：JSON 输出

- **WHEN** 执行 `openspec validate --all --json` 时
- **THEN** 以 JSON 格式输出验证结果
- **AND** 包含每个项目的详细问题
- **AND** 包含摘要统计信息

#### 场景：批量验证的 JSON 输出架构

- **WHEN** 执行 `openspec validate --all --json`（或 `--changes` / `--specs`）时
- **THEN** 输出具有以下形状的 JSON 对象：
 - `items`：对象数组，字段为 `{ id: string, type: "change"|"spec", valid: boolean, issues: Issue[], durationMs: number }`
 - `summary`：对象 `{ totals: { items: number, passed: number, failed: number }, byType: { change?: { items: number, passed: number, failed: number }, spec?: { items: number, passed: number, failed: number } } }`
 - `version`：架构的字符串标识符（例如 `"1.0"`）
- **AND** 如果任何 `items[].valid === false`，以代码 1 退出

其中 `Issue` 遵循现有的逐项验证报告形状 `{ level: "ERROR"|"WARNING"|"INFO", path: string, message: string }`。

#### 场景：显示验证进度

- **WHEN** 验证多个项目（--all、--changes 或 --specs）时
- **THEN** 显示进度指示器或状态更新
- **AND** 指示当前正在验证哪个项目
- **AND** 显示通过/失败项目的运行计数

#### 场景：性能并发限制

- **WHEN** 验证多个项目时
- **THEN** 以有限的并发度运行验证（例如，4-8 个并行）
- **AND** 确保进度指示器保持响应

### 需求：项目类型检测和歧义处理

validate 命令应处理歧义名称和显式类型覆盖，以确保清晰、确定的行为。

#### 场景：直接项目验证，带自动类型检测

- **WHEN** 执行 `openspec validate <item-name>` 时
- **THEN** 如果 `<item-name>` 唯一匹配变更或 spec，则验证该项目

#### 场景：变更和 spec 名称之间的歧义

- **GIVEN** `<item-name>` 同时作为变更和 spec 存在
- **WHEN** 执行 `openspec validate <item-name>` 时
- **THEN** 打印歧义错误，说明两者都匹配
- **AND** 建议传递 `--type change` 或 `--type spec`，或使用 `openspec change validate` / `openspec spec validate`
- **AND** 以代码 1 退出，不执行验证

#### 场景：未知的项目名称

- **WHEN** `<item-name>` 既不匹配变更也不匹配 spec 时
- **THEN** 打印未找到错误
- **AND** 在可用时显示最接近的匹配建议
- **AND** 以代码 1 退出

#### 场景：显式类型覆盖

- **WHEN** 执行 `openspec validate --type change <item>` 时
- **THEN** 将 `<item>` 视为变更 ID 并进行验证（跳过自动检测）

- **WHEN** 执行 `openspec validate --type spec <item>` 时
- **THEN** 将 `<item>` 视为 spec ID 并进行验证（跳过自动检测）

### 需求：交互控制

- CLI 应尊重 `--no-interactive` 以禁用提示。
- CLI 应尊重 `OPEN_SPEC_INTERACTIVE=0` 以全局禁用提示。
- 交互式提示仅应在标准输入是 TTY 且交互功能未被禁用时显示。

#### 场景：通过标志或环境禁用提示

- **WHEN** 使用 `--no-interactive` 或环境 `OPEN_SPEC_INTERACTIVE=0` 执行 `openspec validate` 时
- **THEN**CLI 不应显示交互式提示
- **AND** 应根据需要打印非交互式提示或选择的输出

### 需求：解析器应处理跨平台换行符
Markdown 解析器应正确识别部分，无论换行符格式如何（LF、CRLF、CR）。

#### 场景：使用 CRLF 换行符解析必需部分
- **GIVEN** 使用 CRLF 换行符保存的变更 proposal markdown
- **AND** 文档包含 `## Why` 和 `## What Changes`
- **WHEN** 运行 `openspec validate <change-id>` 时
- **THEN** 验证应识别这些部分并且不引发解析错误
