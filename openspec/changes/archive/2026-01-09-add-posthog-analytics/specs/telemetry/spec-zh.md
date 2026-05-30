## 新增需求

### 需求：命令执行跟踪
当任何 CLI 命令执行时，系统应向 PostHog 发送一个 `command_executed` 事件，仅包含命令名称和 OpenSpec 版本作为属性。

#### 场景：标准命令执行
- **WHEN** 用户运行任何 openspec 命令
- **THEN** 系统发送带有 `command` 和 `version` 属性的 `command_executed` 事件

#### 场景：子命令执行
- **WHEN** 用户运行嵌套命令如 `openspec change apply`
- **THEN** 系统发送带有完整命令路径的 `command_executed` 事件（例如 `change:apply`）

### 需求：隐私保护的事件设计
系统的遥测事件不应包含命令参数、文件路径、项目名称、spec 内容、错误消息或 IP 地址。

#### 场景：带参数的命令
- **WHEN** 用户运行 `openspec init my-project --force`
- **THEN** 遥测事件仅包含 `command: "init"` 和 `version: "<version>"`，不含参数

#### 场景：IP 地址排除
- **WHEN** 系统发送遥测事件
- **THEN** 事件显式设置 `$ip: null` 以防止 IP 跟踪

### 需求：环境变量选择退出
当设置了 `OPENSPEC_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 环境变量时，系统应禁用遥测。

#### 场景：OPENSPEC_TELEMETRY 选择退出
- **WHEN** 环境中设置了 `OPENSPEC_TELEMETRY=0`
- **THEN** 系统不发送任何遥测事件

#### 场景：DO_NOT_TRACK 选择退出
- **WHEN** 环境中设置了 `DO_NOT_TRACK=1`
- **THEN** 系统不发送任何遥测事件

#### 场景：环境变量优先
- **WHEN** 用户之前使用过 CLI（配置存在）
- **AND** 用户设置了 `OPENSPEC_TELEMETRY=0`
- **THEN** 无论配置状态如何，遥测都被禁用

### 需求：CI 环境自动禁用
当检测到 `CI=true` 环境变量时，系统应自动禁用遥测。

#### 场景：CI 环境检测
- **WHEN** 环境中设置了 `CI=true`
- **THEN** 系统不发送任何遥测事件

#### 场景：CI 中显式启用
- **WHEN** 设置了 `CI=true`
- **AND** 显式设置了 `OPENSPEC_TELEMETRY=1`
- **THEN** 遥测保持禁用（为隐私考虑，CI 优先）

### 需求：首次运行遥测通知
系统应在首次命令执行时、发送任何遥测数据之前显示一行遥测披露通知。

#### 场景：首次命令执行
- **WHEN** 用户运行他们的第一个 openspec 命令
- **AND** 遥测已启用
- **THEN** 系统显示："注意：OpenSpec 收集匿名使用统计。选择退出：OPENSPEC_TELEMETRY=0"

#### 场景：后续命令执行
- **WHEN** 用户已经看到过通知（配置中 noticeSeen: true）
- **THEN** 系统不再显示通知

#### 场景：通知在遥测之前
- **WHEN** 显示首次运行通知时
- **THEN** 通知在任何遥测事件发送之前出现

### 需求：匿名用户标识
系统应在首次发送遥测时生成一个随机 UUID 作为匿名标识符，存储在全局配置中。

#### 场景：首次遥测事件
- **WHEN** 发送第一个遥测事件
- **AND** 配置中不存在 anonymousId
- **THEN** 系统生成一个随机 UUID v4 并存储在配置中

#### 场景：持久身份
- **WHEN** 用户在多个会话中运行多个命令
- **THEN** 所有事件使用相同的 anonymousId

#### 场景：选择退出的惰性生成
- **WHEN** 用户在运行任何命令之前选择退出
- **THEN** 永远不会生成或存储 anonymousId

### 需求：即时事件发送
系统应立即发送遥测事件，无需批处理，使用 `flushAt: 1` 和 `flushInterval: 0` 配置。

#### 场景：事件传输时机
- **WHEN** 命令执行
- **THEN** 遥测事件立即发送，不排队等待批处理传输

### 需求：优雅关闭
系统应在 CLI 退出前调用 `posthog.shutdown()` 以确保待处理事件被刷新。

#### 场景：正常退出
- **WHEN** 命令成功完成
- **THEN** 系统在退出前等待 `shutdown()`

#### 场景：错误退出
- **WHEN** 命令因错误失败
- **THEN** 系统在退出前仍然等待 `shutdown()`

### 需求：静默失败处理
系统应静默忽略遥测失败，而不影响 CLI 功能。

#### 场景：网络故障
- **WHEN** 遥测请求因网络错误失败
- **THEN** CLI 命令正常完成，不显示错误消息

#### 场景：PostHog 服务中断
- **WHEN** PostHog 服务不可用
- **THEN** CLI 命令正常完成，不显示错误消息

#### 场景：关闭失败
- **WHEN** `shutdown()` 失败或超时
- **THEN** CLI 正常退出，不显示错误消息
