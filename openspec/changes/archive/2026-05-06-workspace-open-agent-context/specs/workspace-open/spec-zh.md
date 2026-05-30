## 新增需求

### 需求：工作区打开命令
OpenSpec 应提供一个 `workspace open` 命令，通过代理或 VS Code 编辑器打开 OpenSpec 工作区工作集。

#### 场景：打开当前工作区
- **GIVEN** 命令在 OpenSpec 工作区内部运行
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应打开当前工作区
- **AND** 它应使用该工作区已选的开启器

#### 场景：打开命名工作区
- **GIVEN** 名为 `platform` 的工作区在本地已知
- **WHEN** 用户运行 `openspec workspace open platform`
- **THEN** OpenSpec 应打开 `platform` 工作区

#### 场景：使用选择标志打开命名工作区
- **GIVEN** 名为 `platform` 的工作区在本地已知
- **WHEN** 用户运行 `openspec workspace open --workspace platform`
- **THEN** OpenSpec 应打开 `platform` 工作区

#### 场景：冲突的工作区选择器
- **GIVEN** 名为 `platform` 和 `checkout` 的工作区在本地已知
- **WHEN** 用户运行 `openspec workspace open platform --workspace checkout`
- **THEN** OpenSpec 应失败并显示清晰的冲突错误
- **AND** 错误应指明两个冲突的选择器

#### 场景：处理不支持的预览和 JSON 标志
- **WHEN** 用户运行带 `--prepare-only` 或 `--json` 的 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误，说明根工作区开放界面支持通过选定的开启器启动
- **AND** 错误应将预览或机器可读上下文需求引导至未来的上下文/查询界面

#### 场景：在工作区规划前处理变更范围打开
- **WHEN** 用户运行 `openspec workspace open --change <id>`
- **THEN** OpenSpec 应失败并显示清晰的错误，说明此切片支持根工作区打开
- **AND** 错误应将变更范围打开行为引导至未来的工作区变更规划

### 需求：打开的工作区选择
OpenSpec 应使用当前工作区上下文、本地注册表状态和交互式选择来解析要打开的工作区。

#### 场景：当前工作区优先
- **GIVEN** 命令从工作区文件夹或其子目录之一运行
- **AND** 未提供工作区名称
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应打开当前工作区

#### 场景：自动选择唯一已知的工作区
- **GIVEN** 命令在工作区外部运行
- **AND** 本地恰好知道一个工作区
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应直接打开该已知工作区

#### 场景：从多个工作区中选择
- **GIVEN** 命令在工作区外部运行
- **AND** 本地已知多个工作区
- **AND** 终端是交互式的
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应显示一个包含工作区名称和位置的选择器
- **AND** 它应打开用户选择的工作区

#### 场景：非交互式模糊选择
- **GIVEN** 命令在工作区外部运行
- **AND** 本地已知多个工作区
- **AND** 终端是非交互式的
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误消息，列出已知的工作区名称
- **AND** 它应要求用户传递工作区名称

#### 场景：没有已知的工作区
- **GIVEN** 命令在工作区外部运行
- **AND** 本地没有已知的工作区
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误消息
- **AND** 它应建议运行 `openspec workspace setup`

### 需求：开启器解析
OpenSpec 应从命令覆盖、工作区本地偏好或交互式提示中解析开启器。

#### 场景：冲突的开启器覆盖
- **WHEN** 用户运行 `openspec workspace open --agent codex --editor`
- **THEN** OpenSpec 应失败并显示清晰的冲突错误，指明 `--agent` 和 `--editor`
- **AND** 它应避免启动任何开启器
- **AND** 它应保持已存储的偏好开启器不变

#### 场景：使用已存储的偏好开启器
- **GIVEN** 工作区有一个机器本地的偏好开启器
- **WHEN** 用户使用默认开启器解析运行 `openspec workspace open`
- **THEN** OpenSpec 应使用已存储的偏好开启器

#### 场景：为单个会话覆盖使用代理
- **GIVEN** 工作区有一个已存储的偏好开启器
- **WHEN** 用户运行 `openspec workspace open --agent codex`
- **THEN** OpenSpec 应在此次打开命令中使用 Codex
- **AND** 它应保持已存储的偏好开启器不变

#### 场景：为单个会话覆盖使用 VS Code 编辑器
- **GIVEN** 工作区有一个已存储的偏好开启器
- **WHEN** 用户运行 `openspec workspace open --editor`
- **THEN** OpenSpec 应在 VS Code 编辑器模式下打开工作区
- **AND** 它应保持已存储的偏好开启器不变

#### 场景：未存储开启器时提示
- **GIVEN** 工作区没有存储的偏好开启器
- **AND** 终端是交互式的
- **WHEN** 用户使用默认开启器解析运行 `openspec workspace open`
- **THEN** OpenSpec 应提示用户选择开启器
- **AND** 它应仅提供检测到可执行文件的开启器

