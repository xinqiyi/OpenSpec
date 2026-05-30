## 新增的需求

### 需求：workspace 设置安装 agent skill
OpenSpec 应允许用户在 workspace 设置期间将 OpenSpec agent skill 安装到 workspace 中。

#### 场景：提示选择 workspace agent skill
- **WHEN** 交互式 workspace 设置到达 agent skill 安装步骤
- **THEN** OpenSpec 应询问哪些 agent 应在此 workspace 获得 OpenSpec skill
- **AND** 提示应使用 agent skill 语言而非"AI 工具"语言

#### 场景：预选首选开启器
- **GIVEN** 用户选择了支持 OpenSpec skill 生成的首选开启器
- **WHEN** 交互式 workspace 设置询问哪些 agent 应获得 skill
- **THEN** OpenSpec 应预选匹配的 agent
- **AND** 用户应能够选择其他 agent 或取消选择预选的 agent

#### 场景：安装选中的 workspace skill
- **WHEN** workspace 设置完成且选中了一个或多个 agent
- **THEN** OpenSpec 应为每个选中的 agent 在 workspace 根目录生成或刷新 OpenSpec skill 文件
- **AND** 它应报告哪些 agent 获得了 skill
- **AND** 它应将选中的 agent 存储在 workspace 本地机器状态中

#### 场景：安装 profile 选择的 workflow
- **GIVEN** 全局配置解析为 workflow profile
- **WHEN** workspace 设置安装 agent skill
- **THEN** OpenSpec 应为该 profile 选择的 workflow 安装 workspace 本地 skill
- **AND** 它应将 `--tools` 视为 agent 选择，而非 workflow 选择
- **AND** 它应记录最后应用的 workflow ID 用于漂移检测

#### 场景：设置期间仅安装 skill
- **WHEN** workspace 设置安装 agent skill
- **THEN** OpenSpec 应仅生成 skill 文件
- **AND** 它不应生成斜杠命令文件或全局命令文件作为 workspace 设置的一部分

#### 场景：workspace 设置忽略命令交付
- **GIVEN** 全局配置交付为 `commands` 或 `both`
- **WHEN** workspace 设置安装 agent skill
- **THEN** OpenSpec 仍应仅生成 workspace 本地 skill
- **AND** 它应报告 workspace 命令生成不是此切片的一部分

#### 场景：在 skill 安装期间保留链接的 repository
- **WHEN** workspace 设置安装 agent skill
- **THEN** OpenSpec 应保持链接的 repository 和文件夹不变
- **AND** 生成的 skill 应限定在 workspace planning 目录范围内

#### 场景：非交互式设置工具选择
- **WHEN** 非交互式 workspace 设置收到 `--tools all`、`--tools none` 或 `--tools <ids>`
- **THEN** OpenSpec 应使用选中的工具集进行 workspace agent skill 安装
- **AND** 它应使用与 repository 初始化 skill 生成相同的受支持工具 ID 验证工具 ID

#### 场景：非交互式设置无工具选择
- **WHEN** 非交互式 workspace 设置省略 `--tools`
- **THEN** OpenSpec 应在不安装 agent skill 的情况下创建 workspace
- **AND** 它应报告未安装 workspace skill
- **AND** 它应告知用户稍后运行 `openspec workspace update --tools <ids>` 来安装 skill

#### 场景：在 JSON 输出中报告设置 skill
- **WHEN** 非交互式 workspace 设置安装 agent skill 且 JSON 输出已启用
- **THEN** OpenSpec 应在机器可读输出中包含已生成、已刷新、已跳过或失败的 skill 安装结果

### 需求：workspace 更新管理 agent skill
OpenSpec 应提供一个 workspace 更新流程，用于在设置后刷新 agent skill。

#### 场景：更新当前 workspace
- **GIVEN** 命令从 OpenSpec workspace 内部运行
- **WHEN** 用户运行 `openspec workspace update`
- **THEN** OpenSpec 应更新该当前 workspace

#### 场景：更新命名的 workspace
- **GIVEN** 名为 `platform` 的 workspace 在本地已知
- **WHEN** 用户运行 `openspec workspace update platform`
- **THEN** OpenSpec 应更新 `platform` workspace

#### 场景：通过标志更新 workspace
- **GIVEN** 名为 `platform` 的 workspace 在本地已知
- **WHEN** 用户运行 `openspec workspace update --workspace platform`
- **THEN** OpenSpec 应更新 `platform` workspace

#### 场景：更新选中的 workspace skill
- **WHEN** workspace 更新完成且选中了 agent
- **THEN** OpenSpec 应为选中的 agent 刷新 OpenSpec skill
- **AND** 它应为新选中的 agent 添加 skill
- **AND** 它应移除不再选中的 agent 的 OpenSpec 管理 workflow skill 目录
- **AND** 它应更新存储的 workspace 本地选中 agent 列表

