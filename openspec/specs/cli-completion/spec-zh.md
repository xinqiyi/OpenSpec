# cli-completion 规范

## 目的
为 OpenSpec CLI 提供 shell 补全脚本，实现在多种 shell 中对命令、标志和动态值（变更 ID、规范 ID）的 Tab 补全。支持 Zsh、Bash、Fish 和 PowerShell。
## 需求
### 需求：原生 Shell 行为集成

补全系统应尊重并集成每个受支持 shell 的原生补全模式和用户交互模型。

#### 场景：Zsh 原生补全

- **当** 生成 Zsh 补全脚本时
- **那么** 使用 Zsh 补全系统，配合 `_arguments`、`_describe` 和 `compadd`
- **并且** 补全应在单次 TAB 上触发（标准 Zsh 行为）
- **并且** 显示为交互式菜单，用户可用 TAB/方向键导航
- **并且** 自动支持 Oh My Zsh 的增强菜单样式

#### 场景：Bash 原生补全

- **当** 生成 Bash 补全脚本时
- **那么** 使用 Bash 补全，配合 `complete` 内置命令和 `COMPREPLY` 数组
- **并且** 补全应在双击 TAB 上触发（标准 Bash 行为）
- **并且** 显示为空格分隔列表或列格式
- **并且** 同时支持 bash-completion v1 和 v2 模式

#### 场景：Fish 原生补全

- **当** 生成 Fish 补全脚本时
- **那么** 使用 Fish 的 `complete` 命令配合条件
- **并且** 补全应在单次 TAB 上触发，带有自动建议预览
- **并且** 使用 Fish 的原生着色和描述对齐显示
- **并且** 自动利用 Fish 的内置缓存

#### 场景：PowerShell 原生补全

- **当** 生成 PowerShell 补全脚本时
- **那么** 使用 `Register-ArgumentCompleter` 配合脚本块
- **并且** 补全应在 TAB 上触发，具有循环行为
- **并且** 使用 PowerShell 的原生补全 UI 显示
- **并且** 同时支持 Windows PowerShell 5.1 和 PowerShell Core 7+

#### 场景：无自定义 UX 模式

- **当** 为任何 shell 实现补全时
- **那么** 不要尝试自定义补全触发行为
- **并且** 不要覆盖特定于 shell 的导航模式
- **并且** 确保补全对该 shell 的有经验用户来说感觉原生

### 需求：命令结构

补全命令应遵循子命令模式，用于生成和管理补全脚本。

#### 场景：可用的子命令

- **当** 用户执行 `openspec completion --help`
- **那么** 显示可用的子命令：
  - `generate [shell]` - 为某个 shell 生成补全脚本（输出到 stdout）
  - `install [shell]` - 为 Zsh 安装补全（自动检测或需要显式 shell）
  - `uninstall [shell]` - 移除 Zsh 的补全（自动检测或需要显式 shell）

### 需求：Shell 检测

补全系统应自动检测用户的当前 shell 环境。

#### 场景：从环境检测 Zsh

- **当** 未显式指定 shell 时
- **那么** 读取 `$SHELL` 环境变量
- **并且** 从路径中提取 shell 名称（例如 `/bin/zsh` → `zsh`）
- **并且** 验证 shell 是以下之一：`zsh`、`bash`、`fish`、`powershell`
- **并且** 如果 shell 不受支持则抛出错误

#### 场景：从环境检测 Bash

- **当** `$SHELL` 路径中包含 `bash`
- **那么** 将 shell 检测为 `bash`
- **并且** 继续进行 bash 特定的补全逻辑

#### 场景：从环境检测 Fish

- **当** `$SHELL` 路径中包含 `fish`
- **那么** 将 shell 检测为 `fish`
- **并且** 继续进行 fish 特定的补全逻辑

#### 场景：从环境检测 PowerShell

- **当** `$PSModulePath` 环境变量存在
- **那么** 将 shell 检测为 `powershell`
- **并且** 继续进行 PowerShell 特定的补全逻辑

