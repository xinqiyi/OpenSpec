# spec：规则注入

## 新增的需求

### 需求：仅对匹配的 artifact 注入规则

系统应仅在 artifact ID 匹配规则对象中的键时，将配置中的规则注入到指令中。

#### 场景：规则存在于 artifact 中
- **WHEN** 加载 "proposal" 的指令且配置包含 `rules: { proposal: ["规则 1", "规则 2"] }`
- **THEN** 指令输出包含两条规则的 rules 章节

#### 场景：artifact 没有规则
- **WHEN** 加载 "design" 的指令且配置包含 `rules: { proposal: [...] }`
- **THEN** 指令输出不包含 `<rules>` 标签

#### 场景：规则对象未定义
- **WHEN** 配置省略了 rules 字段或 rules 未定义
- **THEN** 任何 artifact 的指令输出都不包含 `<rules>` 标签

#### 场景：artifact 的规则数组为空
- **WHEN** 配置包含 `rules: { proposal: [] }`
- **THEN** 指令输出不包含 `<rules>` 标签

### 需求：使用 XML 风格标签和项目符号列表格式化规则

系统应将规则包裹在 `<rules>` 标签中，每条规则作为项目符号列表项。

#### 场景：artifact 单条规则
- **WHEN** 配置包含 `rules: { proposal: ["包含回滚计划"] }`
- **THEN** 指令输出包含 `<rules>\n- 包含回滚计划\n</rules>\n\n`

#### 场景：artifact 多条规则
- **WHEN** 配置包含 `rules: { proposal: ["规则 1", "规则 2", "规则 3"] }`
- **THEN** 指令输出将每条规则作为单独的项目符号点

#### 场景：规则出现在上下文之后、template 之前
- **WHEN** 生成同时包含上下文和规则的指令时
- **THEN** 顺序为 `<context>` 然后 `<rules>` 然后 `<template>`

### 需求：保留规则文本原样

系统应注入规则文本而不进行修改、转义或解释。

#### 场景：规则包含 Markdown
- **WHEN** 规则包含如 "使用 **Given/When/Then** 格式" 的 Markdown
- **THEN** Markdown 在注入内容中保留

#### 场景：规则包含特殊字符
- **WHEN** 规则包含如 `<`、`>`、引号等字符
- **THEN** 字符按原样保留

#### 场景：规则是多行字符串
- **WHEN** 规则文本包含换行符
- **THEN** 项目符号点内保留换行符

### 需求：支持不同规则的多 artifact

系统应允许在同一配置中为不同 artifact 设置不同的规则集。

#### 场景：多个 artifact 有规则
- **WHEN** 配置包含 `rules: { proposal: ["P1"], specs: ["S1", "S2"], tasks: ["T1"] }`
- **THEN** proposal 指令仅显示 ["P1"]，specs 仅显示 ["S1", "S2"]，tasks 仅显示 ["T1"]

#### 场景：部分 artifact 有规则，部分没有
- **WHEN** 配置仅为 proposal 和 specs 设置了规则
- **THEN** design 和 tasks 指令没有 `<rules>` 章节

### 需求：规则是对 schema 指导的补充

系统应将配置规则添加到 schema 内置的 artifact 指令中，而非替换它。

#### 场景：artifact 有 schema 指令和配置规则
- **WHEN** artifact 有来自 schema 的内置指令且配置提供了规则
- **THEN** 最终指令包含 schema 指导和配置规则

#### 场景：规则提供额外约束
- **WHEN** schema 说"创建 proposal"且配置规则说"包含回滚计划"
- **THEN** agent 同时看到 schema template 和额外规则

### 需求：在加载指令时验证 artifact ID

系统应在加载指令时验证规则中的 artifact ID 是否与 schema 匹配，并为未知 ID 发出警告。

#### 场景：所有 artifact ID 有效
- **WHEN** 指令已加载且配置对包含这些 artifact 的 schema 设置了 `rules: { proposal: [...], specs: [...] }`
- **THEN** 不发出验证警告

#### 场景：规则中存在未知 artifact ID
- **WHEN** 指令已加载且配置包含 `rules: { unknownartifact: [...] }`
- **THEN** 发出警告："规则中存在未知 artifact ID：'unknownartifact'。schema 'spec-driven' 的有效 ID：design、proposal、specs、tasks"

#### 场景：多个未知 artifact ID
- **WHEN** 指令已加载且配置包含多个未知 artifact ID
- **THEN** 为每个未知 artifact ID 分别发出警告

#### 场景：每个会话仅显示一次验证警告
- **WHEN** 在同一个 CLI 会话中多次加载指令
- **THEN** 每个唯一的验证警告仅显示一次（缓存）
