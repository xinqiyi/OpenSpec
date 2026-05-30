## 1. 更新 ClineSlashCommandConfigurator
- [x] 将 `src/core/configurators/slash/cline.ts` 中的 `FILE_PATHS` 从 `.clinerules/openspec-*.md` 改为 `.clinerules/workflows/openspec-*.md`

## 2. 更新测试
- [x] 更新 `test/core/update.test.ts` 中的"应刷新现有 Cline 规则文件"测试，使用 workflow 路径
- [x] 更新 `test/core/init.test.ts` 中的"应使用 template 创建 Cline 规则文件"测试，使用 workflow 路径

## 3. 更新文档
- [x] 更新 README.md 表格，为 Cline 显示"workflow 位于 `.clinerules/workflows/` 目录"

## 4. 验证变更
- [x] 确保所有测试使用新路径通过
- [x] 验证变更遵循 OpenSpec 约定