#### 场景：检测到不受支持的 shell

- **当** shell 路径指示不受支持的 shell
- **那么** 抛出错误："Shell '<name>' 不受支持。支持的 shell：zsh、bash、fish、powershell"

### 需求：补全生成

补全命令应按需为所有受支持的 shell 生成补全脚本。

#### 场景：生成 Zsh 补全

- **当** 用户执行 `openspec completion generate zsh`
- **那么** 将完整的 Zsh 补全脚本输出到 stdout
- **并且** 包含所有命令的补全：init、list、show、validate、archive、view、update、change、spec、completion
- **并且** 包含所有命令特定的标志和选项
- **并且** 使用 Zsh 的 `_arguments` 和 `_describe` 内置函数
- **并且** 支持变更和规范 ID 的动态补全

#### 场景：生成 Bash 补全

- **当** 用户执行 `openspec completion generate bash`
- **那么** 将完整的 Bash 补全脚本输出到 stdout
- **并且** 包含所有命令和子命令的补全
- **并且** 使用 `complete -F` 配合自定义补全函数
- **并且** 用适当的建议填充 `COMPREPLY`
- **并且** 通过 `openspec __complete` 支持变更和规范 ID 的动态补全

#### 场景：生成 Fish 补全

- **当** 用户执行 `openspec completion generate fish`
- **那么** 将完整的 Fish 补全脚本输出到 stdout
- **并且** 使用 `complete -c openspec` 配合条件
- **并且** 包含带有 `--condition` 谓词的命令特定补全
- **并且** 通过 `openspec __complete` 支持变更和规范 ID 的动态补全
- **并且** 为每个补全选项包含描述

#### 场景：生成 PowerShell 补全

- **当** 用户执行 `openspec completion generate powershell`
- **那么** 将完整的 PowerShell 补全脚本输出到 stdout
- **并且** 使用 `Register-ArgumentCompleter -CommandName openspec`
- **并且** 实现处理命令上下文的脚本块
- **并且** 通过 `openspec __complete` 支持变更和规范 ID 的动态补全
- **并且** 返回 `[System.Management.Automation.CompletionResult]` 对象

### 需求：动态补全

补全系统应为项目特定值提供上下文感知的动态补全。

#### 场景：补全变更 ID

- **当** 补全接受变更名称的命令的参数（show、validate、archive）
- **那么** 从 `openspec/changes/` 目录发现活动的变更
- **并且** 排除 `openspec/changes/archive/` 中的已归档变更
- **并且** 将变更 ID 作为补全建议返回
- **并且** 仅在 OpenSpec 启用的项目内部时才提供建议

#### 场景：补全规范 ID

- **当** 补全接受规范名称的命令的参数（show、validate）
- **那么** 从 `openspec/specs/` 目录发现规范
- **并且** 将规范 ID 作为补全建议返回
- **并且** 仅在 OpenSpec 启用的项目内部时才提供建议

#### 场景：补全缓存

- **当** 请求动态补全时
- **那么** 将发现的变更和规范 ID 缓存 2 秒
- **并且** 在缓存窗口内对后续请求重用缓存值
- **并且** 在过期后自动刷新缓存

#### 场景：项目检测

- **当** 用户在 OpenSpec 项目外部请求补全
- **那么** 跳过动态变更/规范 ID 补全
- **并且** 仅建议静态命令和标志

### 需求：安装自动化

补全命令应自动将补全脚本安装到所有受支持 shell 的配置文件中。

#### 场景：为 Oh My Zsh 安装

- **当** 用户执行 `openspec completion install zsh`
- **那么** 通过检查 `$ZSH` 环境变量或 `~/.oh-my-zsh/` 目录检测是否安装了 Oh My Zsh
- **并且** 如果不存在，在 `~/.oh-my-zsh/custom/completions/` 创建自定义补全目录
- **并且** 将补全脚本写入 `~/.oh-my-zsh/custom/completions/_openspec`
- **并且** 确保 `~/.oh-my-zsh/custom/completions` 在 `$fpath` 中，必要时更新 `~/.zshrc`
- **并且** 显示成功消息，并提示运行 `exec zsh` 或重启终端

