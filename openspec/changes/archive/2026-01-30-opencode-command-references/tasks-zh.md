## 1. 实现

- [x] 1.1 创建 `src/utils/command-references.ts`，包含 `transformToHyphenCommands()` 函数
- [x] 1.2 从 `src/utils/index.ts` 导出 `transformToHyphenCommands`
- [x] 1.3 更新 `src/core/shared/skill-generation.ts` 中的 `generateSkillContent()`，接受可选的 `transformInstructions` 回调
- [x] 1.4 更新 `src/core/command-generation/adapters/opencode.ts` 中的 OpenCode 适配器，在正文文本中使用 `transformToHyphenCommands()`
- [x] 1.5 更新 `init.ts`，在为 OpenCode 生成技能时传递转换器
- [x] 1.6 更新 `update.ts`，在为 OpenCode 生成技能时传递转换器

## 2. 测试

- [x] 2.1 创建 `test/utils/command-references.test.ts`，包含 `transformToHyphenCommands()` 的单元测试
- [x] 2.2 向 `test/core/command-generation/adapters.test.ts` 添加 OpenCode 正文转换测试
- [x] 2.3 向 `test/core/shared/skill-generation.test.ts` 添加转换器回调测试

## 3. 验证

- [x] 3.1 运行 `npx vitest run test/utils/command-references.test.ts test/core/command-generation/adapters.test.ts test/core/shared/skill-generation.test.ts` 确保测试通过
- [x] 3.2 运行 `pnpm run build` 确保无 TypeScript 错误
- [x] 3.3 在临时目录中运行 `openspec init --tools opencode` 并验证：
  - `.opencode/command/` 中的命令文件包含 `/opsx-` 引用（不是 `/opsx:`）
  - `.opencode/skills/` 中的技能文件包含 `/opsx-` 引用（不是 `/opsx:`）
