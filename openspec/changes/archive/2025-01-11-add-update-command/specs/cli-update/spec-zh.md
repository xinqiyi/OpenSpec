# Update 命令 spec

## 目的

作为使用 OpenSpec 的开发者，我希望在发布新版本时更新项目中的 OpenSpec 指令，以便从 AI agent 指令的改进中受益。

## 核心需求

### 更新行为

update 命令应将 OpenSpec 指令文件更新到最新 template。

当用户运行 `openspec update` 时，命令应：
- 检查 `openspec` 目录是否存在
- 将 `openspec/README.md` 替换为最新 template（完全替换）
- 使用标记更新 `CLAUDE.md` 中 OpenSpec 管理的块
 - 保留标记外的用户内容
 - 如果 `CLAUDE.md` 缺失则创建它
- 显示 ASCII 安全成功消息："已更新 OpenSpec 指令"

### 先决条件

该命令要求：
- 存在 `openspec` 目录（由 `openspec init` 创建）

如果 `openspec` 目录不存在，则：
- 显示错误："未找到 OpenSpec 目录。请先运行 'openspec init'。"
- 以退出码 1 退出

### 文件处理

update 命令应：
- 完全替换 `openspec/README.md` 为最新 template
- 仅使用标记更新 `CLAUDE.md` 中 OpenSpec 管理的块
- 使用默认目录名 `openspec`
- 是幂等的（重复运行没有额外效果）

## 边缘情况

### 文件权限
如果文件写入失败，则让错误自然冒泡并包含文件路径。

### CLAUDE.md 缺失
如果 CLAUDE.md 不存在，则使用 template 内容创建它。

### 自定义目录名
此变更中不支持。应使用默认目录名 `openspec`。

## 成功标准

用户应能够：
- 通过单个命令更新 OpenSpec 指令
- 获取最新的 AI agent 指令
- 看到清晰的更新确认

更新过程应：
- 简单且快速（无需版本检查）
- 可预测（每次结果相同）
- 自包含（无需网络）
