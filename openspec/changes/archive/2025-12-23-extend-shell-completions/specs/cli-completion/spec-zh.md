# cli-completion 规范变更

## 修改后的需求

### 需求：原生 Shell 行为集成

补全系统应尊重并集成每个支持的 shell 的原生补全模式和用户交互模型。

#### 场景：Zsh 原生补全

- **当** 生成 Zsh 补全脚本时
- **那么** 使用带有 `_arguments`、`_describe` 和 `compadd` 的 Zsh 补全系统
- **且** 补全应在单次 TAB 时触发（标准 Zsh 行为）
- **且** 显示为交互式菜单，用户使用 TAB/方向键导航
- **且** 自动支持 Oh My Zsh 的增强菜单样式

#### 场景：Bash 原生补全

- **当** 生成 Bash 补全脚本时
- **那么** 使用 Bash 的 `complete` 内置命令和 `COMPREPLY` 数组
- **且** 补全应在双次 TAB 时触发（标准 Bash 行为）
- **且** 显示为空格分隔列表或列格式
- **且** 同时支持 bash-completion v1 和 v2 模式

#### 场景：Fish 原生补全

- **当** 生成 Fish 补全脚本时
- **那么** 使用 Fish 的 `complete` 命令配合条件
- **且** 补全应在单次 TAB 时触发，带有自动建议预览
- **且** 使用 Fish 的原生着色和描述对齐显示
- **且** 自动利用 Fish 的内置缓存

#### 场景：PowerShell 原生补全

- **当** 生成 PowerShell 补全脚本时
- **那么** 使用带有 scriptblock 的 `Register-ArgumentCompleter`
- **且** 补全应在 TAB 时触发，带有循环行为
- **且** 使用 PowerShell 的原生补全 UI 显示
- **且** 同时支持 Windows PowerShell 5.1 和 PowerShell Core 7+

#### 场景：无自定义 UX 模式

- **当** 为任何 shell 实现补全时
- **那么** 不要尝试自定义补全触发行为
- **且** 不要覆盖特定 shell 的导航模式
- **且** 确保补全对该 shell 的有经验用户感觉原生

### 需求：Shell 检测

补全系统应自动检测用户当前的 shell 环境。

#### 场景：从环境检测 Zsh

- **当** 未显式指定 shell 时
- **那么** 读取 `$SHELL` 环境变量
- **且** 从路径中提取 shell 名称（例如，`/bin/zsh` -> `zsh`）
- **且** 验证 shell 是以下之一：`zsh`、`bash`、`fish`、`powershell`
- **且** 如果 shell 不受支持则抛出错误

#### 场景：从环境检测 Bash

- **当** `$SHELL` 在路径中包含 `bash`
- **那么** 将 shell 检测为 `bash`
- **且** 继续进行特定于 bash 的补全逻辑

#### 场景：从环境检测 Fish

- **当** `$SHELL` 在路径中包含 `fish`
- **那么** 将 shell 检测为 `fish`
- **且** 继续进行特定于 fish 的补全逻辑

#### 场景：从环境检测 PowerShell

- **当** 存在 `$PSModulePath` 环境变量
- **那么** 将 shell 检测为 `powershell`
- **且** 继续进行特定于 PowerShell 的补全逻辑

#### 场景：检测到不支持的 shell

- **当** shell 路径指示不支持的 shell
- **那么** 抛出错误："Shell '<name>' 不受支持。支持的 shell：zsh、bash、fish、powershell"

### 需求：补全生成

补全命令应按需为所有支持的 shell 生成补全脚本。

#### 场景：生成 Zsh 补全

- **当** 用户执行 `openspec completion generate zsh`
- **那么** 将完整的 Zsh 补全脚本输出到标准输出
- **且** 包括所有命令的补全：init、list、show、validate、archive、view、update、change、spec、completion
- **且** 包括所有命令特定的标志和选项
- **且** 使用 Zsh 的 `_arguments` 和 `_describe` 内置函数
- **且** 支持变更和规范 ID 的动态补全

