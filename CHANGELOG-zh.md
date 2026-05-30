# @fission-ai/openspec

## 1.3.1

### 补丁变更

- [#995](https://github.com/Fission-AI/OpenSpec/pull/995) [`d1f3861`](https://github.com/Fission-AI/OpenSpec/commit/d1f3861d9ec694cc924b042b5da01963dcf93137) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 错误修复

  - **规范化的工件路径** — 工作流工件路径现在通过原生的 `realpath` 解析，因此符号链接和大小写不敏感的文件系统不再导致 apply 和 archive 过程中的路径不匹配。
  - **全局 apply 指令** — 包含全局工件输出的 apply 指令现在能正确解析，并且字面工件输出被强制要求为文件路径。
  - **隐藏的主规范需求** — 嵌套在围栏代码块中或以其他方式隐藏在主要规范中的需求现在在验证期间能被检测到。
  - **干净的 `--json` 输出** — 传递 `--json` 时，进度旋转文本不再泄漏到 stderr，因此合并 stdout 和 stderr 的 AI 代理可以可靠地解析 JSON。
  - **防火墙环境中的静默遥测** — PostHog 网络错误现在以 1 秒超时被吞没，并禁用了重试和远程配置，因此 OpenSpec 在受限网络中不再显示 `PostHogFetchNetworkError`。遥测选择退出的说明已提前在 README、安装指南和 CLI 参考中进行了文档化。

## 1.3.0

### 次要变更

- [#952](https://github.com/Fission-AI/OpenSpec/pull/952) [`cce787e`](https://github.com/Fission-AI/OpenSpec/commit/cce787ec4083da2b27781f6786f5ce0002909a7b) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 新功能

  - **Junie 支持** — 为 JetBrains Junie 添加了工具和命令生成
  - **Lingma IDE 支持** — 为 Lingma IDE 添加了配置支持
  - **ForgeCode 支持** — 为 ForgeCode 添加了工具支持
  - **IBM Bob 支持** — 为 IBM Bob 编程助手添加了支持

  ### 错误修复

  - **Shell 补全选择加入** — 补全安装现在改为选择加入，修复了 PowerShell 编码损坏问题
  - **Copilot 自动检测** — 防止了从空的 `.github/` 目录错误检测 GitHub Copilot
  - **pi.dev 命令生成** — 修复了命令参考转换和模板参数传递

### 补丁变更

- [#760](https://github.com/Fission-AI/OpenSpec/pull/760) [`61eb999`](https://github.com/Fission-AI/OpenSpec/commit/61eb999f7c6c0fc98d2e7f3678756fce6a3f4378) 感谢 [@fsilvaortiz](https://github.com/fsilvaortiz)！ - 修复：OpenCode 适配器现在使用 `.opencode/commands/`（复数形式）以匹配 OpenCode 的官方目录约定。修复 #748。

- [#759](https://github.com/Fission-AI/OpenSpec/pull/759) [`afdca0d`](https://github.com/Fission-AI/OpenSpec/commit/afdca0d5dab1aa109cfd8848b2512333ccad60c3) 感谢 [@fsilvaortiz](https://github.com/fsilvaortiz)！ - 修复：`openspec status` 现在在不存在变更时优雅退出，而不是抛出致命错误。修复 #714。

## 1.2.0

### 次要变更

- [#747](https://github.com/Fission-AI/OpenSpec/pull/747) [`1e94443`](https://github.com/Fission-AI/OpenSpec/commit/1e94443a3551b228eecbc89e95d96d3b9600a192) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 新功能

  - **配置文件系统** — 在 `core`（4 个基本工作流）和 `custom`（选择任意子集）配置文件之间选择，以控制安装哪些技能。使用新的 `openspec config profile` 命令管理配置文件
  - **提议工作流** — 新的单步工作流，从单个请求创建完整的变更提案，包含设计、规范和任务 — 无需分别运行 `new` 再运行 `ff`
  - **AI 工具自动检测** — `openspec init` 现在扫描你的项目以查找现有的工具目录（`.claude/`、`.cursor/` 等）并预选检测到的工具
  - **Pi (pi.dev) 支持** — Pi 编码代理现在是一个支持的工具，具有提示和技能生成功能
  - **Kiro 支持** — AWS Kiro IDE 现在是一个支持的工具，具有提示和技能生成功能
  - **同步会修剪取消选择的工作流** — `openspec update` 现在会移除你取消选择的工作流的命令文件和技能目录，保持项目整洁
  - **配置漂移警告** — 当全局配置与当前项目不同步时，`openspec config list` 会发出警告

  ### 错误修复

  - 修复了 onboard 预检在刚初始化的项目上给出错误的"未初始化"错误
  - 修复了归档工作流在同步过程中中途停止的问题 — 现在同步完成后会正确恢复
  - 为 onboard shell 命令添加了 Windows PowerShell 替代方案

## 1.1.1

### 补丁变更

- [#627](https://github.com/Fission-AI/OpenSpec/pull/627) [`afb73cf`](https://github.com/Fission-AI/OpenSpec/commit/afb73cf9ec59c6f8b26d0c538c0218c203ba3c56) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 错误修复

  - **OpenCode 命令引用** — 生成文件中的命令引用现在使用正确的 `/opsx-` 连字符格式，而不是 `/opsx:` 冒号格式，确保命令在 OpenCode 中正常工作

## 1.1.0

### 次要变更

- [#625](https://github.com/Fission-AI/OpenSpec/pull/625) [`53081fb`](https://github.com/Fission-AI/OpenSpec/commit/53081fb2a26ec66d2950ae0474b9a56cbc5b5a76) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 错误修复

  - **Codex 全局路径支持** — Codex 适配器现在正确解析全局路径，修复了在项目目录外运行时的工��文件生成问题 (#622)
  - **跨设备或受限路径上的归档操作** — 当重命名因 EPERM 或 EXDEV 错误失败时，归档现在回退到复制+删除，修复了网络/外部驱动器上的故障 (#605)
  - **工作流消息中的斜杠命令提示** — 工作流完成消息现在显示有用的斜杠命令提示，指导下一步操作 (#603)
  - **Windsurf 工作流文件路径** — 更新了 Windsurf 适配器以使用正确的 `workflows` 目录，而不是旧的 `commands` 路径 (#610)

### 补丁变更

- [#550](https://github.com/Fission-AI/OpenSpec/pull/550) [`86d2e04`](https://github.com/Fission-AI/OpenSpec/commit/86d2e04cae76a999dbd1b4571f52fa720036be0c) 感谢 [@jerome-benoit](https://github.com/jerome-benoit)！ - ### 改进

  - **Nix flake 维护** — 版本现在从 package.json 动态读取，减少了手动同步问题
  - **Nix 构建优化** — 源过滤排除了 node_modules 和构建产物，提高了构建速度
  - **update-flake.sh 脚本** — 检测哈希已正确时跳过不必要的重建

  ### 其他

  - 将 Nix CI 操作更新到最新版本（nix-installer v21，magic-nix-cache v13）

## 1.0.2

### 补丁变更

- [#596](https://github.com/Fission-AI/OpenSpec/pull/596) [`e91568d`](https://github.com/Fission-AI/OpenSpec/commit/e91568deb948073f3e9d9bb2d2ab5bf8080d6cf4) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 错误修复

  - 澄清了规范命名约定 — 规范应根据功能命名（`specs/<capability>/spec.md`），而非变更
  - 修复了任务复选框格式指南 — 任务现在明确要求使用 `- [ ]` 复选框格式以进行 apply 阶段跟踪

## 1.0.1

### 补丁变更

- [#587](https://github.com/Fission-AI/OpenSpec/pull/587) [`943e0d4`](https://github.com/Fission-AI/OpenSpec/commit/943e0d41026d034de66b9442d1276c01b293eb2b) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 错误修复

  - 修复了入门文档中的错误归档路径 — 模板现在显示正确的路径 `openspec/changes/archive/YYYY-MM-DD-<name>/`，而不是错误的 `openspec/archive/YYYY-MM-DD--<name>/`

## 1.0.0

### 主要变更

- [#578](https://github.com/Fission-AI/OpenSpec/pull/578) [`0cc9d90`](https://github.com/Fission-AI/OpenSpec/commit/0cc9d9025af367faa1688a7b2606a2549053cd3f) 感谢 [@TabishB](https://github.com/TabishB)！ - ## OpenSpec 1.0 — OPSX 版本

  工作流已从头重建。OPSX 用基于动作的系统取代了旧的阶段锁定 `/openspec:*` 命令，AI 能理解哪些工件存在、哪些已准备好创建以及每个动作解锁了什么。

  ### 破坏性变更

  - **旧命令已移除** — `/openspec:proposal`、`/openspec:apply` 和 `/openspec:archive` 不再存在
  - **配置文件已移除** — 工具特定的指令文件（`CLAUDE.md`、`.cursorrules`、`AGENTS.md`、`project.md`）不再生成
  - **迁移** — 运行 `openspec init` 进行升级。旧的工件会被检测到并在确认后清理。

  ### 从静态提示到动态指令

  **之前：** AI 每次收到相同的静态指令，无论项目状态如何。

  **现在：** 指令从三个层次动态组装：

  1. **上下文** — 来自 `config.yaml` 的项目背景（技术栈、约定）
  2. **规则** — 工件特定的约束（例如"为未知事项提议调研任务"）
  3. **模板** — 输出文件的实际结构

  AI 查询 CLI 获取实时状态：哪些工件存在、哪些已准备好创建、哪些依赖已满足，以及每个动作解锁了什么。

  ### 从阶段锁定到基于动作

  **之前：** 线性工作流 — 提案 → apply → 归档。无法轻松返回或迭代。

  **现在：** 针对变更的灵活动作。随时编辑任何工件。工件图自动跟踪状态。

  | 命令                 | 作用                                             |
  | -------------------- | ------------------------------------------------ |
  | `/opsx:explore`      | 在提交变更之前思考想法                            |
  | `/opsx:new`          | 开始一个新的变更                                  |
  | `/opsx:continue`     | 一次创建一个工件（逐步进行）                      |
  | `/opsx:ff`           | 一次性创建所有规划工件（快进）                    |
  | `/opsx:apply`        | 实施任务                                          |
  | `/opsx:verify`       | 验证实施与工件是否匹配                            |
  | `/opsx:sync`         | 将增量规范同步到主规范                            |
  | `/opsx:archive`      | 归档已完成的变更                                  |
  | `/opsx:bulk-archive` | 批量归档多个变更，带冲突检测                      |
  | `/opsx:onboard`      | 引导式 15 分钟完整工作流演练                      |

  ### 从文本合并到语义规范同步

  **之前：** 规范更新需要手动合并或整体文件替换。

  **现在：** 增量规范使用 AI 理解的语义标记：

  - `## ADDED Requirements` — 要添加的新需求
  - `## MODIFIED Requirements` — 部分更新（添加场景而不复制现有场景）
  - `## REMOVED Requirements` — 删除，附有原因和迁移说明
  - `## RENAMED Requirements` — 重命名，保留内容

  归档在需求级别解析这些内容，而不是脆弱的标题匹配。

  ### 从分散的文件到代理技能

  **之前：** 项目根目录下 8 个以上的配置文件 + 分散在 21 个工具特定位置的斜杠命令，格式各异。

  **现在：** 单一的 `.claude/skills/` 目录，包含 YAML 前置元数据的 markdown 文件。可被 Claude Code、Cursor、Windsurf 自动检测。跨编辑器兼容。

  ### 新功能

  - **入门技能** — `/opsx:onboard` 引导新用户完成他们的第一个完整变更，包含代码库感知的任务建议和逐步讲解（11 个阶段，约 15 分钟）

  - **支持 21 种 AI 工具** — Claude Code、Cursor、Windsurf、Continue、Gemini CLI、GitHub Copilot、Amazon Q、Cline、RooCode、Kilo Code、Auggie、CodeBuddy、Qoder、Qwen、CoStrict、Crush、Factory、OpenCode、Antigravity、iFlow 和 Codex

  - **交互式设置** — `openspec init` 显示动画欢迎屏幕和可搜索的多选工具选择界面。预选已配置的工具以便轻松刷新。

  - **可自定义的模式** — 在 `openspec/schemas/` 中定义自定义工件工作流，无需修改包代码。团队可以通过版本控制共享工作流。

  ### 错误修复

  - 修复了命令名称包含冒号时 Claude Code YAML 解析失败的问题
  - 修复了任务文件解析以处理复选框行上的尾随空白
  - 修复了 JSON 指令输出，使上下文/规则与模板分离 — AI 之前将约束块复制到了工件文件中

  ### 文档

  - 新的入门指南、CLI 参考、概念文档
  - 移除了未实现的"飞行中编辑并继续"等误导性声明
  - 添加了从 OPSX 之前版本升级的迁移指南

## 0.23.0

### 次要变更

- [#540](https://github.com/Fission-AI/OpenSpec/pull/540) [`c4cfdc7`](https://github.com/Fission-AI/OpenSpec/commit/c4cfdc7c499daef30d8a218f5f59b8d9e5adb754) 感谢 [@TabishB](https://github.com/TabishB)！ - ### 新功能

  - **批量归档技能** — 使用 `/opsx:bulk-archive` 在单个操作中归档多个已完成的变更。包含批量验证、规范冲突检测和整合确认

  ### 其他

  - **简化设置** — 配置创建现在使用合理的默认值，附有有用的注释，而不是交互式提示

## 0.22.0

### 次要变更

- [#530](https://github.com/Fission-AI/OpenSpec/pull/530) [`33466b1`](https://github.com/Fission-AI/OpenSpec/commit/33466b1e2a6798bdd6d0e19149173585b0612e6f) 感谢 [@TabishB](https://github.com/TabishB)！ - 添加项目级配置、项目本地模式和模式管理命令

  **新功能**

  - **项目级配置** — 通过 `openspec/config.yaml` 配置 OpenSpec 行为，包括自定义规则注入、上下文文件和模式解析设置
  - **项目本地模式** — 在项目的 `openspec/schemas/` 目录中为项目特定工作流定义自定义工件模式
  - **模式管理命令** — 新的 `openspec schema` 命令（`list`、`show`、`export`、`validate`），用于检查和管理工件模式（实验性）

  **错误修复**

  - 修复了项目配置中空 `rules` 字段的配置加载问题

## 0.21.0

### 次要变更

- [#516](https://github.com/Fission-AI/OpenSpec/pull/516) [`b5a8847`](https://github.com/Fission-AI/OpenSpec/commit/b5a884748be6156a7bb140b4941cfec4f20a9fc8) 感谢 [@TabishB](https://github.com/TabishB)！ - 添加反馈命令和 Nix flake 支持

  **新功能**

  - **反馈命令** — 直接从 CLI 使用 `openspec feedback` 提交反馈，创建 GitHub Issues，自动包含元数据，并提供优雅的手动提交降级方案
  - **Nix flake 支持** — 使用新的 `flake.nix` 通过 Nix 安装和开发 openspec，包括自动 flake 维护和 CI 验证

  **错误修复**

  - **探索模式护栏** — 探索模式现在明确阻止实施，保持专注于思考和发现，同时仍允许创建工件

  **其他**

  - 改进了 `opsx apply` 中的变更推断 — 当模糊时，从对话上下文或提示中自动检测目标变更
  - 简化了归档同步评估，提供了更清晰的增量规范位置指导

## 0.20.0

### 次要变更

- [#502](https://github.com/Fission-AI/OpenSpec/pull/502) [`9db74aa`](https://github.com/Fission-AI/OpenSpec/commit/9db74aa5ac6547efadaed795217cfa17444f2004) 感谢 [@TabishB](https://github.com/TabishB)！ - 添加 `/opsx:verify` 命令并修复 vitest 进程风暴

  **新功能**

  - **`/opsx:verify` 命令** — 验证变更实施是否与其规范匹配

  **错误修复**

  - 通过限制工作线程并行度修复了 vitest 进程风暴
  - 修复了代理工作流，使其使用非交互模式进行验证命令
  - 修复了 PowerShell 补全生成器，移除了尾随逗号

## 0.19.0

### 次要变更

- eb152eb: 添加 Continue IDE 支持、shell 补全和 `/opsx:explore` 命令

  **新功能**

  - **Continue IDE 支持** — OpenSpec 现在为 [Continue](https://continue.dev/) 生成斜杠命令，扩展了除 Cursor、Windsurf、Claude Code 等之外的编辑器集成选项
  - **Bash、Fish 和 PowerShell 的 Shell 补全** — 运行 `openspec completion install` 设置在你偏好 shell 中的 Tab 补全
  - **`/opsx:explore` 命令** — 一种新的思考伙伴模式，用于在提交变更之前探索想法和调查问题
  - **Codebuddy 斜杠命令改进** — 更新了前置元数据格式以提高兼容性

  **错误修复**

  - Shell 补全现在在命令有子命令时正确提供父级标志（如 `--help`）
  - 修复了测试中的 Windows 兼容性问题

  **其他**

  - 添加了可选匿名使用统计信息，以帮助了解 OpenSpec 的使用情况。默认为**选择退出** — 设置 `OPENSPEC_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 以禁用。仅收集命令名称和版本；不收集参数、文件路径或内容。在 CI 环境中自动禁用。

## 0.18.0

### 次要变更

- 8dfd824: 添加 OPSX 实验性工作流命令和增强的工件系统

  **新命令：**

  - `/opsx:ff` - 快进创建工件，一次性生成所有需要的工件
  - `/opsx:sync` - 将变更中的增量规范同步到主规范
  - `/opsx:archive` - 归档已完成的变更，带智能同步检查

  **工件工作流增强：**

  - 模式感知的 apply 指令，带有内联指导和 XML 输出
  - 用于实验性工件工作流的代理模式选择
  - 通过 `.openspec.yaml` 文件的每个变更模式元数据
  - 用于实验性工件工作流的代理技能
  - 用于模板加载和变更上下文的指令加载器
  - 重构为带模板的目录结构模式

  **改进：**

  - 增强的 list 命令，带有最后修改时间戳和排序
  - 变更创建工具，以更好地支持工作流

  **修复：**

  - 规范化路径以实现跨平台 glob 兼容性
  - 创建新规范文件时允许 REMOVED 需求

## 0.17.2

### 补丁变更

- 455c65f: 修复 validate 命令中的 `--no-interactive` 标志以正确禁用旋转指示器，防止在 pre-commit 钩子和 CI 环境中挂起

## 0.17.1

### 补丁变更

- a2757e7: 通过使用动态导入 @inquirer/prompts 修复 config 命令中的 pre-commit 钩子挂起问题

  config 命令由于在模块加载时注册了 stdin 事件监听器，导致 pre-commit 钩子无限挂起。此修复将静态导入转换为动态导入，仅在 `config reset` 命令实际交互使用时才加载 inquirer。

  同时添加了 ESLint 规则以防止静态 @inquirer 导入，避免未来出现回归问题。

## 0.17.0

### 次要变更

- 2e71835: 添加 `openspec config` 命令和 Oh-my-zsh 补全

  **新功能**

  - 添加 `openspec config` 命令，用于管理全局配置设置
  - 实现全局配置目录，支持 XDG Base Directory 规范
  - 添加 Oh-my-zsh shell 补全支持，提升 CLI 体验

  **错误修复**

  - 通过使用动态导入修复 pre-commit 钩子中的挂起问题
  - 在所有平台上尊重 XDG_CONFIG_HOME 环境变量
  - 解决 zsh-installer 测试中的 Windows 兼容性问题
  - 使 cli-completion 规范与实现一致
  - 从斜杠命令中移除硬编码的代理字段

  **文档**

  - 将 README 中的 AI 工具列表按字母排序并使其可折叠

## 0.16.0

### 次要变更

- c08fbc1: 添加新的 AI 工具集成和增强功能：

  - **feat(iflow-cli)**: 添加 iFlow-cli 集成，支持斜杠命令和文档
  - **feat(init)**: 在 init 后添加 IDE 重启说明，告知用户斜杠命令可用性
    **feat(antigravity)**: 添加 Antigravity 斜杠命令支持
  - **fix**: 为 Qwen Code 生成 TOML 命令（修复 #293）
  - 澄清脚手架提案文档并增强提案指南
  - 更新提案指南，强调在实施前先进行设计的方法

## 未发布

### 次要变更

- 添加 Continue 斜杠命令支持，使 `openspec init` 可以生成带有 MARKDOWN 前置元数据和 `$ARGUMENTS` 占位符的 `.continue/prompts/openspec-*.prompt` 文件，并在 `openspec update` 时刷新。

- 添加 Antigravity 斜杠命令支持，使 `openspec init` 可以生成带有仅描述前置元数据的 `.agent/workflows/openspec-*.md` 文件，并且 `openspec update` 在 Windsurf 旁边刷新现有工作流。

## 0.15.0

### 次要变更

- 4758c5c: 添加新的 AI 工具支持，原生斜杠命令集成

  - **Gemini CLI**: 为 Gemini CLI 添加原生基于 TOML 的斜杠命令支持，集成 `.gemini/commands/openspec/`
  - **RooCode**: 添加 RooCode 集成，包含配置器、斜杠命令和模板
  - **Cline**: 修复 Cline，使用工作流代替规则来实现斜杠命令（`.clinerules/workflows/` 路径）
  - **文档**: 更新文档以反映新的集成和工作流变更

## 0.14.0

### 次要变更

- 8386b91: 添加新的 AI 助手支持和配置改进

  - feat: 添加 Qwen Code 支持，集成斜杠命令
  - feat: 为 apply 斜杠命令添加 $ARGUMENTS 支持，实现动态变量传递
  - feat: 在配置和文档中添加 Qoder CLI 支持
  - feat: 添加 CoStrict AI 助手支持
  - fix: 在扩展模式下重新创建缺失的 openspec 模板文件
  - fix: 防止工具的错误"已配置"检测
  - fix: 使用变更 ID 作为回退标题，而不是"未命名变更"
  - docs: 添加填充项目级上下文的指导
  - docs: 在 README 中添加 Crush 到支持的 AI 工具列表

## 0.13.0

### 次要变更

- 668a125: 添加多个 AI 助手支持并改进验证

  本次发布增加对多个新的 AI 编程助手支持：

  - CodeBuddy Code - AI 驱动的编程助手
  - CodeRabbit - AI 代码审查助手
  - Cline - Claude 驱动的 CLI 助手
  - Crush AI - AI 助手平台
  - Auggie (Augment CLI) - 代码增强工具

  新功能：

  - 归档斜杠命令现在支持参数，实现更灵活的工作流

  错误修复：

  - 增量规范验证现在处理大小写不敏感的标题并正确检测空部分
  - 归档验证现在正确遵循 --no-validate 标志并忽略元数据

  文档改进：

  - 添加 VS Code 开发容器配置，便于开发设置
  - 更新 AGENTS.md，明确变更 ID 表示法
  - 增强斜杠命令文档，添加重启说明

## 0.12.0

### 次要变更

- 082abb4: 为斜杠命令添加工厂函数支持和非交互式初始化选项

  本次发布包含两个新功能：

  - **斜杠命令的工厂函数支持**：斜杠命令现在可以定义为返回命令对象的函数，实现动态命令配置
  - **非交互式初始化选项**：为 `openspec init` 添加了 `--tools`、`--all-tools` 和 `--skip-tools` CLI 标志，用于 CI/CD 管道中的自动化初始化，同时保持向后兼容交互式模式

## 0.11.0

### 次要变更

- 312e1d6: 添加 Amazon Q Developer CLI 集成。OpenSpec 现在支持 Amazon Q Developer，在 `.amazonq/prompts/` 目录中自动生成提示，允许你在 Amazon Q 的 @-语法中使用 OpenSpec 斜杠命令。

## 0.10.0

### 次要变更

- d7e0ce8: 改进初始化向导的 Enter 键行为，使通过提示的流程更自然

## 0.9.2

### 补丁变更

- 2ae0484: 修复跨平台路径处理问题。本次发布包含针对 joinPath 行为和斜杠命令路径解析的修复，确保 OpenSpec 在所有平台上正确运行。

## 0.9.1

### 补丁变更

- 8210970: 修复选中 Codex 集成时 OpenSpec 在 Windows 上无法工作的问题。本次发布包含跨平台路径处理和规范化的修复，确保 OpenSpec 在 Windows 系统上正确运行。

## 0.9.0

### 次要变更

- efbbf3b: 添加对 Codex 和 GitHub Copilot 斜杠命令的支持，支持 YAML 前置元数据和 $ARGUMENTS

## 未发布

### 次要变更

- 添加 GitHub Copilot 斜杠命令支持。OpenSpec 现在将提示写入 `.github/prompts/openspec-{proposal,apply,archive}.prompt.md`，包含 YAML 前置元数据和 `$ARGUMENTS` 占位符，并在 `openspec update` 时刷新。

## 0.8.1

### 补丁变更

- d070d08: 修复 CLI 版本不匹配问题，添加发布保护，验证打包的 tarball 通过 `openspec --version` 打印的版本与 package.json 相同。

## 0.8.0

### 次要变更

- c29b06d: 添加 Windsurf 支持。
- 添加 Codex 斜杠命令支持。OpenSpec 现在直接将提示写入 Codex 的全局目录（`~/.codex/prompts` 或 `$CODEX_HOME/prompts`），并在 `openspec update` 时刷新。

## 0.7.0

### 次要变更

- 添加原生 Kilo Code 工作流集成，使 `openspec init` 和 `openspec update` 管理 `.kilocode/workflows/openspec-*.md` 文件。
- 始终搭建受管理根目录 `AGENTS.md` 交接存根，并在 init/update 期间重新组织 AI 工具提示，以保持指令一致。

## 0.6.0

### 次要变更

- 将生成的根代理指令精简为受管理的交接存根，并更新 init/update 流程以安全地刷新它。

## 0.5.0

### 次要变更

- feat: 实现阶段 1 端到端测试，包含跨平台 CI 矩阵

  - 在 test/helpers/run-cli.ts 中添加共享的 runCLI 助手，用于 spawn 测试
  - 创建 test/cli-e2e/basic.test.ts，涵盖 help、version、validate 流程
  - 迁移现有的 CLI exec 测试以使用 runCLI 助手
  - 将 CI 矩阵扩展到 bash（Linux/macOS）和 pwsh（Windows）
  - 拆分 PR 和主分支工作流以优化反馈

### 补丁变更

- 使 apply 指令更具体

  改进代理模板和斜杠命令模板，提供更具体和可操作的 apply 指令。

- docs: 改进文档和清理

  - 为 archive 命令记录非交互式标志
  - 替换 README 中的 Discord 徽章
  - 归档已完成的变更以便更好地组织

## 0.4.0

### 次要变更

- 为 CLI 改进和增强用户体验添加 OpenSpec 变更提案
- 添加 Opencode 斜杠命令支持，用于 AI 驱动的开发工作流

### 补丁变更

- 添加文档改进，包括 archive 命令模板的 --yes 标志和 Discord 徽章
- 修复 markdown 解析器中的换行符规范化，以正确处理 CRLF 文件

## 0.3.0

### 次要变更

- 使用扩展模式、多工具选择和交互式 `AGENTS.md` 配置器增强 `openspec init`。

## 0.2.0

### 次要变更

- ce5cead: - 添加 `openspec view` 仪表盘，一览规范计数和变更进度
  - 生成和更新 AI 斜杠命令，同时重命名 `openspec/AGENTS.md` 指令文件
  - 移除已弃用的 `openspec diff` 命令，引导用户使用 `openspec show`

## 0.1.0

### 次要变更

- 24b4866: 初始发布
