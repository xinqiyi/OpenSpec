## 新增的需求

### 需求：状态 JSON 提供 planning 上下文

status 命令应为 repository 本地和 workspace 变更提供机器可读的 planning 上下文。

#### 场景：报告 planning 归属
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应标识变更是 repository 本地还是 workspace 范围
- **AND** 应包含 planning 归属根路径和变更根路径

#### 场景：报告具体 artifact 路径
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应包含现有 artifact 的具体路径
- **AND** agent 应能读取这些路径，无需假设 `openspec/changes/<id>/`
- **AND** workspace 范围的嵌套 spec 路径应在不展平区域或能力路径的情况下报告

#### 场景：报告 workspace 受影响区域
- **GIVEN** 变更属于 workspace 范围
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应包含已知的受影响区域
- **AND** 应在无需额外区域清单 artifact 的情况下，指示受影响区域尚未解决

#### 场景：报告后续步骤
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应包含 agent 的后续步骤指导
- **AND** 指导应使用简洁的行动语言

### 需求：状态 JSON 行动上下文

status 命令应暴露行动上下文，使 agent 无需硬编码的文件系统假设即可行动。

#### 场景：planning 行动上下文
- **WHEN** workspace 变更仍处于 planning 阶段
- **THEN** 状态 JSON 应标识 agent 可以读取或更新的 planning artifact
- **AND** 应指示链接的 repository 和文件夹是供探索的上下文

#### 场景：实施行动上下文
- **WHEN** workspace 变更有选定的受影响区域进行实施
- **THEN** 状态 JSON 应包含该区域的允许编辑根路径
- **AND** 应避免授权对选定区域之外的编辑

#### 场景：repository 本地行动上下文
- **GIVEN** 变更是 repository 本地的
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 状态 JSON 应保留现有 artifact 状态行为
- **AND** 应为使用行动上下文的 agent 报告 repository 本地 planning 归属

### 需求：指令使用解析后的 planning 路径

artifact 和应用指令应使用解析后的 planning 路径，而非硬编码的 repository 本地变更路径。

#### 场景：workspace artifact 指令
- **GIVEN** 变更属于 workspace 范围
- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 指令输出应指向 workspace 变更根路径下的 artifact 路径
- **AND** 不应指示 agent 写入链接的 repository，除非有明确的实施上下文允许

#### 场景：repository 本地 artifact 指令
- **GIVEN** 变更是 repository 本地的
- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 指令输出应保留现有的 repository 本地路径

### 需求：workflow skill 使用 CLI artifact 上下文

生成的 workflow skill 应使用 OpenSpec CLI 输出作为 artifact 位置的真实来源。

#### 场景：skill 在 artifact 工作前检查状态
- **WHEN** 生成的 workflow skill 需要检查或创建变更的 artifact 时
- **THEN** 应指示 agent 运行 `openspec status --change <id> --json`
- **AND** 应使用返回的 planning 上下文和 artifact 路径，而非假设 repository 本地变更路径

#### 场景：skill 在写入 artifact 前使用指令
- **WHEN** 生成的 workflow skill 即将创建或更新 artifact 时
- **THEN** 应指示 agent 运行 `openspec instructions <artifact> --change <id> --json`
- **AND** 应写入命令返回的已解析 artifact 路径

#### 场景：skill 避免硬编码的 repository 本地路径
- **WHEN** 生成的 workflow skill 描述 artifact 位置时
- **THEN** 应避免要求变更位于 `openspec/changes/<id>/` 下的硬编码示例
- **AND** 任何示例都应参考 CLI 报告的路径，无论是 repository 本地还是 workspace 范围变更

#### 场景：skill 保护不支持的 workspace workflow
- **GIVEN** 生成的 workflow skill 被全局配置文件选中
- **AND** 该 workflow 在此切片中尚未具备完整的 workspace 范围行为
- **WHEN** 该 skill 用于 workspace 范围变更时
- **THEN** 应告知 agent 该 workspace 操作尚不支持
- **AND** 不应指示 agent 回退到 repository 本地路径或在没有明确允许编辑根路径的情况下编辑链接的 repository

### 需求：workspace schema 指令

workflow 命令应为使用 workspace planning schema 的 workspace 范围变更使用 workspace planning schema 指令。

#### 场景：workspace planning artifact 顺序
- **GIVEN** workspace 范围变更使用 schema `workspace-planning`
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** artifact 列表应反映 workspace planning schema
- **AND** 应包括正常的 proposal、spec、设计和任务 artifact

#### 场景：workspace spec 指令
- **GIVEN** workspace 范围变更使用 schema `workspace-planning`
- **WHEN** 用户请求 spec artifact 的指令时
- **THEN** 指令输出应引导 agent 在 workspace 范围的 `specs/` 路径下组织特定区域的需求
- **AND** 不应要求所有受影响区域都确定后才能继续 planning
- **AND** 不应指示 agent 在变更仍处于 workspace planning 阶段时创建 repository 本地 spec 文件
