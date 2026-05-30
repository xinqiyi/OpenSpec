# cli-artifact-workflow spec

## 目的
定义脚手架化和活跃变更的构件 workflow CLI 行为（`status`、`instructions`、`templates` 和设置流程）。

## 需求
### 需求：状态命令

系统应当显示变更的构件完成状态，包括脚手架化（空）变更。

> **修复了 Bug**：之前通过 `getActiveChangeIds()` 要求 `proposal.md` 必须存在。

#### 场景：显示包含所有状态

- **WHEN** 用户运行 `openspec status --change <id>`
- **THEN** 系统显示每个构件及其状态指示：
 - `[x]` 表示已完成的构件
 - `[ ]` 表示就绪的构件
 - `[-]` 表示被阻塞的构件（列出缺失的依赖）

#### 场景：状态显示完成摘要

- **WHEN** 用户运行 `openspec status --change <id>`
- **THEN** 输出包括完成百分比和计数（例如，"2/4 构件已完成"）

#### 场景：状态 JSON 输出

- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 系统输出 JSON，包含 changeName、schemaName、isComplete 和 artifacts 数组

#### 场景：状态 JSON 包含应用阶段要求

- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 系统输出 JSON，包含：
 - `changeName`、`schemaName`、`isComplete`、`artifacts` 数组
 - `applyRequires`：应用阶段所需的构件 ID 数组

#### 场景：脚手架化变更的状态

- **WHEN** 用户对没有构件的变更运行 `openspec status --change <id>`
- **THEN** 系统显示所有构件及其状态
- **AND** 根构件（无依赖）显示为就绪 `[ ]`
- **AND** 依赖构件显示为被阻塞 `[-]`

#### 场景：缺少 change 参数

- **WHEN** 用户运行 `openspec status` 而不带 `--change`
- **THEN** 系统显示错误，并列出现有的可用变更
- **AND** 包括脚手架化变更（没有 proposal.md 的目录）

#### 场景：未知变更

- **WHEN** 用户运行 `openspec status --change unknown-id`
- **AND** 目录 `openspec/changes/unknown-id/` 不存在
- **THEN** 系统显示错误，列出所有可用的变更目录

### 需求：下一个构件发现

workflow 应当使用 `openspec status` 输出来确定下一步可以创建什么，而不是使用独立的 next-command 接口。

#### 场景：从状态输出中发现下一个构件

- **WHEN** 用户需要知道接下来要创建哪个构件
- **THEN** `openspec status --change <id>` 标识出 `[ ]` 状态的就绪构件
- **AND** 不需要专门的"next command"来继续 workflow

### 需求：指令命令

系统应当输出用于创建构件的增强指令，包括针对脚手架化变更的指令。

#### 场景：显示增强指令

- **WHEN** 用户运行 `openspec instructions <artifact> --change <id>`
- **THEN** 系统输出：
 - 构件元数据（ID、输出路径、描述）
 - template 内容
 - 依赖状态（已完成/缺失）
 - 解锁的构件（完成后可用的内容）

#### 场景：指令 JSON 输出

- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 系统输出符合 ArtifactInstructions 接口的 JSON

#### 场景：未知构件

- **WHEN** 用户运行 `openspec instructions unknown-artifact --change <id>`
- **THEN** 系统显示错误，列出该架构的有效构件 ID

#### 场景：依赖未满足的构件

- **WHEN** 用户请求被阻塞构件的指令
- **THEN** 系统显示指令并附带缺失依赖的警告

#### 场景：脚手架化变更的指令

- **WHEN** 用户对脚手架化变更运行 `openspec instructions proposal --change <id>`
- **THEN** 系统输出用于创建 proposal 的 template 和元数据
- **AND** 不要求已有任何构件存在

### 需求：template 命令
系统应当显示架构中所有构件的已解析 template 路径。

#### 场景：使用默认架构列出 template 路径
- **WHEN** 用户运行 `openspec templates`
- **THEN** 系统使用默认架构显示每个构件及其已解析的 template 路径

#### 场景：使用自定义架构列出 template 路径
- **WHEN** 用户运行 `openspec templates --schema tdd`
- **THEN** 系统显示指定架构的 template 路径

