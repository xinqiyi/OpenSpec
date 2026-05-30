## 新增需求

### 需求：workspace 首选开启器状态
当用户明确选择时，OpenSpec 应将 workspace 的首选开启器存储在机器本地 workspace 状态中。

#### 场景：记录交互式设置开启器选择
- **WHEN** 交互式用户在 `openspec workspace setup` 期间选择首选开启器
- **THEN** OpenSpec 应将开启器记录在 `.openspec-workspace/local.yaml` 中
- **AND** 存储的值应使用包含 `kind` 和 `id` 的结构化 `preferred_opener` 对象

#### 场景：记录非交互式设置开启器选择
- **WHEN** 非交互式用户运行 `openspec workspace setup --no-interactive --opener codex`
- **THEN** OpenSpec 应将 `preferred_opener.kind` 记录为 `agent`
- **AND** 应将 `preferred_opener.id` 记录为 `codex`

#### 场景：在非交互式设置中保持开启器未设置
- **WHEN** 非交互式用户运行 `openspec workspace setup --no-interactive` 且未指定开启器选择
- **THEN** OpenSpec 应保持 workspace 首选开启器未设置
- **AND** 未设置状态应允许后续通过 `workspace open` 进行提示

#### 场景：支持的首选开启器值
- **WHEN** OpenSpec 接受首选开启器值时
- **THEN** 应接受 `codex`、`claude`、`github-copilot` 和 `editor`
- **AND** 应将 `editor` 映射到 `kind: editor` 和 `id: vscode`
- **AND** 应将 agent 值映射到 `kind: agent` 和对应的 agent `id`

#### 场景：设置开启器选择的排序
- **WHEN** 交互式设置显示开启器选择时
- **THEN** OpenSpec 应显示所有支持的开启器
- **AND** 应将检测到可执行文件的开启器排在前，不可用的开启器排在后
- **AND** 不可用的开启器应保持可见并附上可用性说明

### 需求：维护的 workspace 开放表面
OpenSpec 应维护使 workspace 在设置和链接更改后可直接打开的文件。

#### 场景：在设置期间创建开放表面
- **WHEN** `openspec workspace setup` 创建 workspace 时
- **THEN** OpenSpec 应创建或刷新 `AGENTS.md`
- **AND** 应创建或刷新 `<workspace-name>.code-workspace`
- **AND** 应为机器本地开放文件创建或刷新 workspace 忽略规则

#### 场景：在链接后刷新开放表面
- **WHEN** `openspec workspace link` 成功时
- **THEN** OpenSpec 应刷新 `AGENTS.md`
- **AND** 应刷新 `<workspace-name>.code-workspace`
- **AND** 应为机器本地开放文件刷新 workspace 忽略规则

#### 场景：在重新链接后刷新开放表面
- **WHEN** `openspec workspace relink` 成功时
- **THEN** OpenSpec 应刷新 `AGENTS.md`
- **AND** 应刷新 `<workspace-name>.code-workspace`
- **AND** 应为机器本地开放文件刷新 workspace 忽略规则

#### 场景：构建 VS Code workspace 文件
- **WHEN** OpenSpec 刷新 `<workspace-name>.code-workspace` 时
- **THEN** 该文件应包含 workspace 根目录
- **AND** workspace 根文件夹条目应使用根路径，不添加合成显示名称
- **AND** 应包含每个具有有效本地路径的已链接 repository 或文件夹
- **AND** 应省略本地路径缺失或无效的已链接 repository 或文件夹

#### 场景：忽略维护的 VS Code workspace 文件
- **WHEN** OpenSpec 刷新 workspace 忽略规则时
- **THEN** 应忽略特定的维护 `<workspace-name>.code-workspace` 文件
- **AND** 用户编写的 `*.code-workspace` 文件仍应可被跟踪

#### 场景：保留用户编写的 AGENTS 内容
- **GIVEN** `AGENTS.md` 包含 OpenSpec workspace 指导标记之外的内容
- **WHEN** OpenSpec 刷新 workspace 指导时
- **THEN** 应仅替换标记的 OpenSpec workspace 指导块
- **AND** 应保留标记之外的内容

#### 场景：在标记缺失时追加 AGENTS 指导
- **GIVEN** `AGENTS.md` 存在且缺少 OpenSpec workspace 指导标记
- **WHEN** OpenSpec 刷新 workspace 指导时
- **THEN** 应追加标记的 OpenSpec workspace 指导块
- **AND** 应保留现有文件内容
