## 动机
当前的 `openspec init` 命令需要交互式提示，无法在 CI/CD 流水线和脚本化设置中使用。添加非交互式选项将支持自动化工作流的编程式初始化，同时保持现有的交互式体验作为默认方式。

## 变更内容
- 将多个标志设计替换为单个 `--tools` 选项，接受 `all`、`none` 或逗号分隔的工具 ID 列表
- 更新 InitCommand，在提供 `--tools` 时跳过交互式提示，并应用单标志验证规则
- 通过 CLI init 规范增量文档化非交互式行为（`all`、`none`、列表解析和无效条目的场景）
- 从 `AI_TOOLS` 动态生成 CLI 帮助文本，使支持的工具保持同步

## 影响范围
- 受影响的规范：`specs/cli-init/spec.md`
- 受影响的代码：`src/cli/index.ts`、`src/core/init.ts`
