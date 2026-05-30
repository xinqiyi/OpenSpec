## 上下文

`global-config` spec 定义了 OpenSpec 如何读写 `config.json`，但用户目前需要手动编辑它。本命令为配置提供了一个 CLI 接口。

## 目标 / 非目标

**目标：**
- 为配置管理提供可发现的 CLI
- 支持通过机器可读输出进行脚本化操作
- 使用 zod schema 验证配置变更
- 优雅地处理嵌套键

**非目标：**
- 项目本地配置（保留给未来通过 `--scope` 标志实现）
- 复杂查询（JSONPath、过滤）
- 配置文件格式迁移

## 决策

### 键命名：camelCase + 点号记法

**决策：** 键使用与 JSON 结构匹配的 camelCase，嵌套使用点号记法。

**理由：**
- 匹配实际的 JSON 键（无需转换层）
- 点号记法直观且广泛使用（lodash、jq、kubectl）
- 避免支持多种命名风格的复杂性

**示例：**
```bash
openspec config get featureFlags # 返回对象
openspec config get featureFlags.experimental # 返回嵌套值
openspec config set featureFlags.newFlag true
```

### 类型强制转换：自动检测 + `--string` 覆盖

**决策：** 自动解析值；提供 `--string` 标志强制存储为字符串。

**理由：**
- 对常见情况最直观（`true`、`false`、`123`）
- 为边界情况提供显式覆盖（存储字面量字符串 "true"）
- 遵循 npm/yarn 配置 schema

**强制转换规则：**
| 输入 | 存储为 |
|-------|-----------|
| `true`、`false` | boolean |
| 数字字符串（`123`、`3.14`） | number |
| 其他所有内容 | string |
| 带 `--string` 标志的任何值 | string |

### 输出格式：默认原始输出

**决策：** `get` 只打印原始值。`list` 默认打印类似 YAML 的格式，`--json` 打印 JSON。

**理由：**
- 原始输出支持管道操作：`VAR=$(openspec config get key)`
- 类似 YAML 的格式便于人类阅读检查
- JSON 用于自动化/脚本

### Schema 验证：Zod + 未知字段透传

**决策：** 使用 zod 进行验证，但根据 `global-config` spec 保留未知字段。

**理由：**
- 已知字段的类型安全
- 向前兼容（旧 CLI 不会破坏新配置）
- 遵循已有的 `global-config` spec 要求

### 保留标志：`--scope`

**决策：** 保留 `--scope global|project`，但初始只实现 `global`。

**理由：**
- 避免后续添加项目本地配置时的破坏性变更
- 如果有人尝试 `--scope project`，给出清晰的错误信息

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|------------|
| 点号记法与包含点的键冲突 | 实践中罕见；记录此限制 |
| 类型强制转换的意外行为 | `--string` 逃生口；记录规则 |
| $EDITOR 未设置 | 检查并提供有用的错误信息 |

## 开放问题

无——设计直接明了。