#### 场景：生成 Bash 补全

- **当** 用户执行 `openspec completion generate bash`
- **那么** 将完整的 Bash 补全脚本输出到标准输出
- **且** 包括所有命令和子命令的补全
- **且** 使用带有自定义补全函数的 `complete -F`
- **且** 使用适当的建议填充 `COMPREPLY`
- **且** 通过 `openspec __complete` 支持变更和规范 ID 的动态补全

#### 场景：生成 Fish 补全

- **当** 用户执行 `openspec completion generate fish`
- **那么** 将完整的 Fish 补全脚本输出到标准输出
- **且** 使用带有条件的 `complete -c openspec`
- **且** 使用 `--condition` 谓词包括命令特定的补全
- **且** 通过 `openspec __complete` 支持变更和规范 ID 的动态补全
- **且** 为每个补全选项包括描述

#### 场景：生成 PowerShell 补全

- **当** 用户执行 `openspec completion generate powershell`
- **那么** 将完整的 PowerShell 补全脚本输出到标准输出
- **且** 使用 `Register-ArgumentCompleter -CommandName openspec`
- **且** 实现处理命令上下文的 scriptblock
- **且** 通过 `openspec __complete` 支持变更和规范 ID 的动态补全
- **且** 返回 `[System.Management.Automation.CompletionResult]` 对象

### 需求：安装自动化

补全命令应自动将补全脚本安装到所有支持的 shell 的配置文件中。

#### 场景：为 Oh My Zsh 安装

- **当** 用户执行 `openspec completion install zsh`
- **那么** 通过检查 `$ZSH` 环境变量或 `~/.oh-my-zsh/` 目录检测是否安装了 Oh My Zsh
- **且** 如果不存在则在 `~/.oh-my-zsh/custom/completions/` 创建自定义补全目录
- **且** 将补全脚本写入 `~/.oh-my-zsh/custom/completions/_openspec`
- **且** 如有需要，通过更新 `~/.zshrc` 确保 `~/.oh-my-zsh/custom/completions` 在 `$fpath` 中
- **且** 显示成功消息，指导用户运行 `exec zsh` 或重启终端

#### 场景：为标准 Zsh 安装

- **当** 用户执行 `openspec completion install zsh` 且未检测到 Oh My Zsh
- **那么** 如果不存在则在 `~/.zsh/completions/` 创建补全目录
- **且** 将补全脚本写入 `~/.zsh/completions/_openspec`
- **且** 如果尚未存在，将 `fpath=(~/.zsh/completions $fpath)` 添加到 `~/.zshrc`
- **且** 如果尚未存在，将 `autoload -Uz compinit && compinit` 添加到 `~/.zshrc`
- **且** 显示成功消息，指导用户运行 `exec zsh` 或重启终端

#### 场景：为 Bash 安装（带 bash-completion）

- **当** 用户执行 `openspec completion install bash`
- **那么** 通过检查 `/usr/share/bash-completion` 或 `/etc/bash_completion.d` 检测是否安装了 bash-completion
- **且** 如果 bash-completion 可用，写入到 `/etc/bash_completion.d/openspec`（需 sudo）或 `~/.local/share/bash-completion/completions/openspec`
- **且** 如果 bash-completion 不可用，写入到 `~/.bash_completion.d/openspec` 并从 `~/.bashrc` 引用
- **且** 如有需要，使用基于标记的更新将引用行添加到 `~/.bashrc`
- **且** 显示成功消息，指导用户运行 `exec bash` 或重启终端

#### 场景：为 Fish 安装

- **当** 用户执行 `openspec completion install fish`
- **那么** 如果不存在则在 `~/.config/fish/completions/` 创建 Fish 补全目录
- **且** 将补全脚本写入 `~/.config/fish/completions/openspec.fish`
- **且** Fish 自动从此目录加载补全（无需修改配置文件）
- **且** 显示成功消息，指示补全立即可用