#### 场景：为标准 Zsh 安装

- **当** 用户执行 `openspec completion install zsh` 且未检测到 Oh My Zsh
- **那么** 如果不存在，在 `~/.zsh/completions/` 创建补全目录
- **并且** 将补全脚本写入 `~/.zsh/completions/_openspec`
- **并且** 如果 `~/.zshrc` 中尚未存在，添加 `fpath=(~/.zsh/completions $fpath)`
- **并且** 如果 `~/.zshrc` 中尚未存在，添加 `autoload -Uz compinit && compinit`
- **并且** 显示成功消息，并提示运行 `exec zsh` 或重启终端

#### 场景：为带有 bash-completion 的 Bash 安装

- **当** 用户执行 `openspec completion install bash`
- **那么** 通过检查 `/usr/share/bash-completion` 或 `/etc/bash_completion.d` 检测是否安装了 bash-completion
- **并且** 如果 bash-completion 可用，写入 `/etc/bash_completion.d/openspec`（需 sudo）或 `~/.local/share/bash-completion/completions/openspec`
- **并且** 如果 bash-completion 不可用，写入 `~/.bash_completion.d/openspec` 并从 `~/.bashrc` 引用
- **并且** 使用基于标记的更新，在必要时向 `~/.bashrc` 添加引用行
- **并且** 显示成功消息，并提示运行 `exec bash` 或重启终端

#### 场景：为 Fish 安装

- **当** 用户执行 `openspec completion install fish`
- **那么** 如果不存在，在 `~/.config/fish/completions/` 创建 Fish 补全目录
- **并且** 将补全脚本写入 `~/.config/fish/completions/openspec.fish`
- **并且** Fish 会自动从此目录加载补全（无需修改配置文件）
- **并且** 显示成功消息，表明补全立即可用

#### 场景：为 PowerShell 安装

- **当** 用户执行 `openspec completion install powershell`
- **那么** 通过 `$PROFILE` 环境变量或默认路径检测 PowerShell 配置文件位置
- **并且** 如果不存在，创建配置文件目录
- **并且** 使用基于标记的更新向配置文件添加补全脚本导入
- **并且** 将补全脚本写入 PowerShell 模块目录或与配置文件同目录
- **并且** 显示成功消息，并提示重启 PowerShell 或运行 `. $PROFILE`

#### 场景：自动检测 shell 进行安装

- **当** 用户执行 `openspec completion install` 而未指定 shell
- **那么** 使用 shell 检测逻辑检测当前 shell
- **并且** 为检测到的 shell（zsh、bash、fish 或 powershell）安装补全
- **并且** 显示检测到哪个 shell

#### 场景：已安装

- **当** 目标 shell 的补全已安装
- **那么** 显示消息指示补全已安装
- **并且** 提供通过覆盖现有文件进行重新安装/更新的选项
- **并且** 以退出码 0 退出

### 需求：卸载

补全命令应移除所有受支持 shell 的已安装补全脚本和配置。

#### 场景：卸载 Zsh 补全

- **当** 用户执行 `openspec completion uninstall zsh`
- **那么** 在继续前提示确认（除非提供了 `--yes` 标志）
- **并且** 如果用户拒绝，取消卸载并显示"卸载已取消。"
- **并且** 如果用户确认，如果检测到 Oh My Zsh，移除 `~/.oh-my-zsh/custom/completions/_openspec`
- **并且** 如果检测到标准 Zsh 设置，移除 `~/.zsh/completions/_openspec`
- **并且** 使用基于标记的移除从 `~/.zshrc` 中移除 fpath 修改
- **并且** 显示成功消息

#### 场景：卸载 Bash 补全

