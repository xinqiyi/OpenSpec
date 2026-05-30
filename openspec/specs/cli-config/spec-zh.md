# cli-config spec

## 目的
提供一个用户友好的 CLI 界面，用于查看和修改全局 OpenSpec 配置设置，而无需手动编辑 JSON 文件。

## 需求
### 需求：命令结构

config 命令应提供用于所有配置操作的子命令。

#### 场景：可用的子命令

- **WHEN** 用户执行 `openspec config --help`
- **THEN** 显示可用的子命令：
 - `path` - 显示配置文件位置
 - `list` - 显示所有当前设置
 - `get <key>` - 获取特定值
 - `set <key> <value>` - 设置一个值
 - `unset <key>` - 移除一个键（恢复为默认值）
 - `reset` - 将配置重置为默认值
 - `edit` - 在编辑器中打开配置

### 需求：配置路径

config 命令应显示配置文件位置。

#### 场景：显示配置路径

- **WHEN** 用户执行 `openspec config path`
- **THEN** 打印配置文件的绝对路径
- **AND** 以代码 0 退出

### 需求：配置列表

config 命令应显示所有当前配置值。

#### 场景：以人类可读格式列出配置

- **WHEN** 用户执行 `openspec config list`
- **THEN** 以类似 YAML 的格式显示所有配置值
- **AND** 显示带缩进的嵌套对象

#### 场景：以 JSON 格式列出配置

- **WHEN** 用户执行 `openspec config list --json`
- **THEN** 将完整配置作为有效的 JSON 输出
- **AND** 仅输出 JSON（无额外文本）

### 需求：配置获取

config 命令应检索特定的配置值。

#### 场景：获取顶层键

- **WHEN** 用户使用有效的顶层键执行 `openspec config get <key>`
- **THEN** 仅打印原始值（无标签或格式）
- **AND** 以代码 0 退出

#### 场景：使用点号表示法获取嵌套键

- **WHEN** 用户执行 `openspec config get featureFlags.someFlag`
- **THEN** 使用点号表示法遍历嵌套结构
- **AND** 打印该路径处的值

#### 场景：获取不存在的键

- **WHEN** 用户使用不存在的键执行 `openspec config get <key>`
- **THEN** 不打印任何内容（空输出）
- **AND** 以代码 1 退出

#### 场景：获取对象值

- **WHEN** 用户执行 `openspec config get <key>` 且值为对象
- **THEN** 将对象作为 JSON 打印

### 需求：配置设置

config 命令应设置配置值，并自动进行类型强制转换。

#### 场景：设置字符串值

- **WHEN** 用户执行 `openspec config set <key> <value>`
- **AND** 值不匹配布尔或数字 schema
- **THEN** 将值存储为字符串
- **AND** 显示确认消息

#### 场景：设置布尔值

- **WHEN** 用户执行 `openspec config set <key> true` 或 `openspec config set <key> false`
- **THEN** 将值存储为布尔值（非字符串）
- **AND** 显示确认消息

#### 场景：设置数值

- **WHEN** 用户执行 `openspec config set <key> <value>`
- **AND** 值是有效数字（整数或浮点数）
- **THEN** 将值存储为数字（非字符串）

#### 场景：使用 --string 标志强制为字符串

- **WHEN** 用户执行 `openspec config set <key> <value> --string`
- **THEN** 无论内容如何，都将值存储为字符串
- **AND** 这允许将字面量 "true" 或 "123" 存储为字符串

#### 场景：设置嵌套键

- **WHEN** 用户执行 `openspec config set featureFlags.newFlag true`
- **THEN** 如果中间对象不存在，则创建它们
- **AND** 在嵌套路径处设置值

### 需求：配置移除

config 命令应移除配置覆盖。

#### 场景：移除现有键

- **WHEN** 用户执行 `openspec config unset <key>`
- **AND** 该键存在于配置中
- **THEN** 从配置文件中移除该键
- **AND** 该值恢复为其默认值
- **AND** 显示确认消息

#### 场景：移除不存在的键

- **WHEN** 用户执行 `openspec config unset <key>`
- **AND** 该键不存在于配置中
- **THEN** 显示消息指示该键未设置
- **AND** 以代码 0 退出

