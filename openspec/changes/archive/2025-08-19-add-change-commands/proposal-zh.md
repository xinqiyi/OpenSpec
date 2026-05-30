# 变更：添加带 JSON 输出的变更命令

## 为什么

OpenSpec 变更 proposal 目前只能作为 markdown 文件查看，这造成了与 spec 相同的编程访问限制。此外，当前 `openspec list` 命令仅列出变更，这与新的基于资源的命令结构不一致。

## 变更内容

- **cli-change：** 添加用于管理变更 proposal 的新命令，包含 show、list 和 validate 子命令
- **cli-list：** 为遗留 list 命令添加弃用通知，引导用户使用新的 change list 命令

## 影响

- **受影响的 spec**：cli-list（修改以添加弃用通知）
- **受影响的代码**：
 - src/cli/index.ts（注册新命令）
 - src/core/list.ts（添加弃用通知）
