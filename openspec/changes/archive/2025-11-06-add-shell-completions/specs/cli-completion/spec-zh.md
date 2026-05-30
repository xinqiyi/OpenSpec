# CLI 补全规范

## 目的

`openspec completion` 命令应为所有 OpenSpec CLI 命令、标志和动态值（变更 ID、规范 ID）提供 shell 补全功能，支持 Zsh（包括 Oh My Zsh），并具有可扩展的架构，为未来的 shell（bash、fish、PowerShell）做好准备。补全系统应与 Zsh 的原生补全行为集成，而不是尝试自定义用户体验。

## ADDED Requirements

### Requirement: 原生 Shell 行为集成

补全系统应尊重并与 Zsh 的原生补全模式和用户交互模型集成。

#### Scenario: Zsh 原生补全

- **WHEN** 生成 Zsh 补全脚本时
- **THEN** 使用 Zsh 补全系统，包含 `_arguments`、`_describe` 和 `compadd`
- **AND** 补全应在单次 TAB 键时触发（标准 Zsh 行为）
- **AND** 显示为交互式菜单，用户通过 TAB/方向键导航
- **AND** 自动支持 Oh My Zsh 的增强菜单样式

#### Scenario: 无自定义 UX 模式

- **WHEN** 实现 Zsh 补全时
- **THEN** 不要尝试自定义补全触发行为
- **AND** 不要覆盖 Zsh 特定的导航模式
- **AND** 确保补全对有经验的 Zsh 用户感觉原生

### Requirement: 命令结构

补全命令应遵循子命令模式，用于生成和管理补全脚本。

#### Scenario: 可用子命令

- **WHEN** 用户执行 `openspec completion --help`
- **THEN** 显示可用的子命令：
  - `zsh` - 生成 Zsh 补全脚本
  - `install [shell]` - 为 Zsh 安装补全（自动检测或需要显式指定 shell）
  - `uninstall [shell]` - 移除 Zsh 补全（自动检测或需要显式指定 shell）

### Requirement: Shell 检测

补全系统应自动检测用户当前的 shell 环境。

#### Scenario: 从环境检测 Zsh

- **WHEN** 未显式指定 shell 时
- **THEN** 读取 `$SHELL` 环境变量
- **AND** 从路径中提取 shell 名称（例如 `/bin/zsh` → `zsh`）
- **AND** 验证 shell 是否为 `zsh`
- **AND** 如果 shell 不是 `zsh`，则抛出错误，提示目前仅支持 Zsh

#### Scenario: 检测到非 Zsh shell

- **WHEN** shell 路径指示 bash、fish、powershell 或其他非 Zsh shell
- **THEN** 抛出错误："Shell '<name>' 暂不支持。当前支持：zsh"

### Requirement: 补全生成

补全命令应按需生成 Zsh 补全脚本。

#### Scenario: 生成 Zsh 补全

- **WHEN** 用户执行 `openspec completion zsh`
- **THEN** 将完整的 Zsh 补全脚本输出到 stdout
- **AND** 包含所有命令的补全：init、list、show、validate、archive、view、update、change、spec、completion
- **AND** 包含所有命令特定的标志和选项
- **AND** 使用 Zsh 的 `_arguments` 和 `_describe` 内置函数
- **AND** 支持变更和规范 ID 的动态补全

### Requirement: 动态补全

补全系统应为项目特定值提供上下文感知的动态补全。

#### Scenario: 补全变更 ID

- **WHEN** 补全接受变更名称的命令（show、validate、archive）的参数时
- **THEN** 从 `openspec/changes/` 目录发现活跃变更
- **AND** 排除 `openspec/changes/archive/` 中的已归档变更
- **AND** 返回变更 ID 作为补全建议
- **AND** 仅在 OpenSpec 启用的项目内提供建议

#### Scenario: 补全规范 ID

- **WHEN** 补全接受规范名称的命令（show、validate）的参数时
- **THEN** 从 `openspec/specs/` 目录发现规范
- **AND** 返回规范 ID 作为补全建议
- **AND** 仅在 OpenSpec 启用的项目内提供建议

#### Scenario: 补全缓存

- **WHEN** 请求动态补全时
- **THEN** 将发现的变更和规范 ID 缓存 2 秒
- **AND** 在缓存窗口内对后续请求重用缓存值
- **AND** 过期后自动刷新缓存

#### Scenario: 项目检测

- **WHEN** 用户在 OpenSpec 项目外请求补全时
- **THEN** 跳过动态变更/规范 ID 补全
- **AND** 仅建议静态命令和标志

