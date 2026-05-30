## 1. 设置

- [x] 1.1 添加 `posthog-node` 包作为依赖
- [x] 1.2 创建 `src/telemetry/` 模块目录
- [x] 1.3 添加 PostHog API 密钥配置（环境变量或内嵌）

## 2. 全局配置

- [x] 2.1 创建或扩展全局配置模块，用于 `~/.config/openspec/config.json`
- [x] 2.2 实现保留现有配置字段的读/写函数
- [x] 2.3 定义遥测配置结构（`anonymousId`、`noticeSeen`）

## 3. 核心遥测模块

- [x] 3.1 实现 `isTelemetryEnabled()`，检查 `OPENSPEC_TELEMETRY`、`DO_NOT_TRACK` 和 `CI` 环境变量
- [x] 3.2 实现 `getOrCreateAnonymousId()`，具有惰性 UUID 生成
- [x] 3.3 使用 `flushAt: 1` 和 `flushInterval: 0` 初始化 PostHog 客户端
- [x] 3.4 实现带有 `$ip: null` 的 `trackCommand(commandName, version)`
- [x] 3.5 实现带有 try/catch 静默失败处理的 `shutdown()`

## 4. 首次运行通知

- [x] 4.1 实现 `maybeShowTelemetryNotice()` 函数
- [x] 4.2 在显示通知前检查 `noticeSeen` 标志
- [x] 4.3 显示通知文本："注意：OpenSpec 收集匿名使用统计。退出：OPENSPEC_TELEMETRY=0"
- [x] 4.4 首次显示后在配置中更新 `noticeSeen`

## 5. CLI 集成

- [x] 5.1 添加 Commander.js `preAction` 钩子以显示通知和跟踪命令
- [x] 5.2 添加 Commander.js `postAction` 钩子以调用 shutdown
- [x] 5.3 处理子命令路径提取（例如，`change:apply`）

## 6. 测试

- [x] 6.1 测试通过 `OPENSPEC_TELEMETRY=0` 退出
- [x] 6.2 测试通过 `DO_NOT_TRACK=1` 退出
- [x] 6.3 测试在 CI 环境中自动禁用
- [x] 6.4 测试首次运行通知显示和 noticeSeen 持久化
- [x] 6.5 测试匿名 ID 生成和持久化
- [x] 6.6 测试网络错误时的静默失败（模拟 PostHog）

## 7. 文档

- [x] 7.1 在 README 中添加遥测披露部分
- [x] 7.2 记录退出方法（`OPENSPEC_TELEMETRY=0`、`DO_NOT_TRACK=1`）
- [x] 7.3 记录收集和不收集的数据
