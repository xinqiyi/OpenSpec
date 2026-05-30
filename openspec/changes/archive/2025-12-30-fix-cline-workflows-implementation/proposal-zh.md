## 为什么
Cline 的实现存在架构性错误。根据 Cline 的官方文档，Cline 使用工作流（workflows）进行按需自动化，使用规则（rules）作为行为指南。OpenSpec 斜杠命令是程序性工作流（搭建 → 实施 → 归档），而非行为规则，因此应放置在 `.clinerules/workflows/` 而非 `.clinerules/` 中。

## 变更内容
- 更新 ClineSlashCommandConfigurator，使用 `.clinerules/workflows/` 路径替代 `.clinerules/` 路径
- 更新所有测试以期望正确的工作流文件位置
- 更新 README.md 文档以反映工作流而非规则
- **破坏性变更**：现有的 Cline 用户需要重新运行 `openspec init` 以获取修正后的工作流文件

## 影响范围
- 受影响的规范：cli-init、cli-update（修正后的 Cline 工作流路径）
- 受影响的代码：`src/core/configurators/slash/cline.ts`、测试文件、README.md
- 已修改的文件：`.clinerules/workflows/openspec-*.md`（从 `.clinerules/openspec-*.md` 移入）