### Requirement: 安装自动化

补全命令应自动将补全脚本安装到 shell 配置文件中。

#### Scenario: 为 Oh My Zsh 安装

- **WHEN** 用户执行 `openspec completion install zsh`
- **THEN** 通过检查 `$ZSH` 环境变量或 `~/.oh-my-zsh/` 目录检测是否安装了 Oh My Zsh
- **AND** 在 `~/.oh-my-zsh/custom/completions/` 创建自定义补全目录（如果不存在）
- **AND** 将补全脚本写入 `~/.oh-my-zsh/custom/completions/_openspec`
- **AND** 如有需要，通过更新 `~/.zshrc` 确保 `~/.oh-my-zsh/custom/completions` 在 `$fpath` 中
- **AND** 显示成功消息，提示运行 `exec zsh` 或重启终端

#### Scenario: 为标准 Zsh 安装

- **WHEN** 用户执行 `openspec completion install zsh` 且未检测到 Oh My Zsh
- **THEN** 在 `~/.zsh/completions/` 创建补全目录（如果不存在）
- **AND** 将补全脚本写入 `~/.zsh/completions/_openspec`
- **AND** 如果尚未存在，添加 `fpath=(~/.zsh/completions $fpath)` 到 `~/.zshrc`
- **AND** 如果尚未存在，添加 `autoload -Uz compinit && compinit` 到 `~/.zshrc`
- **AND** 显示成功消息，提示运行 `exec zsh` 或重启终端

#### Scenario: 自动检测 Zsh 以进行安装

- **WHEN** 用户执行 `openspec completion install` 而未指定 shell
- **THEN** 使用 shell 检测逻辑检测当前 shell
- **AND** 如果检测到 Zsh，则安装补全
- **AND** 如果检测到的 shell 不是 Zsh，则抛出错误
- **AND** 显示检测到的 shell

#### Scenario: 已安装

- **WHEN** 目标 shell 的补全已安装时
- **THEN** 显示消息表示补全已安装
- **AND** 提供通过覆盖现有文件重新安装/更新的选项
- **AND** 以退出码 0 退出

### Requirement: 卸载

补全命令应移除已安装的补全脚本和配置。

#### Scenario: 卸载 Oh My Zsh 补全

- **WHEN** 用户执行 `openspec completion uninstall zsh`
- **THEN** 如果检测到 Oh My Zsh，移除 `~/.oh-my-zsh/custom/completions/_openspec`
- **AND** 如果检测到标准 Zsh 设置，移除 `~/.zsh/completions/_openspec`
- **AND** 可选地从 `~/.zshrc` 移除 fpath 修改（需确认）
- **AND** 显示成功消息

#### Scenario: 自动检测 Zsh 以进行卸载

- **WHEN** 用户执行 `openspec completion uninstall` 而未指定 shell
- **THEN** 检测当前 shell 并卸载补全（如果 shell 是 Zsh）
- **AND** 如果检测到的 shell 不是 Zsh，则抛出错误

#### Scenario: 未安装

- **WHEN** 尝试卸载未安装的补全时
- **THEN** 显示消息表示补全未安装
- **AND** 以退出码 0 退出

### Requirement: 架构模式

补全实现应遵循清洁架构原则和 TypeScript 最佳实践。

#### Scenario: Shell 特定生成器

- **WHEN** 实现补全生成器时
- **THEN** 为 Zsh 创建 `ZshCompletionGenerator` 类
- **AND** 实现公共 `CompletionGenerator` 接口，包含方法：
  - `generate(): string` - 返回完整的 shell 脚本
  - `getInstallPath(): string` - 返回目标安装路径
  - `getConfigFile(): string` - 返回 shell 配置文件路径
- **AND** 将接口设计为可扩展，以支持未来的 shell（bash、fish、powershell）

#### Scenario: 动态补全提供者

- **WHEN** 实现动态补全时
- **THEN** 创建封装项目发现逻辑的 `CompletionProvider` 类
- **AND** 实现方法：
  - `getChangeIds(): Promise<string[]>` - 发现活跃变更 ID
  - `getSpecIds(): Promise<string[]>` - 发现规范 ID
  - `isOpenSpecProject(): boolean` - 检查当前目录是否启用了 OpenSpec
- **AND** 使用类属性实现 2 秒 TTL 的缓存

#### Scenario: 命令注册表