#### 场景：template JSON 输出
- **WHEN** 用户运行 `openspec templates --json`
- **THEN** 系统输出将构件 ID 映射到 template 路径的 JSON

#### 场景：template 解析来源
- **WHEN** 显示 template 路径时
- **THEN** 系统指示每个 template 是来自用户覆盖还是包内置

### 需求：新建变更命令
系统应当创建带有验证的新变更目录。

#### 场景：创建有效变更
- **WHEN** 用户运行 `openspec new change add-feature`
- **THEN** 系统创建 `openspec/changes/add-feature/` 目录

#### 场景：无效变更名称
- **WHEN** 用户使用无效名称运行 `openspec new change "Add Feature"`
- **THEN** 系统显示带有指导的验证错误

#### 场景：重复变更名称
- **WHEN** 用户对已存在的变更运行 `openspec new change existing-change`
- **THEN** 系统显示错误，指示该变更已存在

#### 场景：附带描述创建
- **WHEN** 用户运行 `openspec new change add-feature --description "Add new feature"`
- **THEN** 系统创建变更目录，并在 README.md 中包含描述

### 需求：workspace 设置命令
CLI 构件 workflow 应当在创建变更之前公开 workspace 设置命令。

#### 场景：在变更前准备 workspace planning
- **WHEN** 用户需要跨 repository 或文件夹准备 workspace planning
- **THEN** CLI 应当提供设置、列出、链接、重新链接和诊断 workspace 的命令
- **AND** 这些命令不应要求存在活跃的 workspace 变更

#### 场景：使用简短命令列出 workspace
- **WHEN** 用户需要简洁的 workspace 列表命令
- **THEN** CLI 应当支持 `openspec workspace ls`
- **AND** 其行为应与 `openspec workspace list` 相同

#### 场景：将设置与 agent 启动分开
- **WHEN** 用户完成 workspace 设置
- **THEN** 设置 workflow 应将 agent 启动和 workspace 打开行为留给后面的 workflow
- **AND** 设置不应要求首选 agent 选择

#### 场景：避免公开直接创建
- **WHEN** 用户在首次 workspace 设置流程中创建 workspace
- **THEN** CLI 应使用 `openspec workspace setup`
- **AND** 不应将 `openspec workspace create` 公开为公共创建路径

### 需求：架构选择
系统应当支持 workflow 命令的自定义架构选择。

#### 场景：默认架构
- **WHEN** 用户运行不带 `--schema` 的 workflow 命令
- **THEN** 系统使用 "spec-driven" 架构

#### 场景：自定义架构
- **WHEN** 用户运行 `openspec status --change <id> --schema tdd`
- **THEN** 系统对构件图使用指定的架构

#### 场景：未知架构
- **WHEN** 用户指定未知架构
- **THEN** 系统显示错误列出现有可用架构

### 需求：输出格式
系统应当提供一致的输出格式。

#### 场景：彩色输出
- **WHEN** 终端支持颜色
- **THEN** 状态指示器使用颜色：绿色（已完成）、黄色（就绪）、红色（被阻塞）

#### 场景：无颜色输出
- **WHEN** 使用 `--no-color` 标志或设置了 `NO_COLOR` 环境变量
- **THEN** 输出仅使用文本指示器，不带 ANSI 颜色

#### 场景：进度指示
- **WHEN** 加载变更状态需要时间
- **THEN** 系统在加载期间显示旋转指示器

### 需求：实验性隔离
系统应当以隔离方式实现构件 workflow 命令，以便于移除。

#### 场景：单文件实现
- **WHEN** 实现构件 workflow 功能时
- **THEN** 所有命令位于 `src/commands/artifact-workflow.ts`

#### 场景：帮助文本标记
- **WHEN** 用户在任何构件 workflow 命令上运行 `--help`
- **THEN** 帮助文本指示该命令是实验性的

### 需求：架构应用阶段块

系统应当支持架构定义中的 `apply` 块，用于控制何时以及如何开始实现。

#### 场景：带 apply 块的架构

- **WHEN** 架构定义了 `apply` 块
- **THEN** 系统使用 `apply.requires` 确定在应用阶段之前必须存在哪些构件
- **AND** 使用 `apply.tracks` 标识进度跟踪文件（如果没有则为 null）
- **AND** 使用 `apply.instruction` 作为向 agent 显示的指导

