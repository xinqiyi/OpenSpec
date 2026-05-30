## 1. 适配器修复

- [x] 1.1 更新 `src/core/command-generation/adapters/opencode.ts`：将 `path.join('.opencode', 'command', ...)` 改为 `path.join('.opencode', 'commands', ...)` 并更新 JSDoc 注释

## 2. 遗留清理

- [x] 2.1 更新 `src/core/legacy-cleanup.ts`：将 `LEGACY_SLASH_COMMAND_PATHS` 中的 `'opencode'` 条目更新为检测 `.opencode/command/` 下的 `opsx-*.md` 和 `openspec-*.md` 两种 schema 以实现向后兼容

## 3. 文档

- [x] 3.1 更新 `docs/supported-tools.md`：将 OpenCode 命令路径从 `.opencode/command/opsx-<id>.md` 改为 `.opencode/commands/opsx-<id>.md`

## 4. 测试

- [x] 4.1 更新 `test/core/command-generation/adapters.test.ts`：将 OpenCode 文件路径断言从 `path.join('.opencode', 'command', 'opsx-explore.md')` 改为 `path.join('.opencode', 'commands', 'opsx-explore.md')`

## 5. Changeset

- [x] 5.1 创建 changeset 文件（`.changeset/fix-opencode-commands-directory.md`），使用 patch bump 描述路径修复
