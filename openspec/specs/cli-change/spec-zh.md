# cli-change 规范

## 目的

定义 `openspec change` 命令用于显示、列出和验证变更提案及增量的行为。

## 需求

### 需求：变更命令

系统应提供 `change` 命令，包含用于显示、列出和验证变更提案的子命令。

#### 场景：以 JSON 格式显示变更

- **当** 执行 `openspec change show update-error --json`
- **则** 解析 Markdown 变更文件
- **并且** 提取变更结构和增量
- **并且** 向 stdout 输出有效的 JSON

#### 场景：列出所有变更

- **当** 执行 `openspec change list`
- **则** 扫描 openspec/changes 目录
- **并且** 返回所有待处理变更的列表
- **并且** 支持使用 `--json` 标志输出 JSON

#### 场景：仅显示需求变更

- **当** 执行 `openspec change show update-error --requirements-only`
- **则** 仅显示需求变更（新增/已修改/已删除/已重命名）
- **并且** 排除原因和变更内容章节

#### 场景：验证变更结构

- **当** 执行 `openspec change validate update-error`
- **则** 解析变更文件
- **并且** 根据 Zod 模式进行验证
- **并且** 确保增量格式正确

### 需求：遗留兼容性

系统应在显示弃用通知的同时，保持与现有 `list` 命令的向后兼容性。

#### 场景：遗留 list 命令

- **当** 执行 `openspec list`
- **则** 显示当前变更列表（现有行为）
- **并且** 显示弃用通知："注意：'openspec list' 已弃用。请改用 'openspec change list'。"

#### 场景：带 --all 标志的遗留 list

- **当** 执行 `openspec list --all`
- **则** 显示所有变更（现有行为）
- **并且** 显示相同的弃用通知

### 需求：交互式显示选择

change show 命令应在未提供变更名称时支持交互式选择。

#### 场景：用于 show 的交互式变更选择

- **当** 执行 `openspec change show` 不带参数
- **则** 显示可用变更的交互式列表
- **并且** 允许用户选择要显示的变更
- **并且** 显示所选变更的内容
- **并且** 保留所有现有的 show 选项（--json、--deltas-only）

#### 场景：非交互式回退保持当前行为

- **给定** 标准输入不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **当** 执行 `openspec change show` 不带变更名称
- **则** 不进行交互式提示
- **并且** 打印包含可用变更 ID 的现有提示
- **并且** 设置 `process.exitCode = 1`

### 需求：交互式验证选择

change validate 命令应在未提供变更名称时支持交互式选择。

#### 场景：用于验证的交互式变更选择

- **当** 执行 `openspec change validate` 不带参数
- **则** 显示可用变更的交互式列表
- **并且** 允许用户选择要验证的变更
- **并且** 验证所选变更

#### 场景：非交互式回退保持当前行为

- **给定** 标准输入不是 TTY，或提供了 `--no-interactive`，或环境变量 `OPEN_SPEC_INTERACTIVE=0`
- **当** 执行 `openspec change validate` 不带变更名称
- **则** 不进行交互式提示
- **并且** 打印包含可用变更 ID 的现有提示
- **并且** 设置 `process.exitCode = 1`