#### 场景：不带 apply 块的架构

- **WHEN** 架构没有 `apply` 块
- **THEN** 系统要求所有构件都存在后才可以进行应用阶段
- **AND** 使用默认指令："所有构件已完成。开始实施。"

### 需求：应用阶段指令命令

系统应当通过 `openspec instructions apply` 生成感知架构的应用阶段指令。

#### 场景：生成应用阶段指令

- **WHEN** 用户运行 `openspec instructions apply --change <id>`
- **AND** 所有必需的构件（根据架构的 `apply.requires`）都存在
- **THEN** 系统输出：
 - `contextFiles`：将构件 ID 映射到所有现有构件的具体路径数组
 - 架构特定的指令文本
 - 进度跟踪文件路径（如果设置了 `apply.tracks`）

#### 场景：因缺少构件而阻塞应用阶段

- **WHEN** 用户运行 `openspec instructions apply --change <id>`
- **AND** 必需的构件缺失
- **THEN** 系统指示应用阶段被阻塞
- **AND** 列出必须先创建的构件

#### 场景：应用阶段指令 JSON 输出

- **WHEN** 用户运行 `openspec instructions apply --change <id> --json`
- **THEN** 系统输出 JSON，包含：
 - `contextFiles`：将构件 ID 映射到现有构件的具体路径数组的对象
 - `instruction`：应用阶段指令文本
 - `tracks`：进度文件路径或 null
 - `applyRequires`：必需的构件 ID 列表

### 需求：工具选择标志

`artifact-experimental-setup` 命令应当接受 `--tool <tool-id>` 标志来指定目标 AI 工具。

#### 场景：通过标志指定工具

- **WHEN** 用户运行 `openspec artifact-experimental-setup --tool cursor`
- **THEN** skill 文件生成在 `.cursor/skills/` 目录下
- **AND** 命令文件使用 Cursor 的 frontmatter 格式生成

#### 场景：缺少工具标志

- **WHEN** 用户运行 `openspec artifact-experimental-setup` 而不带 `--tool`
- **THEN** 系统显示错误，要求提供 `--tool` 标志
- **AND** 在错误消息中列出有效的工具 ID

#### 场景：未知工具 ID

- **WHEN** 用户运行 `openspec artifact-experimental-setup --tool unknown-tool`
- **AND** 该工具 ID 不在 `AI_TOOLS` 中
- **THEN** 系统显示错误列出现有有效的工具 ID

#### 场景：没有 skillsDir 的工具

- **WHEN** 用户指定了一个没有配置 `skillsDir` 的工具
- **THEN** 系统显示错误，指示该工具不支持 skill 生成

#### 场景：没有命令适配器的工具

- **WHEN** 用户指定了一个有 `skillsDir` 但没有注册命令适配器的工具
- **THEN** skill 文件生成成功
- **AND** 命令生成被跳过，并显示信息性消息

### 需求：输出消息

设置命令应当显示关于生成了什么的清晰输出。

#### 场景：在输出中显示目标工具

- **WHEN** 设置命令成功运行
- **THEN** 输出包括目标工具名称（例如，"正在为 Cursor 设置..."）

#### 场景：显示生成的路径

- **WHEN** 设置命令完成
- **THEN** 输出列出所有生成的 skill 文件路径
- **AND** 列出所有生成的命令文件路径（如果适用）

#### 场景：显示跳过的命令消息

- **WHEN** 命令生成因缺少适配器而被跳过
- **THEN** 输出包括消息："命令生成已跳过 - 没有适用于 <tool> 的适配器"

### 需求：状态 JSON 提供 planning 上下文
状态命令应当为 repository 本地和 workspace 变更提供机器可读的 planning 上下文。

#### 场景：报告 planning 根目录
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应当标识变更是 repository 本地还是 workspace 范围
- **AND** 应包括 planning 根目录和变更根目录

#### 场景：报告具体构件路径
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应当包含现有构件的具体路径
- **AND** agent 应当能够读取这些路径，而不假设为 `openspec/changes/<id>/`
- **AND** workspace 范围的嵌套 spec 路径应当在不展平区域或能力路径的情况下报告

