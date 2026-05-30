## 新增需求

### 需求：变更命令

系统应提供一个 `change` 命令，包含用于显示、列出和验证变更 proposal 的子命令。

#### 场景：以 JSON 格式显示变更

- **WHEN** 执行 `openspec change show update-error --json`
- **THEN** 解析 markdown 变更文件
- **AND** 提取变更结构和 delta
- **AND** 输出有效的 JSON 到标准输出

#### 场景：列出所有变更

- **WHEN** 执行 `openspec change list`
- **THEN** 扫描 openspec/changes 目录
- **AND** 返回所有待处理变更的列表
- **AND** 支持使用 `--json` 标志输出 JSON

#### 场景：仅显示需求变更

- **WHEN** 执行 `openspec change show update-error --requirements-only`
- **THEN** 仅显示需求变更（新增/修改/移除/重命名）
- **AND** 排除原因和变更内容部分

#### 场景：验证变更结构

- **WHEN** 执行 `openspec change validate update-error`
- **THEN** 解析变更文件
- **AND** 根据 Zod schema 进行验证
- **AND** 确保 delta 格式正确

### 需求：向后兼容性

系统应保持与现有 `list` 命令的向后兼容性，同时显示弃用通知。

#### 场景：旧版 list 命令

- **WHEN** 执行 `openspec list`
- **THEN** 显示当前变更列表（现有行为）
- **AND** 显示弃用通知："注意：'openspec list' 已弃用，请改用 'openspec change list'。"

#### 场景：带 --all 标志的旧版 list

- **WHEN** 执行 `openspec list --all`
- **THEN** 显示所有变更（现有行为）
- **AND** 显示相同的弃用通知
