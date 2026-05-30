# context-injection spec

## 目的
定义如何将 `openspec/config.yaml` 中的项目上下文注入到 workflow 指令中，同时保留源文本和格式。

## 需求
### 需求：向所有制品指令注入上下文

系统应将项目配置中的上下文字段注入到所有制品的指令中，包裹在 XML 风格的 `<context>` 标签内。

#### 场景：配置包含上下文字段
- **WHEN** 配置包含 `context: "Tech stack: TypeScript, React"`
- **THEN** 指令输出包含 `<context>\nTech stack: TypeScript, React\n</context>`

#### 场景：配置没有上下文字段
- **WHEN** 配置省略了上下文字段或 context 未定义
- **THEN** 指令输出不包含 `<context>` 标签

#### 场景：上下文为多行字符串
- **WHEN** 配置包含多行上下文
- **THEN** 指令输出保留 `<context>` 标签内的换行符

#### 场景：上下文应用于所有制品
- **WHEN** 为任何制品（proposal、specs、design、tasks）加载指令时
- **THEN** 所有指令输出中都会出现上下文部分

### 需求：使用 XML 风格标签格式化上下文

系统应将上下文内容包裹在 `<context>` 开始标签和 `</context>` 结束标签中，内容位于单独的行。

#### 场景：上下文标签结构
- **WHEN** 上下文被注入到指令中
- **THEN** 格式严格为 `<context>\n{content}\n</context>\n\n`

#### 场景：上下文出现在 template 之前
- **WHEN** 生成了包含上下文的指令
- **THEN** `<context>` 部分出现在 `<template>` 部分之前

### 需求：保持上下文内容完全按提供的形式呈现

系统应注入上下文内容而不进行修改、转义或解释。

#### 场景：上下文包含特殊字符
- **WHEN** 上下文包含 `<`、`>`、`&`、引号等字符
- **THEN** 字符完全按照配置文件中的写法保留

#### 场景：上下文包含 URL
- **WHEN** 上下文包含类似 "docs at https://example.com" 的 URL
- **THEN** URL 在注入内容中完全保留

#### 场景：上下文包含 Markdown
- **WHEN** 上下文包含如 `**bold**` 或 `[links](url)` 的 Markdown 格式
- **THEN** Markdown 被保留，不进行渲染或转义
