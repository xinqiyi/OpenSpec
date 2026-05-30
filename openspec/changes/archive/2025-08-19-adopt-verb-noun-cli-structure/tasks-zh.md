# 实施任务

## 1. CLI 行为和帮助
- [x] 1.1 取消弃用顶级 `openspec list`；将 `change list` 标记为已弃用，并显示指向 `openspec list` 的警告
- [x] 1.2 添加通过 `openspec list --specs` 列出 spec 的支持，保持 `--changes` 为默认
- [x] 1.3 更新命令描述和 `--help` 输出，强调动词-名词 schema
- [x] 1.4 保持 `openspec spec ...` 和 `openspec change ...` 命令可用，但打印弃用通知

## 2. 核心列表逻辑
- [x] 2.1 扩展 `src/core/list.ts` 以接受 schema：`changes`（默认）或 `specs`
- [x] 2.2 实现 `specs` 列出：扫描 `openspec/specs/*/spec.md`，通过解析器计算需求数量，一致地格式化输出
- [x] 2.3 两种 schema 共享输出结构；保留当前文本表格；确保未来 JSON 对等

## 3. spec 和约定
- [x] 3.1 更新 `openspec/specs/cli-list/spec.md` 以记录 `--specs`（并默认列出变更）
- [x] 3.2 更新 `openspec/specs/openspec-conventions/spec.md`，增加动词-名词 CLI 设计和弃用指南的需求

## 4. 测试和文档
- [x] 4.1 更新测试：确保 `openspec list` 对变更和 spec 均有效；保留 `change list` 测试但断言警告
- [ ] 4.2 更新 README 和使用文档以显示新的主要命令
- [ ] 4.3 在 repository CHANGELOG 或 README 中添加迁移说明

## 5. 后续工作（可选，不在此变更中）
- [ ] 5.1 考虑 `openspec show --specs/--changes` 用于无需 ID 的发现
- [ ] 5.2 考虑为 `openspec list` 添加 JSON 输出 `--json`，支持两种 schema
