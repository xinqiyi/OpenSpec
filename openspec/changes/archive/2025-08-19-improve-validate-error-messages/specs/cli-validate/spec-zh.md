# Validate 命令

## 新增需求

### 需求：验证应提供可操作的修复步骤
验证输出应包括修复每个错误的特定指导，包括预期结构、示例标题和建议的验证修复命令。

#### 场景：变更中未找到 delta
- **WHEN** 验证解析出零个 delta 的变更时
- **THEN** 显示错误"未找到 delta"并附上指导：
 - 确保 `openspec/changes/{id}/specs/` 存在并包含 `.md` 文件
 - 使用 delta 标题：`## 新增需求`、`## 修改后的需求`、`## 移除的需求`、`## 重命名的需求`
 - 每个需求必须包含至少一个 `#### Scenario:` 块
 - 尝试：`openspec change show {id} --json --deltas-only` 检查解析的内容

#### 场景：缺少必需的部分
- **WHEN** 缺少必需的部分时
- **THEN** 验证器应包含预期的标题名称和最小骨架：
 - 对于 spec：`## Purpose`、`## Requirements`
 - 对于变更：`## Why`、`## What Changes`
 - 显示缺少部分的示例片段

### 需求：验证器应检测可能格式错误的场景并发出修复警告
验证器应识别看起来像场景的要点的行（例如以 WHEN/THEN/AND 开头的行），并发出包含转换为 `#### Scenario:` 示例的有针对性警告。

#### 场景：需求下的要点式 WHEN/THEN
- **WHEN** 在需求下找到以 WHEN/THEN/AND 开头的要点，但没有任何 `#### Scenario:` 标题
- **THEN** 发出警告："场景必须使用 '#### Scenario:' 标题"，并显示转换 template：
```
#### Scenario: 简短名称
- **WHEN** ...
- **THEN** ...
- **AND** ...
```

### 需求：所有问题应包含文件路径和结构化位置
错误、警告和信息消息应包含：
- 源文件路径（`openspec/changes/{id}/proposal.md`、`.../specs/{cap}/spec.md`）
- 结构化路径（例如 `deltas[0].requirements[0].scenarios`）

#### 场景：Zod 验证错误
- **WHEN** schema 验证失败时
- **THEN** 消息应包含 `file`、`path` 和适用的修复提示

### 需求：无效结果应在人类可读输出中包含后续步骤页脚
当项目无效且不使用 `--json` 时，CLI 应附加一个后续步骤页脚，包括：
- 带有计数的摘要行
- 前 3 条指导要点（与最常见或阻塞性错误相关）
- 建议使用 `--json` 和/或调试命令重新运行

#### 场景：变更无效摘要
- **WHEN** 变更验证失败时
- **THEN** 打印"后续步骤"并附带 2-3 条有针对性的要点，并建议 `openspec change show <id> --json --deltas-only`
