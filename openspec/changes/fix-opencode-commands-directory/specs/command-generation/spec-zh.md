## 修改后的需求

### 需求：ToolCommandAdapter 接口

系统应定义 `ToolCommandAdapter` 接口，用于按工具格式化。

#### 场景：适配器接口结构

- **WHEN** 实现工具适配器时
- **THEN** `ToolCommandAdapter` 应要求：
 - `toolId`：与 `AIToolOption.value` 匹配的字符串标识符
 - `getFilePath(commandId: string)`：返回命令的文件路径（相对于项目根目录，或对于全局范围工具（如 Codex）为绝对路径）
 - `formatFile(content: CommandContent)`：返回带有 frontmatter 的完整文件内容

#### 场景：Claude 适配器格式化

- **WHEN** 为 Claude Code 格式化命令时
- **THEN** 适配器应输出包含 `name`、`description`、`category`、`tags` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.claude/commands/opsx/<id>.md`

#### 场景：Cursor 适配器格式化

- **WHEN** 为 Cursor 格式化命令时
- **THEN** 适配器应输出包含 `name`（作为 `/opsx-<id>`）、`id`、`category`、`description` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.cursor/commands/opsx-<id>.md`

#### 场景：Windsurf 适配器格式化

- **WHEN** 为 Windsurf 格式化命令时
- **THEN** 适配器应输出包含 `name`、`description`、`category`、`tags` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.windsurf/workflows/opsx-<id>.md`

#### 场景：OpenCode 适配器格式化

- **WHEN** 为 OpenCode 格式化命令时
- **THEN** 适配器应输出包含 `description` 字段的 YAML frontmatter
- **AND** 文件路径应遵循 schema `.opencode/commands/opsx-<id>.md`，使用 `path.join('.opencode', 'commands', ...)` 以实现跨平台兼容性
- **AND** 适配器应将基于冒号的命令引用（`/opsx:name`）在主体中转换为基于连字符的格式（`/opsx-name`）

## 新增需求

### 需求：重命名的 OpenCode 命令目录的旧版清理

旧版清理模块应检测并从之前的单数 `.opencode/command/` 目录路径中移除旧的 OpenCode 命令文件。

#### 场景：检测旧的单数路径 OpenCode 命令文件

- **WHEN** 在项目上运行旧版 artifact 检测时，发现匹配 `.opencode/command/opsx-*.md` 或 `.opencode/command/openspec-*.md` 的文件
- **THEN** 系统应通过 `LEGACY_SLASH_COMMAND_PATHS` 将这些文件包含在旧版斜杠命令文件列表中
- **AND** `LegacySlashCommandPattern.pattern` 应接受 `string | string[]` 以支持每个工具的多个 glob schema

#### 场景：在 init 时清理旧的 OpenCode 命令文件

- **WHEN** 用户在包含旧 `.opencode/command/` artifact 的项目上运行 `openspec init`
- **THEN** 系统应移除旧文件
- **AND** 在 `.opencode/commands/` 生成新的命令文件

#### 场景：在非交互式 schema 下自动清理旧版 artifact

- **WHEN** 用户在非交互式 schema（例如 CI）下运行 `openspec init` 且检测到旧版 artifact
- **THEN** 系统应自动清理旧版 artifact，无需 `--force`
- **AND** 旧版斜杠命令文件（100% OpenSpec 管理）应被移除
- **AND** 配置文件清理应仅移除 OpenSpec 标记（永不删除用户文件）