#### 场景：为 PowerShell 安装

- **当** 用户执行 `openspec completion install powershell`
- **那么** 通过 `$PROFILE` 环境变量或默认路径检测 PowerShell 配置文件位置
- **且** 如果不存在则创建配置文件目录
- **且** 使用基于标记的更新将补全脚本导入添加到配置文件
- **且** 将补全脚本写入 PowerShell 模块目录或与配置文件并列
- **且** 显示成功消息，指导用户重启 PowerShell 或运行 `. $PROFILE`

#### 场景：自动检测 shell 进行安装

- **当** 用户执行 `openspec completion install` 而不指定 shell
- **那么** 使用 shell 检测逻辑检测当前 shell
- **且** 为检测到的 shell（zsh、bash、fish 或 powershell）安装补全
- **且** 显示检测到了哪个 shell

#### 场景：已安装

- **当** 目标 shell 的补全已安装
- **那么** 显示消息指示补全已安装
- **且** 提供通过覆盖现有文件重新安装/更新的选项
- **且** 以代码 0 退出

### 需求：卸载

补全命令应移除所有支持的 shell 的已安装补全脚本和配置。

#### 场景：卸载 Zsh 补全

- **当** 用户执行 `openspec completion uninstall zsh`
- **那么** 在继续之前提示确认（除非提供了 `--yes` 标志）
- **且** 如果用户拒绝，取消卸载并显示"卸载已取消。"
- **且** 如果用户确认，如果检测到 Oh My Zsh，移除 `~/.oh-my-zsh/custom/completions/_openspec`
- **且** 如果检测到标准 Zsh 设置，移除 `~/.zsh/completions/_openspec`
- **且** 使用基于标记的移除方式从 `~/.zshrc` 中移除 fpath 修改
- **且** 显示成功消息

#### 场景：卸载 Bash 补全

- **当** 用户执行 `openspec completion uninstall bash`
- **那么** 提示确认（除非提供了 `--yes` 标志）
- **且** 如果用户确认，从 bash-completion 目录或 `~/.bash_completion.d/` 移除补全文件
- **且** 使用基于标记的移除方式从 `~/.bashrc` 中移除引用行
- **且** 显示成功消息

#### 场景：卸载 Fish 补全

- **当** 用户执行 `openspec completion uninstall fish`
- **那么** 提示确认（除非提供了 `--yes` 标志）
- **且** 如果用户确认，移除 `~/.config/fish/completions/openspec.fish`
- **且** 显示成功消息（无需修改配置文件）

#### 场景：卸载 PowerShell 补全

- **当** 用户执行 `openspec completion uninstall powershell`
- **那么** 提示确认（除非提供了 `--yes` 标志）
- **且** 如果用户确认，使用基于标记的移除方式从 PowerShell 配置文件中移除补全导入
- **且** 移除补全脚本文件
- **且** 显示成功消息

#### 场景：自动检测 shell 进行卸载

- **当** 用户执行 `openspec completion uninstall` 而不指定 shell
- **那么** 检测当前 shell 并卸载该 shell 的补全

#### 场景：未安装

- **当** 尝试卸载未安装的补全时
- **那么** 显示错误消息，指示补全未安装
- **且** 以代码 1 退出

### 需求：架构模式

补全实现应遵循清晰架构原则，采用 TypeScript 最佳实践，通过基于插件的模式支持多个 shell。

#### 场景：特定于 shell 的生成器

- **当** 实现补全生成器时
- **那么** 为每个 shell 创建生成器类：`ZshGenerator`、`BashGenerator`、`FishGenerator`、`PowerShellGenerator`
- **且** 实现一个公共的 `CompletionGenerator` 接口，方法为：
  - `generate(commands: CommandDefinition[]): string` - 返回完整的 shell 脚本
- **且** 每个生成器处理特定于 shell 的语法、转义和模式
- **且** 所有生成器消费来自命令注册表的相同 `CommandDefinition[]`

#### 场景：特定于 shell 的安装器

