## 为什么

用户需要一种方式来查看和修改他们的全局 OpenSpec 设置，而无需手动编辑 JSON 文件。`global-config` 规范提供了基础，但没有面向用户的界面来与配置交互。专门的 `openspec config` 命令提供了可发现性和易用性。

## 变更内容

添加 `openspec config` 子命令，支持以下操作：

```bash
openspec config path                          # 显示配置文件位置
openspec config list [--json]                 # 显示所有当前设置
openspec config get <key>                     # 获取特定值（原始、可脚本化）
openspec config set <key> <value> [--string]  # 设置值（自动强制转换类型）
openspec config unset <key>                   # 移除键（恢复为默认值）
openspec config reset --all [-y]              # 将所有设置重置为默认值
openspec config edit                          # 在 $EDITOR 中打开配置
```

**关键设计决策：**
- **键命名**：使用 camelCase 以匹配 JSON 结构（例如 `featureFlags.someFlag`）
- **嵌套键**：支持点号记法进行嵌套访问
- **类型强制转换**：默认自动检测类型；`--string` 标志强制存储为字符串
- **可脚本化输出**：`get` 仅打印原始值（无标签），便于管道操作
- **Zod 验证**：使用 zod 进行配置 schema 验证和类型安全
- **面向未来**：保留 `--scope global|project` 标志，用于潜在的项目本地配置

**使用示例：**
```bash
$ openspec config path
/Users/me/.config/openspec/config.json

$ openspec config list
featureFlags: {}

$ openspec config set featureFlags.enableTelemetry false
设置 featureFlags.enableTelemetry = false

$ openspec config get featureFlags.enableTelemetry
false

$ openspec config list --json
{
  "featureFlags": {}
}

$ openspec config unset featureFlags.enableTelemetry
取消设置 featureFlags.enableTelemetry（恢复为默认值）

$ openspec config edit
# 在 $EDITOR 中打开 config.json
```

## 影响

- 受影响的规范：新的 `cli-config` 能力
- 受影响的代码：
  - 新的 `src/commands/config.ts`
  - 新的 `src/core/config-schema.ts`（zod schema）
  - 更新 CLI 入口点以注册 config 命令
- 依赖：需要 `global-config` 规范（已实现）