- **WHEN** 定义可补全的命令时
- **THEN** 创建集中的 `CommandDefinition` 类型，包含属性：
  - `name: string` - 命令名称
  - `description: string` - 帮助文本
  - `flags: FlagDefinition[]` - 可用标志
  - `acceptsChangeId: boolean` - 命令是否接受变更 ID 参数
  - `acceptsSpecId: boolean` - 命令是否接受规范 ID 参数
  - `subcommands?: CommandDefinition[]` - 嵌套子命令
- **AND** 导出包含所有命令定义的 `COMMAND_REGISTRY` 常量
- **AND** 生成器使用此注册表以确保一致性

#### Scenario: 类型安全的 shell 检测

- **WHEN** 实现 shell 检测时
- **THEN** 将 `SupportedShell` 类型定义为字面量类型：`'zsh'`
- **AND** 实现返回 'zsh' 或抛出错误的 `detectShell()` 函数
- **AND** 将类型设计为可扩展（例如，未来：`'bash' | 'zsh' | 'fish' | 'powershell'`）

### Requirement: 错误处理

补全命令应为常见的失败场景提供清晰的错误消息。

#### Scenario: 不支持的 shell

- **WHEN** 用户请求不支持的 shell 的补全（bash、fish、powershell 等）
- **THEN** 显示错误消息："Shell '<name>' 暂不支持。当前支持：zsh"
- **AND** 以退出码 1 退出

#### Scenario: 安装过程中权限错误

- **WHEN** 由于文件权限问题导致安装失败
- **THEN** 显示清晰的错误消息，指出权限问题
- **AND** 建议使用适当的权限或替代安装方法
- **AND** 以退出码 1 退出

#### Scenario: 缺少 shell 配置目录

- **WHEN** 预期的 shell 配置目录不存在
- **THEN** 自动创建目录（附带用户通知）
- **AND** 继续安装

#### Scenario: 未检测到 shell

- **WHEN** `openspec completion install` 无法检测当前 shell 或检测到非 Zsh shell
- **THEN** 显示错误："无法检测到 Zsh。请显式指定：openspec completion install zsh"
- **AND** 以退出码 1 退出

### Requirement: 输出格式

补全命令应提供机器可解析和人类可读的输出。

#### Scenario: 脚本生成输出

- **WHEN** 将补全脚本生成到 stdout 时
- **THEN** 仅输出补全脚本内容（无额外消息）
- **AND** 允许重定向到文件：`openspec completion zsh > /path/to/_openspec`

#### Scenario: 安装成功输出

- **WHEN** 安装成功完成时
- **THEN** 显示格式化的成功消息，包含：
  - 勾选标记指示符
  - 安装位置
  - 后续步骤（shell 重载说明）
- **AND** 在终端支持时使用颜色（除非设置了 `--no-color`）

#### Scenario: 详细安装输出

- **WHEN** 用户在安装期间提供 `--verbose` 标志
- **THEN** 显示详细步骤：
  - Shell 检测结果
  - 目标文件路径
  - 配置修改
  - 文件创建确认

### Requirement: 测试支持

补全实现应可通过单元测试和集成测试进行测试。

#### Scenario: 模拟 shell 环境

- **WHEN** 为 shell 检测编写测试时
- **THEN** 允许覆盖 `$SHELL` 环境变量
- **AND** 对文件系统操作使用依赖注入

#### Scenario: 生成器输出验证

- **WHEN** 测试补全生成器时
- **THEN** 验证生成的脚本包含预期模式
- **AND** 测试命令注册表是否被正确消费
- **AND** 确保动态补全占位符存在

#### Scenario: 安装模拟

- **WHEN** 测试安装逻辑时
- **THEN** 使用临时测试目录而非实际主目录
- **AND** 验证文件创建而不修改真实的 shell 配置
- **AND** 独立测试路径解析逻辑

## 不在范围内

以下 shell 在此提案中**在架构上已记录但未实现**。它们将在未来的提案中添加：

- **Bash 补全** - 将使用 bash-completion 框架，包含 `_init_completion`、`compgen` 和 `COMPREPLY`
- **Fish 补全** - 将使用 Fish 的声明式 `complete -c` 语法
- **PowerShell 补全** - 将使用 `Register-ArgumentCompleter` 和补全结果对象

基于插件的架构（CompletionGenerator 接口、命令注册表、动态提供者）旨在使后续变更中轻松添加这些 shell。

## 为什么

Shell 补全对于专业的 CLI 工具至关重要，通过减少日常工作中的摩擦、错误和认知负担，显著提升开发者体验。
