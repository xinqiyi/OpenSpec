## 为什么
需要一个命令将完成的变更归档到归档文件夹，并带有适当的日期前缀，遵循 OpenSpec 约定。目前变更必须手动移动和重命名。

## 变更内容
- 向 CLI 添加新的 `archive` 命令，将变更移动到 `changes/archive/YYYY-MM-DD-[change-name]/`
- 在归档前检查未完成的任务并警告用户
- 允许交互式选择要归档的变更
- 如果目标目录已存在，阻止归档
- 从变更的未来状态规范更新主规范（从 `changes/[name]/specs/` 复制到 `openspec/specs/`）
- 在更新规范前显示确认提示，显示将创建/更新哪些规范
- 支持 `--yes` 标志以跳过确认，用于自动化

## 影响
- 受影响的规范：cli-archive（新建）
- 受影响的代码：src/cli/index.ts、src/core/archive.ts（新建）