- **当** 用户执行 `openspec completion uninstall bash`
- **那么** 提示确认（除非提供了 `--yes` 标志）
- **并且** 如果用户确认，从 bash-completion 目录或 `~/.bash_completion.d/` 移除补全文件
- **并且** 使用基于标记的移除从 `~/.bashrc` 中移除引用行
- **并且** 显示成功消息

#### 场景：卸载 Fish 补全

- **当** 用户执行 `openspec completion uninstall fish`
- **那么** 提示确认（除非提供了 `--yes` 标志）
- **并且** 如果用户确认，移除 `~/.config/fish/completions/openspec.fish`
- **并且** 显示成功消息（无需修改配置文件）

#### 场景：卸载 PowerShell 补全

- **当** 用户执行 `openspec completion uninstall powershell`
- **那么** 提示确认（除非提供了 `--yes` 标志）
- **并且** 如果用户确认，使用基于标记的移除从 PowerShell 配置文件中移除补全导入
- **并且** 移除补全脚本文件
- **并且** 显示成功消息

#### 场景：自动检测 shell 进行卸载

- **当** 用户执行 `openspec completion uninstall` 而未指定 shell
- **那么** 检测当前 shell 并卸载该 shell 的补全

#### 场景：未安装

- **当** 尝试卸载未安装的补全
- **那么** 显示错误消息，指示补全未安装
- **并且** 以退出码 1 退出

### 需求：架构模式

补全实现应遵循清晰的架构原则和 TypeScript 最佳实践，通过基于插件的模式支持多种 shell。

#### 场景：特定于 shell 的生成器

- **当** 实现补全生成器时
- **那么** 为每个 shell 创建生成器类：`ZshGenerator`、`BashGenerator`、`FishGenerator`、`PowerShellGenerator`
- **并且** 实现一个公共的 `CompletionGenerator` 接口，包含方法：
  - `generate(commands: CommandDefinition[]): string` - 返回完整的 shell 脚本
- **并且** 每个生成器处理特定于 shell 的语法、转义和模式
- **并且** 所有生成器消费来自命令注册表的相同 `CommandDefinition[]`

#### 场景：特定于 shell 的安装器

- **当** 实现补全安装器时
- **那么** 为每个 shell 创建安装器类：`ZshInstaller`、`BashInstaller`、`FishInstaller`、`PowerShellInstaller`
- **并且** 实现一个公共的 `CompletionInstaller` 接口，包含方法：
  - `install(script: string): Promise<InstallationResult>` - 安装补全脚本
  - `uninstall(): Promise<{ success: boolean; message: string }>` - 移除补全
- **并且** 每个安装器处理特定于 shell 的路径、配置文件和安装模式

#### 场景：用于 shell 选择的工厂模式

- **当** 选择特定于 shell 的实现时
- **那么** 使用 `CompletionFactory` 类，包含静态方法：
  - `createGenerator(shell: SupportedShell): CompletionGenerator`
  - `createInstaller(shell: SupportedShell): CompletionInstaller`
- **并且** 工厂使用带有 TypeScript 完备性检查的 switch 语句
- **并且** 添加新 shell 需要更新 `SupportedShell` 类型和工厂分支

#### 场景：动态补全提供者

- **当** 实现动态补全时
- **那么** 创建一个封装项目发现逻辑的 `CompletionProvider` 类
- **并且** 实现方法：
  - `getChangeIds(): Promise<string[]>` - 发现活动变更 ID
  - `getSpecIds(): Promise<string[]>` - 发现规范 ID
  - `isOpenSpecProject(): boolean` - 检查当前目录是否为 OpenSpec 启用
- **并且** 使用类属性实现具有 2 秒 TTL 的缓存

#### 场景：命令注册表

- **当** 定义可补全的命令时
- **那么** 创建一个集中的 `CommandDefinition` 类型，包含属性：
  - `name: string` - 命令名称
  - `description: string` - 帮助文本
  - `flags: FlagDefinition[]` - 可用的标志
  - `acceptsPositional: boolean` - 命令是否接受位置参数
  - `positionalType: string` - 位置参数的类型（change-id、spec-id、path、shell）
  - `subcommands?: CommandDefinition[]` - 嵌套的子命令
