# 为 OpenSpec 添加 Init 命令

## 为什么

项目需要一种简单的方式来采用 OpenSpec 约定。目前，用户必须手动创建目录结构并了解所有约定，这给采用带来了摩擦。init 命令可以实现即时 OpenSpec 设置，提供正确的结构和指导。

## 变更内容

- 添加 `openspec init` CLI 命令，创建完整的 OpenSpec 目录结构
- 生成 template 文件（包含 AI 指令的 README.md、project.md template）
- 交互式提示选择要配置哪些 AI 工具（初始为 Claude Code，其他标记为"即将推出"）
- 支持多个 AI 编程助手，具有可扩展的插件架构
- 使用内容标记进行智能文件更新，以保留现有配置
- 使用 `--dir` 标志支持自定义目录命名
- 验证以防止覆盖现有的 OpenSpec 结构
- 带有帮助性指导的清晰错误消息（例如，对现有结构建议使用 'openspec update'）
- 初始化成功后显示可操作的后续步骤

### 破坏性变更
- 无——这是一个新功能

## 影响

- 受影响的 spec：无（新功能）
- 受影响的代码：
 - src/cli/index.ts（添加 init 命令）
 - src/core/init.ts（新建——初始化逻辑）
 - src/core/templates/（新建——template 文件）
 - src/core/configurators/（新建——AI 工具插件）
 - src/utils/file-system.ts（新建——文件操作）
