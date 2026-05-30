# 添加 Shell 补全

## 为什么

OpenSpec CLI 命令缺少 shell 补全，迫使用户手动记忆所有命令、子命令、标志和变更/spec ID。这在日常使用中造成摩擦并降低了开发者 workflow 程的效率。Shell 补全是现代 CLI 工具的标准期望，可以通过以下方式显著改善用户体验：
- 通过 Tab 补全加速命令发现
- 消除记忆需求，减少认知负担
- 通过经过验证的建议减少拼写错误
- 提供生产级工具应有的专业精良度

## 变更内容

此变更为 OpenSpec CLI 添加 shell 补全支持，从 **Zsh（包括 Oh My Zsh）** 开始，并为未来的 shell（bash、fish、PowerShell）建立可扩展的架构。该实现提供：

1. **新的 `openspec completion` 命令**，具有 Zsh 生成和安装/卸载能力
2. **原生 Zsh 集成**，尊重标准的 Zsh Tab 补全行为（单次 TAB 菜单导航）
3. **动态补全提供者**，从当前项目发现活跃的变更和 spec
4. **基于插件的架构**，使用 TypeScript 接口便于在未来的 proposal 中扩展到其他 shell
5. **安装自动化**，适用于 Oh My Zsh（优先）和标准 Zsh 配置
6. **上下文感知的建议**，仅在 OpenSpec 启用的项目中激活

该架构强调清晰的 TypeScript schema、可组合的生成器、shell 特定逻辑与共享补全数据提供者之间的关注点分离，以及与原生 shell 补全系统的集成。其他 shell（bash、fish、PowerShell）在架构上已记录但未在本 proposal 中实现——它们将在后续变更中添加。

## delta

### delta：新的 CLI 补全 spec
- **spec：** cli-completion
- **操作：** 已添加
- **描述：** 定义新的 `openspec completion` 命令的要求，包括生成、安装以及 Oh My Zsh、bash、fish 和 PowerShell 的 shell 特定行为。