#### 场景：更新 profile 选择的 workflow
- **GIVEN** 全局配置解析为 workflow profile
- **WHEN** workspace 更新刷新 workspace 本地 skill
- **THEN** OpenSpec 应将 workspace 本地 skill workflow 集同步到该 profile 选择的 workflow
- **AND** 仅当它们是已知的 OpenSpec 管理 workflow skill 目录时，才应移除取消选择的 workflow skill 目录
- **AND** 它应更新用于漂移检测的最后应用的 workflow ID

#### 场景：workspace 更新忽略命令交付
- **GIVEN** 全局配置交付为 `commands` 或 `both`
- **WHEN** workspace 更新刷新 workspace 本地 skill
- **THEN** OpenSpec 仍应仅更新 workspace 本地 skill
- **AND** 它不应生成斜杠命令文件或全局命令文件

#### 场景：仅移除受管理的 skill 目录
- **WHEN** workspace 更新为未选中的 agent 移除 skill
- **THEN** OpenSpec 应仅移除已知的 OpenSpec 管理 workflow skill 目录
- **AND** 它应保留 agent 目录中的不相关文件

#### 场景：通过标志更新存储的 agent 选择
- **WHEN** workspace 更新收到 `--tools <ids>` 或 `--tools none`
- **THEN** OpenSpec 应将存储的 workspace 本地选中 agent 列表替换为该选择
- **AND** 未来不带 `--tools` 的 workspace 更新应使用存储的选择

#### 场景：非交互式更新工具选择
- **WHEN** workspace 更新收到 `--tools all`、`--tools none` 或 `--tools <ids>`
- **THEN** OpenSpec 应使用该选中的工具集更新 workspace agent skill
- **AND** 它应避免提示 agent 选择

#### 场景：非交互式更新无工具选择
- **GIVEN** workspace 本地选中的 agent 已存储
- **WHEN** 非交互式 workspace 更新省略 `--tools`
- **THEN** OpenSpec 应使用活跃的全局 profile 刷新存储的选中 agent
- **AND** 它应避免提示 agent 选择

#### 场景：非交互式更新无存储的选择
- **GIVEN** 未存储 workspace 本地选中的 agent
- **WHEN** 非交互式 workspace 更新省略 `--tools`
- **THEN** OpenSpec 应在不安装 agent skill 的情况下完成
- **AND** 它应报告无操作，并指导传递 `--tools`

#### 场景：报告 workspace skill 漂移
- **GIVEN** workspace 本地 skill 状态记录了最后应用的 workflow ID
- **AND** 活跃的全局 profile 解析为不同的 workflow 集
- **WHEN** OpenSpec 报告 workspace skill 状态
- **THEN** 它应报告 workspace 本地 skill 与全局 profile 不同步
- **AND** 它应建议 `openspec workspace update`

#### 场景：报告 workspace skill 同步正常
- **GIVEN** workspace 本地 skill 状态与活跃的全局 profile 和选中的 agent 匹配
- **WHEN** OpenSpec 报告 workspace skill 状态
- **THEN** 它不应报告 profile 漂移

#### 场景：报告 workspace skill 更新结果
- **WHEN** workspace 更新更改 agent skill 状态
- **THEN** OpenSpec 应报告哪些 agent 被刷新、添加、移除、跳过或失败

#### 场景：在 JSON 输出中报告 workspace 更新结果
- **WHEN** workspace 更新使用 JSON 输出运行
- **THEN** OpenSpec 应在机器可读输出中包含已刷新、已添加、已移除、已跳过或失败的 skill 结果

### 需求：workspace skill 更新表面已记录
OpenSpec 应在面向用户的命令表面中暴露 workspace skill 设置/更新行为。

#### 场景：workspace 更新出现在帮助中
- **WHEN** 用户运行 `openspec workspace --help`
- **THEN** OpenSpec 应列出 `workspace update`
- **AND** 它应将其描述为刷新 workspace 本地 agent skill

#### 场景：workspace 更新选项出现在帮助中
- **WHEN** 用户运行 `openspec workspace update --help`
- **THEN** OpenSpec 应记录 workspace 选择选项
- **AND** 它应记录 `--tools all|none|<ids>`
- **AND** 它应说明全局 profile 选择 workflow 而 `--tools` 选择 agent

#### 场景：workspace 更新出现在补全中
- **WHEN** 生成 shell 补全时
- **THEN** workspace 命令注册表应包含 `workspace update`
- **AND** 它应包含相关选项，如 `--workspace`、`--tools`、`--json` 和 `--no-interactive`
