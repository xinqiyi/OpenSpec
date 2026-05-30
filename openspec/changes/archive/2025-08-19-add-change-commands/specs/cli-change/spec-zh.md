## 新增需求

### 需求：变更命令

系统应提供一个 `change` 命令，包含用于显示、列出和验证变更提案的子命令。

#### 场景：以 JSON 格式显示变更

- **当** 执行 `openspec change show update-error --json`
- **则** 解析 markdown 变更文件
- **并且** 提取变更结构和增量
- **并且** 输出有效的 JSON 到标准输出

#### 场景：列出所有变更

- **当** 执行 `openspec change list`
- **则** 扫描 openspec/changes 目录
- **并且** 返回所有待处理变更的列表
- **并且** 支持使用 `--json` 标志输出 JSON

#### 场景：仅显示需求变更

- **当** 执行 `openspec change show update-error --requirements-only`
- **则** 仅显示需求变更（新增/修改/移除/重命名）
- **并且** 排除原因和变更内容部分

#### 场景：验证变更结构

- **当** 执行 `openspec change validate update-error`
- **则** 解析变更文件
- **并且** 根据 Zod schema 进行验证
- **并且** 确保增量格式正确

### 需求：向后兼容性

系统应保持与现有 `list` 命令的向后兼容性，同时显示弃用通知。

#### 场景：旧版 list 命令

- **当** 执行 `openspec list`
- **则** 显示当前变更列表（现有行为）
- **并且** 显示弃用通知："注意：'openspec list' 已弃用，请改用 'openspec change list'。"

#### 场景：带 --all 标志的旧版 list

- **当** 执行 `openspec list --all`
- **则** 显示所有变更（现有行为）
- **并且** 显示相同的弃用通知
