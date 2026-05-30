# 实现任务

## 第一阶段：基础与架构

- [x] 创建 `src/utils/shell-detection.ts`，包含 `SupportedShell` 类型和 `detectShell()` 函数
- [x] 创建 `src/core/completions/types.ts`，包含接口：`CompletionGenerator`、`CommandDefinition`、`FlagDefinition`
- [x] 创建 `src/core/completions/command-registry.ts`，包含定义所有 OpenSpec 命令、标志和元数据的 `COMMAND_REGISTRY` 常量
- [x] 创建 `src/core/completions/completion-provider.ts`，包含用于动态变更/spec ID 发现且带有 2 秒缓存的 `CompletionProvider` 类
- [x] 为 shell 检测编写测试（`test/utils/shell-detection.test.ts`）
- [x] 为 completion provider 编写测试（`test/core/completions/completion-provider.test.ts`）

## 第二阶段：Zsh 补全（Oh My Zsh 优先）

- [x] 创建 `src/core/completions/generators/zsh-generator.ts`，实现 `CompletionGenerator` 接口
- [x] 使用 `_arguments` 和 `_describe` 模式实现 Zsh 脚本生成
- [x] 使用 completion provider 为变更/spec ID 添加动态补全逻辑
- [x] 测试 Zsh 生成器输出（`test/core/completions/generators/zsh-generator.test.ts`）
- [x] 创建 `src/core/completions/installers/zsh-installer.ts`，支持 Oh My Zsh 和标准 Zsh
- [x] 实现 Oh My Zsh 检测（`$ZSH` 环境变量或 `~/.oh-my-zsh/` 目录）
- [x] 实现安装到 `~/.oh-my-zsh/custom/completions/_openspec`（针对 Oh My Zsh）
- [x] 实现回退安装到 `~/.zsh/completions/_openspec`，并更新 `fpath`
- [x] 使用模拟文件系统测试 Zsh 安装器逻辑（`test/core/completions/installers/zsh-installer.test.ts`）

## 第三阶段：CLI 命令实现

- [x] 创建 `src/commands/completion.ts`，包含 `CompletionCommand` 类
- [x] 在 `src/cli/index.ts` 中注册 `completion` 命令，包含子命令：generate、install、uninstall
- [x] 实现 `generateSubcommand()`，将 Zsh 脚本输出到 stdout
- [x] 实现 `installSubcommand(shell?: 'zsh')`，带有 Zsh 的自动检测功能
- [x] 实现 `uninstallSubcommand(shell?: 'zsh')`，用于移除 Zsh 补全
- [x] 为详细安装输出添加 `--verbose` 标志支持
- [x] 添加带有清晰信息的错误处理："Shell '<name>' is not supported yet. Currently supported: zsh"
- [x] 测试补全命令集成（`test/commands/completion.test.ts`）

## 第四阶段：集成与完善

- [x] 在 `src/core/completions/factory.ts` 中创建工厂模式，用于实例化 Zsh 生成器/安装器（可扩展以支持未来的 shell）
- [x] 将 `completion` 命令添加到命令注册表中，以实现自引用补全
- [x] 在 Zsh 生成器中实现动态补全辅助函数（`_openspec_complete_changes`、`_openspec_complete_specs`、`_openspec_complete_items`）
- [x] 为补全命令参数添加 `shell` 位置类型
- [x] 测试带有动态辅助函数的补全生成
- [x] 测试补全安装/卸载流程
- [x] 确认所有测试通过（97 个补全测试，共 340 个测试）
- [x] 通过 npm postinstall 脚本实现自动安装
- [x] 添加安全检查（CI 检测、选择退出标志）
- [x] 处理 Oh My Zsh 与标准 Zsh 安装路径
- [x] 为 postinstall 验证添加测试脚本
- [x] 在 README 中记录自动安装行为和选择退出方式
- [ ] 在 Oh My Zsh 环境中手动测试 Zsh 补全（安装、测试 Tab 补全、卸载）
- [ ] 在标准 Zsh 环境中手动测试 Zsh 补全
- [ ] 在真实的 OpenSpec 项目中测试动态变更/spec ID 补全
- [ ] 验证补全缓存行为（2 秒 TTL）
- [ ] 测试在 OpenSpec 项目之外的行为（应跳过动态补全）
- [x] 更新 `openspec --help` 输出，包含 completion 命令（通过 Commander 自动完成）

## 第五阶段：边界情况与错误处理

- [ ] 测试并处理安装过程中的权限错误
- [ ] 测试并处理缺少 shell 配置目录的情况（自动创建并通知）
- [ ] 测试"已安装"检测和重新安装流程
- [ ] 测试卸载时的"未安装"检测
- [ ] 确认补全命令输出中尊重 `--no-color` 标志
- [ ] 测试 shell 检测失败场景，提供有帮助的错误信息
- [ ] 确保在 `$SHELL` 未设置或无效时优雅处理
- [ ] 测试非 Zsh shell 能收到清晰的"尚不支持"错误信息
- [ ] 测试生成器输出可以重定向到文件而不会损坏

## 依赖关系

- 第二阶段依赖第一阶段（基础必须先存在）
- 第三阶段依赖第二阶段（CLI 需要 Zsh 生成器正常工作）
- 第四阶段依赖第三阶段（集成需要 CLI + Zsh 实现）
- 第五阶段依赖第四阶段（核心功能完成后进行边界情况测试）

## 未来工作（不在本提案范围内）

- **Bash 补全** - 在后续提案中创建 bash-generator.ts 和 bash-installer.ts
- **Fish 补全** - 在后续提案中创建 fish-generator.ts 和 fish-installer.ts
- **PowerShell 补全** - 在后续提案中创建 powershell-generator.ts 和 powershell-installer.ts

该架构设计使得通过实现 `CompletionGenerator` 接口即可轻松添加这些 shell 的支持。
