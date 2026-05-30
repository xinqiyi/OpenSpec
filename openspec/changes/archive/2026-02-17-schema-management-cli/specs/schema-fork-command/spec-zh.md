## 新增需求

### 需求：Schema fork 复制现有模式
CLI 应提供 `openspec schema fork <source> [name]` 命令，将现有模式复制到项目的 `openspec/schemas/` 目录。

#### 场景：使用显式名称进行 Fork
- **当** 用户运行 `openspec schema fork spec-driven my-custom`
- **那么** 系统使用解析顺序（项目 → 用户 → 包）定位 `spec-driven` 模式
- **并且** 将所有文件复制到 `openspec/schemas/my-custom/`
- **并且** 将 `schema.yaml` 中的 `name` 字段更新为 `my-custom`
- **并且** 显示包含源路径和目标路径的成功消息

#### 场景：使用默认名称进行 Fork
- **当** 用户运行 `openspec schema fork spec-driven` 而未指定名称
- **那么** 系统复制到 `openspec/schemas/spec-driven-custom/`
- **并且** 将 `schema.yaml` 中的 `name` 字段更新为 `spec-driven-custom`

#### 场景：源模式未找到
- **当** 用户运行 `openspec schema fork nonexistent`
- **那么** 系统显示未找到模式的错误
- **并且** 列出可用的模式
- **并且** 以非零退出码退出

### 需求：Schema fork 防止意外覆盖
当目标模式已存在时，CLI 应要求确认或 `--force` 标志。

#### 场景：目标存在而未使用 force
- **当** 用户运行 `openspec schema fork spec-driven my-custom` 且 `openspec/schemas/my-custom/` 已存在
- **那么** 系统显示目标已存在的错误
- **并且** 建议使用 `--force` 覆盖
- **并且** 以非零退出码退出

#### 场景：目标存在且使用 force 标志
- **当** 用户运行 `openspec schema fork spec-driven my-custom --force` 且目标已存在
- **那么** 系统移除现有的目标目录
- **并且** 将源模式复制到目标
- **并且** 显示成功消息

#### 场景：覆盖的交互式确认
- **当** 用户在交互式模式下运行 `openspec schema fork spec-driven my-custom` 且目标已存在
- **那么** 系统提示确认覆盖
- **并且** 根据用户响应继续操作

### 需求：Schema fork 保留所有模式文件
CLI 应复制完整的模式目录，包括模板、配置和任何其他文件。

#### 场景：复制包含模板文件
- **当** 用户 fork 一个包含模板文件（例如 `proposal.md`、`design.md`）的模式
- **那么** 所有模板文件都被复制到目标
- **并且** 模板文件内容保持不变

#### 场景：复制包含嵌套目录
- **当** 用户 fork 一个包含嵌套目录（例如 `templates/specs/`）的模式
- **那么** 嵌套目录结构被保留
- **并且** 所有嵌套文件都被复制

### 需求：Schema fork 输出 JSON 格式
CLI 应支持 `--json` 标志用于机器可读输出。

#### 场景：成功时的 JSON 输出
- **当** 用户运行 `openspec schema fork spec-driven my-custom --json`
- **那么** 系统输出包含 `forked: true`、`source`、`destination` 和 `sourcePath` 字段的 JSON

#### 场景：JSON 输出显示源位置
- **当** 用户运行 `openspec schema fork spec-driven --json`
- **那么** JSON 输出包含 `sourceLocation` 字段，指示"project"、"user"或"package"
