# command-generation spec

## 目的

定义与工具无关的命令内容和适配器合约，用于生成工具特定的 OpenSpec 命令文件。

## 需求

### 需求：CommandContent 接口

系统应定义一个与工具无关的 `CommandContent` 接口，用于命令数据。

#### 场景：CommandContent 结构

- **WHEN** 定义要生成的命令时
- **THEN** `CommandContent` 应包括：
 - `id`：字符串标识符（例如 'explore'、'apply'）
 - `name`：人类可读的名称（例如 'OpenSpec Explore'）
 - `description`：命令目的的简要描述
 - `category`：分组类别（例如 'OpenSpec'）
 - `tags`：标签字符串数组
 - `body`：命令指令内容

### 需求：ToolCommandAdapter 接口

系统应定义一个 `ToolCommandAdapter` 接口，用于按工具格式化。

#### 场景：适配器接口结构

- **WHEN** 实现工具适配器时
- **THEN** `ToolCommandAdapter` 应要求：
 - `toolId`：与 `AIToolOption.value` 匹配的字符串标识符
 - `getFilePath(commandId: string)`：返回命令的文件路径（相对于项目根目录，或全局范围工具如 Codex 则为绝对路径）
 - `formatFile(content: CommandContent)`：返回包含 frontmatter 的完整文件内容

#### 场景：Claude 适配器格式化

- **WHEN** 为 Claude Code 格式化命令时
- **THEN** 适配器应输出包含 `name`、`description`、`category`、`tags` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.claude/commands/opsx/<id>.md`

#### 场景：Cursor 适配器格式化

- **WHEN** 为 Cursor 格式化命令时
- **THEN** 适配器应输出包含 `name`（格式为 `/opsx-<id>`）、`id`、`category`、`description` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.cursor/commands/opsx-<id>.md`

#### 场景：Windsurf 适配器格式化

- **WHEN** 为 Windsurf 格式化命令时
- **THEN** 适配器应输出包含 `name`、`description`、`category`、`tags` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.windsurf/workflows/opsx-<id>.md`

### 需求：命令生成器函数

系统应提供一个 `generateCommand` 函数，将内容与适配器结合。

#### 场景：生成命令文件

- **WHEN** 调用 `generateCommand(content, adapter)`
- **THEN** 应返回一个包含以下内容的对象：
 - `path`：来自 `adapter.getFilePath(content.id)` 的文件路径
 - `fileContent`：来自 `adapter.formatFile(content)` 的格式化内容

#### 场景：生成多个命令

- **WHEN** 为某个工具生成所有 opsx 命令时
- **THEN** 系统应遍历命令内容，并使用该工具的适配器逐一生成

### 需求：CommandAdapterRegistry

系统应提供一个注册表，用于查找工具适配器。

#### 场景：通过工具 ID 获取适配器

- **WHEN** 调用 `CommandAdapterRegistry.get('cursor')`
- **THEN** 应返回 Cursor 适配器，如果未注册则返回 undefined

#### 场景：获取所有适配器

- **WHEN** 调用 `CommandAdapterRegistry.getAll()`
- **THEN** 应返回所有已注册适配器的数组

#### 场景：未找到适配器

- **WHEN** 查找未注册工具的适配器时
- **THEN** `CommandAdapterRegistry.get()` 应返回 undefined
- **AND** 调用方应适当处理缺少适配器的情况

### 需求：共享命令主体内容

命令的主体内容应在所有工具间共享。

#### 场景：跨工具使用相同指令

- **WHEN** 为 Claude 和 Cursor 生成 'explore' 命令时
- **THEN** 两者应使用相同的 `body` 内容
- **AND** 仅 frontmatter 和文件路径应不同