#### 场景：无法提示开启器时失败
- **GIVEN** 工作区没有存储的偏好开启器
- **AND** 终端是交互式的
- **AND** `PATH` 上没有可用的受支持开启器可执行文件
- **WHEN** 用户使用默认开启器解析运行 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误消息，说明没有可用的受支持开启器
- **AND** 它应避免提示无法启动的选项

#### 场景：在非交互模式下未存储开启器时失败
- **GIVEN** 工作区没有存储的偏好开启器
- **AND** 终端是非交互式的
- **WHEN** 用户使用默认开启器解析运行 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误消息
- **AND** 它应要求用户传递 `--agent <tool>` 或 `--editor`

### 需求：开启器启动行为
OpenSpec 应使用现有的工作区文件和链接路径状态启动选定的开启器。

#### 场景：打开 VS Code 编辑器
- **GIVEN** 用户选择了 VS Code 编辑器开启器
- **WHEN** `code` 在 `PATH` 上可用
- **THEN** OpenSpec 应使用 VS Code 打开工作区维护的 `.code-workspace` 文件

#### 场景：在 VS Code 中打开 GitHub Copilot
- **GIVEN** 用户选择了 `--agent github-copilot`
- **WHEN** `code` 在 `PATH` 上可用
- **THEN** OpenSpec 应使用 VS Code 打开工作区维护的 `.code-workspace` 文件
- **AND** 它应将其视为 VS Code Copilot 体验

#### 场景：打开 Codex
- **GIVEN** 用户选择了 `--agent codex`
- **WHEN** `codex` 在 `PATH` 上可用
- **THEN** OpenSpec 应从工作区根目录启动 Codex
- **AND** 它应使用 Codex 支持的目录附加机制，附加每个具有有效本地路径的链接仓库或文件夹

#### 场景：打开 Claude
- **GIVEN** 用户选择了 `--agent claude`
- **WHEN** `claude` 在 `PATH` 上可用
- **THEN** OpenSpec 应从工作区根目录启动 Claude
- **AND** 它应使用 Claude 支持的目录附加机制，附加每个具有有效本地路径的链接仓库或文件夹

#### 场景：缺失开启器可执行文件
- **GIVEN** 选定的开启器需要 `PATH` 上不可用的可执行文件
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误，指明缺失的可执行文件
- **AND** 它应保持选定的开启器作为所需的开启器

#### 场景：缺失 VS Code 可执行文件
- **GIVEN** 选定的开启器是 VS Code 编辑器或 VS Code 中的 GitHub Copilot
- **AND** `code` 在 `PATH` 上不可用
- **WHEN** 用户运行 `openspec workspace open`
- **THEN** OpenSpec 应失败并显示清晰的错误，指明 `code`
- **AND** 它应包含维护的 `.code-workspace` 路径，以便用户可以手动打开它

### 需求：链接工作集可见性
OpenSpec 应在创建变更之前使链接的仓库和文件夹对工作区探索和规划可见。

#### 场景：附加有效的链接路径
- **GIVEN** 工作区具有带有有效本地路径的链接仓库或文件夹
- **WHEN** 用户通过支持链接目录附加的开启器打开工作区
- **THEN** OpenSpec 应将每个有效的链接路径包含在打开的工作集中
- **AND** 它应支持在存在工作区变更之前打开

#### 场景：跳过损坏的链接路径
- **GIVEN** 工作区至少有一个链接路径缺失或未在本地记录
- **WHEN** 用户打开工作区
- **THEN** OpenSpec 应跳过损坏的链接路径
- **AND** 它应报告该路径已被跳过，并以 `openspec workspace doctor` 作为修复路径
- **AND** 当选定的开启器本身可用时，它应继续打开工作区

#### 场景：在仓库本地 OpenSpec 状态缺失时打开链接
- **GIVEN** 链接的仓库或文件夹具有有效的本地路径，但缺少仓库本地的 `openspec/` 状态
- **WHEN** 用户打开工作区
- **THEN** OpenSpec 应在本地路径有效时包含该链接
- **AND** 它应将缺失的仓库本地 OpenSpec 状态视为后续工作流的实现就绪性关注点，同时继续打开操作

### 需求：工作区打开指南
OpenSpec 应使用持久化工作区指南作为根工作区打开的主要上下文来源。

#### 场景：使用现有工作区指南启动
- **GIVEN** 工作区在 `AGENTS.md` 中有 OpenSpec 管理的指南
- **WHEN** 用户打开工作区
- **THEN** OpenSpec 应从当前链接路径状态刷新维护的 `.code-workspace`
- **AND** 它应针对刷新后的工作区文件启动选定的开启器
- **AND** 它应使用持久化工作区文件作为主要的工作区打开工件

#### 场景：最小必需启动提示
- **GIVEN** 开启器需要初始提示参数
- **WHEN** OpenSpec 启动该开启器
- **THEN** OpenSpec 应使用最小提示，例如 `Open this OpenSpec workspace.`
- **AND** 持久化工作区规则应保留在工作区文件中
