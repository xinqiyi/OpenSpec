## 1. 创建斜杠命令

- [x] 1.1 创建包含技能定义的 `.claude/commands/opsx/archive.md`
- [x] 1.2 添加 YAML frontmatter（name、description、category、tags）
- [x] 1.3 实现变更选择逻辑（如果未提供则提示）
- [x] 1.4 使用 `openspec status --json` 实现产物完成检查
- [x] 1.5 实现任务完成检查（解析 tasks.md 中的 `- [ ]`）
- [x] 1.6 实现规范同步提示（检查 specs/ 目录，提供 `/opsx:sync`）
- [x] 1.7 实现归档过程（移动到 archive/YYYY-MM-DD-<name>/）
- [x] 1.8 为成功/警告情况添加输出格式化

## 2. 重新生成技能

- [x] 2.1 运行 `openspec artifact-experimental-setup` 以重新生成技能
- [x] 2.2 验证技能出现在 `.claude/skills/` 目录中

## 3. 测试

- [x] 3.1 测试 `/opsx:archive` 与完整变更（所有产物、所有任务完成）
- [x] 3.2 测试 `/opsx:archive` 与不完整产物（验证显示警告）
- [x] 3.3 测试 `/opsx:archive` 与不完整任务（验证显示警告）
- [x] 3.4 测试 `/opsx:archive` 与 delta 规范（验证显示同步提示）
- [x] 3.5 测试 `/opsx:archive` 无变更名称（验证显示选择提示）
