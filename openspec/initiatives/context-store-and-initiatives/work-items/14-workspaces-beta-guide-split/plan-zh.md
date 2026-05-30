# workspace Beta 指南拆分

## 状态

提议的下一个工作项。

## 目标

使 Beta 文档匹配人们应该实际使用该功能的方式：

- 用户使用终端提示进行本地设置和本地路径
- 编码 agent 使用显式 CLI 命令进行 OpenSpec 工作

## 工作模型

面向用户的文档应少用标志，多用 agent 提示。agent CLI 手册应包含确切的命令、JSON 界面、cwd 规则和当前注意事项。

手动 Beta 说明：在 workspace 打开后，用户应要求 agent 从 workspace 探索或起草。agent 应解析 workspace 和倡议上下文，识别所属链接 repository，并从该 repository 运行 repository 本地的 OpenSpec 命令。workspace 是对话界面，而不是制品的存放位置。

## 范围

- 修订 `docs/workspaces-beta/user-guide.md`。
- 修订 `docs/workspaces-beta/agent-cli-playbook.md`。
- 在流程经过手动测试之前保持文档最小化。
- 记录文档审查期间发现的命令或提示差距。

## 非目标

- 在此工作项中不更改 CLI 行为。
- 不承诺同步、克隆、分支、工作树、进度仪表板或强制编辑边界。