### 需求：配置重置

config 命令应将配置重置为默认值。

#### 场景：带确认的全部重置

- **WHEN** 用户执行 `openspec config reset --all`
- **THEN** 在继续之前提示确认
- **AND** 如果确认，删除配置文件或重置为默认值
- **AND** 显示确认消息

#### 场景：使用 -y 标志的全部重置

- **WHEN** 用户执行 `openspec config reset --all -y`
- **THEN** 无需提示确认即可重置

#### 场景：不带 --all 标志的重置

- **WHEN** 用户执行 `openspec config reset` 而不带 `--all`
- **THEN** 显示错误指示需要 `--all`
- **AND** 以代码 1 退出

### 需求：配置编辑

config 命令应在用户的编辑器中打开配置文件。

#### 场景：成功打开编辑器

- **WHEN** 用户执行 `openspec config edit`
- **AND** 设置了 `$EDITOR` 或 `$VISUAL` 环境变量
- **THEN** 在该编辑器中打开配置文件
- **AND** 如果配置文件不存在，则使用默认值创建
- **AND** 等待编辑器关闭后再返回

#### 场景：未配置编辑器

- **WHEN** 用户执行 `openspec config edit`
- **AND** 既未设置 `$EDITOR` 也未设置 `$VISUAL`
- **THEN** 显示错误消息，建议设置 `$EDITOR`
- **AND** 以代码 1 退出

### 需求：配置文件配置流程

`openspec config profile` 命令应提供一个操作优先的交互式流程，允许用户独立修改交付和 workflow 设置。

#### 场景：首先显示当前配置文件摘要

- **WHEN** 用户在交互式终端中运行 `openspec config profile`
- **THEN** 显示当前状态标题，包括：
 - 当前交付值
 - workflow 数量及配置文件标签（core 或 custom）

#### 场景：操作优先菜单提供可跳过的路径

- **WHEN** 用户以交互方式运行 `openspec config profile`
- **THEN** 第一个提示应提供：
 - `更改交付和 workflow`
 - `仅更改交付`
 - `仅更改 workflow`
 - `保持当前设置（退出）`

#### 场景：交付提示标记当前选择

- **WHEN** 在 `openspec config profile` 中显示交付选择时
- **THEN** 当前配置的交付选项应在标签中包含 `[current]`
- **AND** 该值默认应被预选

#### 场景：无操作退出而不保存或应用提示

- **WHEN** 用户选择 `保持当前设置（退出）` 或做出不改变有效配置值的选项
- **THEN** 命令应打印 `无配置更改。`
- **AND** 不应写入配置更改
- **AND** 不应询问是否将更新应用于当前项目

#### 场景：当前项目不同步时无操作警告

- **WHEN** `openspec config profile` 在 OpenSpec 项目内以 `无配置更改。` 退出
- **AND** 项目文件与当前全局配置文件/交付不同步
- **THEN** 显示非阻塞警告，说明全局配置尚未应用于此项目
- **AND** 包括运行 `openspec update` 以同步项目文件的指导

#### 场景：应用提示仅在实际更改时显示

- **WHEN** 配置值已更改并保存
- **AND** 当前目录是 OpenSpec 项目
- **THEN** 提示 `立即将更改应用于此项目？`
- **AND** 如果确认，为当前项目运行 `openspec update`

### 需求：键命名约定

config 命令应使用与 JSON 结构匹配的 camelCase 键。

#### 场景：键与 JSON 结构匹配

- **WHEN** 通过 CLI 访问配置键时
- **THEN** 使用与实际 JSON 属性名称匹配的 camelCase
- **AND** 支持用于嵌套访问的点号表示法（例如，`featureFlags.someFlag`）

### 需求：架构验证

config 命令应使用 zod 对照配置架构验证配置写入，同时默认拒绝 `config set` 的未知键，除非显式覆盖。

#### 场景：默认拒绝未知键

- **WHEN** 用户执行 `openspec config set someFutureKey 123`
- **THEN** 显示描述性错误消息，指示该键无效
- **AND** 不修改配置文件
- **AND** 以代码 1 退出

#### 场景：使用覆盖接受未知键