- **并且** 导出包含所有命令定义的 `COMMAND_REGISTRY` 常量
- **并且** 所有生成器消费此注册表以确保跨 shell 的一致性

#### 场景：类型安全的 shell 检测

- **当** 实现 shell 检测时
- **那么** 将 `SupportedShell` 类型定义为字面量类型：`'zsh' | 'bash' | 'fish' | 'powershell'`
- **并且** 在 `src/utils/shell-detection.ts` 中实现 `detectShell()` 函数
- **并且** 返回检测到的 shell 或抛出错误并列出受支持的 shell

### 需求：错误处理

补全命令应为常见失败场景提供清晰的错误消息。

#### 场景：不受支持的 shell

- **当** 用户请求不受支持的 shell 的补全时（例如 ksh、csh、tcsh）
- **那么** 显示错误消息："Shell '<name>' 尚不支持。当前支持：zsh、bash、fish、powershell"
- **并且** 以退出码 1 退出

#### 场景：安装过程中的权限错误

- **当** 因文件权限问题导致安装失败
- **那么** 显示清晰的错误消息，指示权限问题
- **并且** 建议使用适当的权限或替代安装方法
- **并且** 以退出码 1 退出

#### 场景：缺少 shell 配置目录

- **当** 预期的 shell 配置目录不存在
- **那么** 自动创建该目录（并通知用户）
- **并且** 继续进行安装

#### 场景：未检测到 shell

- **当** `openspec completion install` 无法检测当前 shell
- **那么** 显示错误："无法自动检测 shell。请显式指定 shell。"
- **并且** 显示使用提示："用法：openspec completion <操作> [shell]"
- **并且** 以退出码 1 退出

### 需求：输出格式

补全命令应提供机器可解析和人类可读的输出。

#### 场景：脚本生成输出

- **当** 将补全脚本生成到 stdout
- **那么** 仅输出补全脚本内容（无额外消息）
- **并且** 允许重定向到文件：`openspec completion generate zsh > /path/to/_openspec`

#### 场景：安装成功输出

- **当** 安装成功完成
- **那么** 显示格式化成功消息，包含：
  - 勾选标记指示符
  - 安装位置
  - 后续步骤（shell 重新加载说明）
- **并且** 当终端支持时使用颜色（除非设置了 `--no-color`）

#### 场景：详细安装输出

- **当** 用户在安装期间提供 `--verbose` 标志
- **那么** 显示详细步骤：
  - Shell 检测结果
  - 目标文件路径
  - 配置修改
  - 文件创建确认

### 需求：测试支持

补全实现应对所有受支持 shell 可使用单元测试和集成测试进行测试。

#### 场景：模拟 shell 环境

- **当** 编写 shell 检测测试时
- **那么** 允许覆盖 `$SHELL` 和 `$PSModulePath` 环境变量
- **并且** 对文件系统操作使用依赖注入
- **并且** 独立测试所有四种 shell 的检测

#### 场景：生成器输出验证

- **当** 测试补全生成器时
- **那么** 为每个 shell 生成器创建测试套件（zsh、bash、fish、powershell）
- **并且** 验证生成的脚本包含该 shell 的预期模式
- **并且** 测试命令注册表被正确消费
- **并且** 确保动态补全占位符存在
- **并且** 验证特定于 shell 的语法和转义

#### 场景：安装器模拟

- **当** 测试安装逻辑时
- **那么** 为每个 shell 安装器创建测试套件
- **并且** 使用临时测试目录代替实际的 home 目录
- **并且** 验证文件创建而不修改真实的 shell 配置
- **并且** 独立测试路径解析逻辑
- **并且** 模拟文件系统操作以避免副作用

#### 场景：跨 shell 一致性

- **当** 测试补全行为时
- **那么** 验证所有 shell 支持相同的命令和标志
- **并且** 验证动态补全在所有 shell 中一致工作
- **并且** 确保错误消息在所有 shell 中一致
