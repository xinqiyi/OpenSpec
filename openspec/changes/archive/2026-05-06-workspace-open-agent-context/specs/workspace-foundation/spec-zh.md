## 新增需求

### 需求：工作区首选开启器状态
当用户明确选择时，OpenSpec 应将工作区的首选开启器存储在机器本地工作区状态中。

#### 场景：记录交互式设置开启器选择
- **当** 交互式用户在 `openspec workspace setup` 期间选择首选开启器
- **那么** OpenSpec 应将开启器记录在 `.openspec-workspace/local.yaml` 中
- **并且** 存储的值应使用包含 `kind` 和 `id` 的结构化 `preferred_opener` 对象

#### 场景：记录非交互式设置开启器选择
- **当** 非交互式用户运行 `openspec workspace setup --no-interactive --opener codex`
- **那么** OpenSpec 应将 `preferred_opener.kind` 记录为 `agent`
- **并且** 应将 `preferred_opener.id` 记录为 `codex`

#### 场景：在非交互式设置中保持开启器未设置
- **当** 非交互式用户运行 `openspec workspace setup --no-interactive` 且未指定开启器选择
- **那么** OpenSpec 应保持工作区首选开启器未设置
- **并且** 未设置状态应允许后续通过 `workspace open` 进行提示

#### 场景：支持的首选开启器值
- **当** OpenSpec 接受首选开启器值时
- **那么** 应接受 `codex`、`claude`、`github-copilot` 和 `editor`
- **并且** 应将 `editor` 映射到 `kind: editor` 和 `id: vscode`
- **并且** 应将 agent 值映射到 `kind: agent` 和对应的 agent `id`

#### 场景：设置开启器选择的排序
- **当** 交互式设置显示开启器选择时
- **那么** OpenSpec 应显示所有支持的开启器
- **并且** 应将检测到可执行文件的开启器排在前，不可用的开启器排在后
- **并且** 不可用的开启器应保持可见并附上可用性说明

### 需求：维护的工作区开放表面
OpenSpec 应维护使工作区在设置和链接更改后可直接打开的文件。

#### 场景：在设置期间创建开放表面
- **当** `openspec workspace setup` 创建工作区时
- **那么** OpenSpec 应创建或刷新 `AGENTS.md`
- **并且** 应创建或刷新 `<workspace-name>.code-workspace`
- **并且** 应为机器本地开放文件创建或刷新工作区忽略规则

#### 场景：在链接后刷新开放表面
- **当** `openspec workspace link` 成功时
- **那么** OpenSpec 应刷新 `AGENTS.md`
- **并且** 应刷新 `<workspace-name>.code-workspace`
- **并且** 应为机器本地开放文件刷新工作区忽略规则

#### 场景：在重新链接后刷新开放表面
- **当** `openspec workspace relink` 成功时
- **那么** OpenSpec 应刷新 `AGENTS.md`
- **并且** 应刷新 `<workspace-name>.code-workspace`
- **并且** 应为机器本地开放文件刷新工作区忽略规则

#### 场景：构建 VS Code 工作区文件
- **当** OpenSpec 刷新 `<workspace-name>.code-workspace` 时
- **那么** 该文件应包含工作区根目录
- **并且** 工作区根文件夹条目应使用根路径，不添加合成显示名称
- **并且** 应包含每个具有有效本地路径的已链接仓库或文件夹
- **并且** 应省略本地路径缺失或无效的已链接仓库或文件夹

#### 场景：忽略维护的 VS Code 工作区文件
- **当** OpenSpec 刷新工作区忽略规则时
- **那么** 应忽略特定的维护 `<workspace-name>.code-workspace` 文件
- **并且** 用户编写的 `*.code-workspace` 文件仍应可被跟踪

#### 场景：保留用户编写的 AGENTS 内容
- **给定** `AGENTS.md` 包含 OpenSpec 工作区指导标记之外的内容
- **当** OpenSpec 刷新工作区指导时
- **那么** 应仅替换标记的 OpenSpec 工作区指导块
- **并且** 应保留标记之外的内容

#### 场景：在标记缺失时追加 AGENTS 指导
- **给定** `AGENTS.md` 存在且缺少 OpenSpec 工作区指导标记
- **当** OpenSpec 刷新工作区指导时
- **那么** 应追加标记的 OpenSpec 工作区指导块
- **并且** 应保留现有文件内容
