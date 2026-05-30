# 增量：OpenSpec 约定 — 动词-名词 CLI 设计

## 新增需求

### 需求：动词-名词 CLI 命令结构
OpenSpec CLI 设计应使用动词作为顶级命令，名词作为参数或标志提供以实现范围限定。

#### 场景：动词优先的命令发现
- **当** 用户运行类似 `openspec list` 的命令时
- **则** 动词清晰地传达操作
- **且** 名词通过标志或参数细化范围（例如 `--changes`、`--specs`）

#### 场景：名词命令的向后兼容性
- **当** 用户运行名词前缀命令如 `openspec spec ...` 或 `openspec change ...`
- **则** CLI 应继续支持它们至少一个版本
- **且** 显示指向动词优先替代方案的弃用警告

#### 场景：消歧指导
- **当** 项目名称在 changes 和 specs 之间存在歧义时
- **则** `openspec show` 和 `openspec validate` 应接受 `--type spec|change`
- **且** 帮助文本应清晰地记录此信息
