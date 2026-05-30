# config-loading 规范

## 目的
定义如何发现、解析、验证 `openspec/config.yaml` 并将其安全地提供给调用者，并包含安全的回退机制。

## 需求
### 需求：从 openspec/config.yaml 加载项目配置

系统应读取和解析位于项目根目录下 `openspec/config.yaml` 的项目配置文件。

#### 场景：存在有效的配置文件
- **当** `openspec/config.yaml` 存在且包含有效的 YAML 内容
- **则** 系统解析该文件并返回一个 ProjectConfig 对象

#### 场景：配置文件不存在
- **当** `openspec/config.yaml` 不存在
- **则** 系统无错误地返回 null

#### 场景：配置文件包含无效的 YAML 语法
- **当** `openspec/config.yaml` 包含格式错误的 YAML
- **则** 系统记录警告消息并返回 null

#### 场景：配置文件包含有效的 YAML 但无效的模式
- **当** `openspec/config.yaml` 包含有效的 YAML 但未通过 Zod 模式验证
- **则** 系统记录包含验证详情的警告消息并返回 null

### 需求：支持 .yml 文件扩展名别名

系统应同时接受 `.yaml` 和 `.yml` 文件扩展名作为配置文件。

#### 场景：配置文件使用 .yml 扩展名
- **当** `openspec/config.yml` 存在且 `openspec/config.yaml` 不存在
- **则** 系统从 `openspec/config.yml` 读取

#### 场景：同时存在 .yaml 和 .yml
- **当** `openspec/config.yaml` 和 `openspec/config.yml` 同时存在
- **则** 系统优先使用 `openspec/config.yaml`

### 需求：使用稳健的逐字段解析

系统应独立解析每个配置字段，收集有效字段并就无效字段发出警告，而不会拒绝整个配置。

#### 场景：Schema 字段有效
- **当** 配置包含 `schema: "spec-driven"`
- **则** schema 字段包含在返回的配置中

#### 场景：Schema 字段缺失
- **当** 配置缺少 `schema` 字段
- **则** 不记录警告（该字段在解析级别是可选的）

#### 场景：Schema 字段为空字符串
- **当** 配置包含 `schema: ""`
- **则** 记录警告且 schema 字段不包含在返回的配置中

#### 场景：Schema 字段类型无效
- **当** 配置包含 `schema: 123`（数字而非字符串）
- **则** 记录警告且 schema 字段不包含在返回的配置中

#### 场景：Context 字段有效
- **当** 配置包含 `context: "Tech stack: TypeScript"`
- **则** context 字段包含在返回的配置中

#### 场景：Context 字段类型无效
- **当** 配置包含 `context: 123`（数字而非字符串）
- **则** 记录警告且 context 字段不包含在返回的配置中

#### 场景：Rules 字段具有有效结构
- **当** 配置包含 `rules: { proposal: ["Rule 1"], specs: ["Rule 2"] }`
- **则** rules 字段包含在返回的配置中，带有有效的规则

#### 场景：Rules 字段中工件值为非数组
- **当** 配置包含 `rules: { proposal: "not an array", specs: ["Valid"] }`
- **则** 为 proposal 记录警告，但 specs 规则仍包含在返回的配置中

#### 场景：Rules 数组包含非字符串元素
- **当** 配置包含 `rules: { proposal: ["Valid rule", 123, ""] }`
- **则** 只包含 "Valid rule"，记录关于无效元素的警告

#### 场景：有效和无效字段混合
- **当** 配置包含有效的 schema、无效的 context 类型、有效的 rules
- **则** 返回包含 schema 和 rules 字段的配置，记录关于 context 的警告

### 需求：强制执行 context 大小限制

系统应拒绝超过 50KB 的 context 字段并记录警告。

#### 场景：Context 在大小限制内
- **当** 配置包含 1KB 的 context
- **则** context 包含在返回的配置中

#### 场景：Context 恰好在大小限制
- **当** 配置包含恰好 50KB 的 context
- **则** context 包含在返回的配置中

#### 场景：Context 超过大小限制
- **当** 配置包含 51KB 的 context
- **则** 记录包含大小和限制的警告，context 字段不包含在返回的配置中

### 需求：将工件 ID 验证推迟到指令加载时

系统在配置加载时不应验证规则中的工件 ID。验证在指令加载时（当 schema 已知时）进行。

#### 场景：加载包含规则的配置
- **当** 配置包含 `rules: { unknownartifact: [...] }`
- **则** 配置成功加载，没有验证错误

#### 场景：验证在指令加载时进行
- **当** 为任何工件加载指令且配置在规则中包含未知工件 ID
- **则** 发出关于未知工件 ID 的警告（详见 rules-injection 规范）

### 需求：优雅处理配置错误而不停止

系统在配置加载或解析失败时应继续使用默认值运行。

#### 场景：命令执行期间配置解析失败
- **当** 配置文件存在语法错误且用户运行 `openspec new change`
- **则** 命令使用默认 schema "spec-driven" 执行

#### 场景：警告对用户可见
- **当** 配置加载失败
- **则** 系统将包含失败详情的警告消息输出到 stderr
