# cli-config spec

## 目的

提供用于查看和修改全局 OpenSpec 配置的 CLI 界面。使用户能够管理设置而无需手动编辑 JSON 文件，支持脚本编写和自动化。

## 新增需求

### 需求：命令结构

config 命令应为所有配置操作提供子命令。

#### 场景：可用的子命令

- **WHEN** 用户执行 `openspec config --help` 时
- **THEN** 显示可用的子命令：
 - `path` - 显示配置文件位置
 - `list` - 显示所有当前设置
 - `get <key>` - 获取特定值
 - `set <key> <value>` - 设置值
 - `unset <key>` - 移除键（恢复为默认值）
 - `reset` - 将配置重置为默认值
 - `edit` - 在编辑器中打开配置

### 需求：配置路径

config 命令应显示配置文件位置。

#### 场景：显示配置路径

- **WHEN** 用户执行 `openspec config path` 时
- **THEN** 打印配置文件的绝对路径
- **AND** 以代码 0 退出

### 需求：配置列表

config 命令应显示所有当前配置值。

#### 场景：以人类可读格式列出配置

- **WHEN** 用户执行 `openspec config list` 时
- **THEN** 以类似 YAML 的格式显示所有配置值
- **AND** 显示带有缩进的嵌套对象

#### 场景：以 JSON 格式列出配置

- **WHEN** 用户执行 `openspec config list --json` 时
- **THEN** 以有效的 JSON 输出完整配置
- **AND** 仅输出 JSON（无额外文本）

### 需求：配置获取

config 命令应检索特定的配置值。

#### 场景：获取顶层键

- **WHEN** 用户使用有效的顶层键执行 `openspec config get <key>` 时
- **THEN** 仅打印原始值（无标签或格式化）
- **AND** 以代码 0 退出

#### 场景：使用点号表示法获取嵌套键

- **WHEN** 用户执行 `openspec config get featureFlags.someFlag` 时
- **THEN** 使用点号表示法遍历嵌套结构
- **AND** 打印该路径上的值

#### 场景：获取不存在的键

- **WHEN** 用户使用不存在的键执行 `openspec config get <key>` 时
- **THEN** 不打印任何内容（空输出）
- **AND** 以代码 1 退出

#### 场景：获取对象值

- **WHEN** 用户对值为对象的键执行 `openspec config get <key>` 时
- **THEN** 以 JSON 格式打印该对象

### 需求：配置设置

config 命令应设置配置值，并自动进行类型转换。

#### 场景：设置字符串值

- **WHEN** 用户执行 `openspec config set <key> <value>` 时
- **AND** 值不匹配布尔值或数字 schema
- **THEN** 将值存储为字符串
- **AND** 显示确认消息

#### 场景：设置布尔值

- **WHEN** 用户执行 `openspec config set <key> true` 或 `openspec config set <key> false` 时
- **THEN** 将值存储为布尔值（而非字符串）
- **AND** 显示确认消息

#### 场景：设置数字值

- **WHEN** 用户执行 `openspec config set <key> <value>` 时
- **AND** 值是有效的数字（整数或浮点数）
- **THEN** 将值存储为数字（而非字符串）

#### 场景：使用 --string 标志强制为字符串

- **WHEN** 用户执行 `openspec config set <key> <value> --string` 时
- **THEN** 无论内容如何，都将值存储为字符串
- **AND** 这允许将文字"true"或"123"存储为字符串

#### 场景：设置嵌套键

- **WHEN** 用户执行 `openspec config set featureFlags.newFlag true` 时
- **THEN** 创建中间对象（如果不存在）
- **AND** 在嵌套路径上设置值

### 需求：配置取消设置

config 命令应移除配置覆盖。

#### 场景：取消设置现有键

- **WHEN** 用户执行 `openspec config unset <key>` 时
- **AND** 该键存在于配置中
- **THEN** 从配置文件中移除该键
- **AND** 该值恢复为默认值
- **AND** 显示确认消息

#### 场景：取消设置不存在的键

- **WHEN** 用户执行 `openspec config unset <key>` 时
- **AND** 该键不存在于配置中
- **THEN** 显示指示该键未设置的消息
- **AND** 以代码 0 退出

### 需求：配置重置

config 命令应将配置重置为默认值。

#### 场景：带确认的重置所有

- **WHEN** 用户执行 `openspec config reset --all` 时
- **THEN** 在继续前提示确认
- **AND** 如果确认，删除配置文件或重置为默认值
- **AND** 显示确认消息

#### 场景：使用 -y 标志重置所有

- **WHEN** 用户执行 `openspec config reset --all -y` 时
- **THEN** 不提示确认直接重置

#### 场景：不带 --all 标志的重置

- **WHEN** 用户执行 `openspec config reset` 而不带 `--all` 时
- **THEN** 显示错误，指示需要 `--all`
- **AND** 以代码 1 退出

### 需求：配置编辑

config 命令应在用户的编辑器中打开配置文件。

#### 场景：成功打开编辑器

- **WHEN** 用户执行 `openspec config edit` 时
- **AND** 设置了 `$EDITOR` 或 `$VISUAL` 环境变量
- **THEN** 在该编辑器中打开配置文件
- **AND** 如果配置文件不存在，使用默认值创建它
- **AND** 等待编辑器关闭后再返回

#### 场景：未配置编辑器

- **WHEN** 用户执行 `openspec config edit` 时
- **AND** `$EDITOR` 和 `$VISUAL` 均未设置
- **THEN** 显示建议设置 `$EDITOR` 的错误消息
- **AND** 以代码 1 退出

### 需求：键命名约定

config 命令应使用与 JSON 结构匹配的 camelCase 键。

#### 场景：键匹配 JSON 结构

- **WHEN** 通过 CLI 访问配置键时
- **THEN** 使用与实际 JSON 属性名称匹配的 camelCase
- **AND** 支持嵌套访问的点号表示法（例如 `featureFlags.someFlag`）

### 需求：架构验证

config 命令应使用 zod 根据配置架构验证配置写入，同时允许未知字段以实现前向兼容性。

#### 场景：接受未知键

- **WHEN** 用户执行 `openspec config set someFutureKey 123` 时
- **THEN** 值成功保存
- **AND** 以代码 0 退出

#### 场景：拒绝无效的功能标志值

- **WHEN** 用户执行 `openspec config set featureFlags.someFlag notABoolean` 时
- **THEN** 显示描述性错误消息
- **AND** 不修改配置文件
- **AND** 以代码 1 退出

### 需求：保留作用域标志

config 命令应保留 `--scope` 标志以供将来扩展。

#### 场景：Scope 标志默认为全局

- **WHEN** 用户不带 `--scope` 执行任何 config 命令时
- **THEN** 操作全局配置（默认行为）

#### 场景：项目作用域尚未实现

- **WHEN** 用户执行 `openspec config --scope project <subcommand>` 时
- **THEN** 显示错误消息："项目本地配置尚未实现"
- **AND** 以代码 1 退出