- **WHEN** 用户执行 `openspec config set someFutureKey 123 --allow-unknown`
- **THEN** 值成功保存
- **AND** 以代码 0 退出

#### 场景：无效功能标志值被拒绝

- **WHEN** 用户执行 `openspec config set featureFlags.someFlag notABoolean`
- **THEN** 显示描述性错误消息
- **AND** 不修改配置文件
- **AND** 以代码 1 退出

### 需求：保留范围标志

config 命令应保留 `--scope` 标志以供将来扩展。

#### 场景：范围标志默认为全局

- **WHEN** 用户不带 `--scope` 执行任何配置命令
- **THEN** 操作全局配置（默认行为）

#### 场景：项目范围尚未实现

- **WHEN** 用户执行 `openspec config --scope project <subcommand>`
- **THEN** 显示错误消息："项目本地配置尚未实现"
- **AND** 以代码 1 退出

### 需求：配置文件应用于当前 workspace
`openspec config profile` 命令应保持全局，同时在从 OpenSpec workspace 内部运行时提供显式的 workspace 应用路径。

#### 场景：在 workspace 内部运行配置文件
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** 用户使用交互式 `openspec config profile` 更改配置文件或交付设置
- **THEN** OpenSpec 应保存全局配置更改
- **AND** 应提示：`立即将更改应用于此 workspace？`

#### 场景：用户确认 workspace 应用
- **GIVEN** `openspec config profile` 在 workspace 内部更改了全局配置文件或交付设置
- **WHEN** 用户确认 workspace 应用提示
- **THEN** OpenSpec 应为当前 workspace 运行 `openspec workspace update`
- **AND** 除非当前 planning 根目录是 repository 本地，否则不应运行 repository 本地 `openspec update`

#### 场景：用户拒绝 workspace 应用
- **GIVEN** `openspec config profile` 在 workspace 内部更改了全局配置文件或交付设置
- **WHEN** 用户拒绝 workspace 应用提示
- **THEN** OpenSpec 应说明全局配置已更新
- **AND** 应告诉用户稍后运行 `openspec workspace update` 以将配置文件应用于 workspace 本地 skill
- **AND** 不应修改 workspace skill 文件

#### 场景：workspace 内部无操作
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** `openspec config profile` 退出时没有有效的配置更改
- **THEN** OpenSpec 不应提示应用更改
- **AND** 如果 workspace 本地 skill 与当前全局配置文件不同步，应发出警告
- **AND** 警告应建议 `openspec workspace update`

#### 场景：workspace 内部的 Core 预设快捷方式
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** 用户运行 `openspec config profile core`
- **THEN** OpenSpec 应保存全局配置更改，而不提示立即应用
- **AND** 应告诉用户运行 `openspec workspace update` 以将配置文件应用于 workspace 本地 skill

#### 场景：repository 项目内部的 Core 预设快捷方式
- **GIVEN** 命令从 repository 本地 OpenSpec 项目内部运行
- **WHEN** 用户运行 `openspec config profile core`
- **THEN** OpenSpec 应保留现有的 repository 本地快捷方式行为
- **AND** 应告诉用户运行 `openspec update` 以将配置文件应用于项目文件

#### 场景：workspace planning 根目录优先于链接的 repository 项目
- **GIVEN** 命令在 workspace planning 根目录下的路径中运行，且该路径也可能检测到 repository 本地 OpenSpec 项目
- **WHEN** OpenSpec 决定显示哪个应用提示时
- **THEN** 最近的当前 planning 根目录应决定是提供 `openspec workspace update` 还是 repository 本地 `openspec update`
- **AND** 当当前 planning 根目录是 workspace 时，OpenSpec 不应将配置文件更改应用于链接的 repository

#### 场景：链接的 repository 保留 repository 本地配置文件行为
- **GIVEN** repository 本地 OpenSpec 项目被注册为 workspace 链接
- **AND** 命令从该链接 repository 内部运行，而不是从 workspace planning 根目录
- **WHEN** OpenSpec 决定显示哪个应用提示或指导时
- **THEN** OpenSpec 应为该 repository 保留 repository 本地 `openspec update` 行为
- **AND** 除非 workspace 被显式选择，否则不应提供 `openspec workspace update`
