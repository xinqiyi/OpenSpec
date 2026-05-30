## 1. CLI init 支持
- [x] 1.1 在原生工具选择器中展示 Antigravity（交互式 + `--tools`），使其可与其他 IDE 一起切换。
- [x] 1.2 生成 `.agent/workflows/openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md`，YAML 前置元数据仅限于每个阶段的单个 `description` 字段，并将主体包裹在 OpenSpec 标记中。
- [x] 1.3 确认工作区搭建覆盖缺失目录创建和重新运行场景，使重复的 init 刷新托管块。

## 2. CLI update 支持
- [x] 2.1 在 `openspec update` 期间检测现有的 Antigravity 工作流文件，仅刷新托管主体，当文件缺失时跳过创建。
- [x] 2.2 确保更新逻辑保留 init 写入时完全相同的 `description` 前置元数据块（包括大小写和间距），并与其他工具一起刷新主体模板。

## 3. 模板和测试
- [x] 3.1 为 Antigravity 添加共享模板条目，复用 Windsurf 的文案，但目标路径为 `.agent/workflows`，并加上仅 description 的前置元数据要求。
- [x] 3.2 扩展自动化测试覆盖（单元或集成），验证 init 和 update 为 Antigravity 生成预期的文件路径、前置元数据和主体标记。
