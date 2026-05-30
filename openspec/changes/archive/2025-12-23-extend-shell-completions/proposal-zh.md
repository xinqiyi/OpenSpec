# 变更 proposal：扩展 Shell 补全

## 为什么

Zsh 补全提供了出色的开发者体验，但许多开发者使用 bash、fish 或 PowerShell。将补全支持扩展到这些 shell 可以为大多数不使用 Zsh 的开发者消除障碍。

## 变更内容

此变更为 bash、fish 和 PowerShell 添加补全支持，遵循为 Zsh 补全建立的相同架构 schema、文档方法和测试严谨性。

## delta

- **spec：** `cli-completion`
 - **操作：** 修改
 - **描述：** 扩展补全生成、安装和测试需求以支持 bash、fish 和 PowerShell，同时保持现有的 Zsh 实现和架构 schema
