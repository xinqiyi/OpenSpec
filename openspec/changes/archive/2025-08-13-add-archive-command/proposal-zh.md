## 为什么
需要一个命令将完成的变更 archive 到 archive 文件夹，并带有适当的日期前缀，遵循 OpenSpec 约定。目前变更必须手动移动和重命名。

## 变更内容
- 向 CLI 添加新的 `archive` 命令，将变更移动到 `changes/archive/YYYY-MM-DD-[change-name]/`
- 在 archive 前检查未完成的任务并警告用户
- 允许交互式选择要 archive 的变更
- 如果目标目录已存在，阻止 archive
- 从变更的未来状态 spec 更新主 spec（从 `changes/[name]/specs/` 复制到 `openspec/specs/`）
- 在更新 spec 前显示确认提示，显示将创建/更新哪些 spec
- 支持 `--yes` 标志以跳过确认，用于自动化

## 影响
- 受影响的 spec：cli-archive（新建）
- 受影响的代码：src/cli/index.ts、src/core/archive.ts（新建）