- **当** 实现补全安装器时
- **那么** 为每个 shell 创建安装器类：`ZshInstaller`、`BashInstaller`、`FishInstaller`、`PowerShellInstaller`
- **且** 实现一个公共的 `CompletionInstaller` 接口，方法为：
  - `install(script: string): Promise<InstallationResult>` - 安装补全脚本
  - `uninstall(): Promise<{ success: boolean; message: string }>` - 移除补全
- **且** 每个安装器处理特定于 shell 的路径、配置文件和安装模式

#### 场景：用于 shell 选择的工厂模式

- **当** 选择特定于 shell 的实现时
- **那么** 使用带有静态方法的 `CompletionFactory` 类：
  - `createGenerator(shell: SupportedShell): CompletionGenerator`
  - `createInstaller(shell: SupportedShell): CompletionInstaller`
- **且** 工厂使用带有 TypeScript 穷举检查的 switch 语句
- **且** 添加新 shell 需要更新 `SupportedShell` 类型和工厂分支

#### 场景：动态补全提供者

- **当** 实现动态补全时
- **那么** 创建一个封装项目发现逻辑的 `CompletionProvider` 类
- **且** 实现方法：
  - `getChangeIds(): Promise<string[]>` - 发现活跃变更 ID
  - `getSpecIds(): Promise<string[]>` - 发现规范 ID
  - `isOpenSpecProject(): boolean` - 检查当前目录是否启用 OpenSpec
- **且** 使用类属性实现具有 2 秒 TTL 的缓存

#### 场景：命令注册表

- **当** 定义可补全的命令时
- **那么** 创建一个集中的 `CommandDefinition` 类型，属性为：
  - `name: string` - 命令名称
  - `description: string` - 帮助文本
  - `flags: FlagDefinition[]` - 可用标志
  - `acceptsPositional: boolean` - 命令是否接受位置参数
  - `positionalType: string` - 位置参数类型（change-id、spec-id、path、shell）
  - `subcommands?: CommandDefinition[]` - 嵌套子命令
- **且** 导出一个包含所有命令定义的 `COMMAND_REGISTRY` 常量
- **且** 所有生成器消费此注册表以确保跨 shell 的一致性

#### 场景：类型安全的 shell 检测

- **当** 实现 shell 检测时
- **那么** 将 `SupportedShell` 类型定义为字面类型：`'zsh' | 'bash' | 'fish' | 'powershell'`
- **且** 在 `src/utils/shell-detection.ts` 中实现 `detectShell()` 函数
- **且** 返回检测到的 shell，或抛出错误并列出支持的 shell

### 需求：测试支持

补全实现应可通过所有支持的 shell 的单元测试和集成测试进行测试。

#### 场景：模拟 shell 环境

- **当** 编写 shell 检测的测试时
- **那么** 允许覆盖 `$SHELL` 和 `$PSModulePath` 环境变量
- **且** 对文件系统操作使用依赖注入
- **且** 独立测试所有四个 shell 的检测

#### 场景：生成器输出验证

- **当** 测试补全生成器时
- **那么** 为每个 shell 生成器创建测试套件（zsh、bash、fish、powershell）
- **且** 验证生成的脚本包含该 shell 的预期模式
- **且** 测试命令注册表被正确消费
- **且** 确保动态补全占位符存在
- **且** 验证特定于 shell 的语法和转义

#### 场景：安装器模拟

- **当** 测试安装逻辑时
- **那么** 为每个 shell 安装器创建测试套件
- **且** 使用临时测试目录代替实际的主目录
- **且** 验证文件创建而不修改真实的 shell 配置
- **且** 独立测试路径解析逻辑
- **且** 模拟文件系统操作以避免副作用

#### 场景：跨 shell 一致性

- **当** 测试补全行为时
- **那么** 验证所有 shell 支持相同的命令和标志
- **且** 验证动态补全在所有 shell 中一致工作
- **且** 确保错误消息跨 shell 一致