#### 场景：报告 workspace 受影响区域
- **GIVEN** 变更是 workspace 范围的
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应当包含已知的受影响区域
- **AND** 应在受影响区域仍未解决时进行指示，而无需额外的区域清单构件

#### 场景：报告下一步
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 输出应当包含给 agent 的下一步指导
- **AND** 指导应使用简洁的操作语言

### 需求：状态 JSON 操作上下文
状态命令应当公开操作上下文，使 agent 无需硬编码的文件系统假设即可行动。

#### 场景：planning 操作上下文
- **WHEN** workspace 变更仍在 planning 中
- **THEN** 状态 JSON 应当标识 agent 可以读取或更新的 planning 构件
- **AND** 应指示链接的 repository 和文件夹是用于探索的上下文

#### 场景：实施操作上下文
- **WHEN** workspace 变更有选定的受影响区域用于实施
- **THEN** 状态 JSON 应当包括该区域的允许编辑根目录
- **AND** 应避免授权对该选定区域之外的编辑

#### 场景：repository 本地操作上下文
- **GIVEN** 变更是 repository 本地的
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 状态 JSON 应当保留现有的构件状态行为
- **AND** 应为使用操作上下文的 agent 报告 repository 本地 planning 根目录

### 需求：指令使用已解析的 planning 路径
构件和应用阶段指令应使用已解析的 planning 路径，而不是硬编码的 repository 本地变更路径。

#### 场景：workspace 构件指令
- **GIVEN** 变更是 workspace 范围的
- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 指令输出应指向 workspace 变更根目录下的构件路径
- **AND** 除非有明确的实施上下文允许，否则不应指示 agent 在链接的 repository 下写入

#### 场景：repository 本地构件指令
- **GIVEN** 变更是 repository 本地的
- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 指令输出应保留现有的 repository 本地路径

### 需求：workflow skill 使用 CLI 构件上下文
生成的 workflow skill 应使用 OpenSpec CLI 输出作为构件位置的唯一真实来源。

#### 场景：skill 在构件工作前检查状态
- **WHEN** 生成的 workflow skill 需要检查或创建变更的构件时
- **THEN** 它应指示 agent 运行 `openspec status --change <id> --json`
- **AND** 应使用返回的 planning 上下文和构件路径，而不是假设 repository 本地变更路径

#### 场景：skill 在写入构件前使用指令
- **WHEN** 生成的 workflow skill 即将创建或更新构件时
- **THEN** 它应指示 agent 运行 `openspec instructions <artifact> --change <id> --json`
- **AND** 应写入命令返回的已解析构件路径

#### 场景：skill 避免硬编码的 repository 本地路径
- **WHEN** 生成的 workflow skill 描述构件位置时
- **THEN** 它们应避免要求变更位于 `openspec/changes/<id>/` 下的硬编码示例
- **AND** 任何示例都应引用 CLI 报告的路径，适用于 repository 本地和 workspace 范围的变更

#### 场景：skill 保护不支持的 workspace workflow
- **GIVEN** 生成的 workflow skill 被全局配置文件选中
- **AND** 该 workflow 在此切片中尚未具有完整的 workspace 范围行为
- **WHEN** 该 skill 用于 workspace 范围的变更时
- **THEN** 它应告知 agent 该 workspace 操作尚不支持
- **AND** 不应指示 agent 回退到 repository 本地路径或在没有明确允许编辑根目录的情况下编辑链接的 repository

### 需求：workspace 架构指令
workflow 命令应对使用 workspace planning 架构的 workspace 范围变更使用 workspace planning 架构指令。

#### 场景：workspace planning 构件顺序
- **GIVEN** workspace 范围变更使用架构 `workspace-planning`
- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 构件列表应反映 workspace planning 架构
- **AND** 应包括正常的 proposal、specs、design 和 tasks 构件

#### 场景：workspace spec 指令
- **GIVEN** workspace 范围变更使用架构 `workspace-planning`
- **WHEN** 用户请求 specs 构件的指令时
- **THEN** 指令输出应指导 agent 在 workspace 范围的 `specs/` 路径下组织特定区域的需求
- **AND** 不应要求所有受影响区域在 planning 继续之前都最终确定
- **AND** 不应指示 agent 在变更仍在 workspace planning 中时创建 repository 本地 spec 文件
