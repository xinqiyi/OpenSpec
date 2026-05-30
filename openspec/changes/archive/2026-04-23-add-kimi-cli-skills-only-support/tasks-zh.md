## 1. 变更产物

- [x] 1.1 为 Kimi CLI 纯技能支持编写提案、设计和规范 delta

## 2. 工具元数据

- [x] 2.1 在 `src/core/config.ts` 中添加 `Kimi CLI`，包含 `value: 'kimi'` 和 `skillsDir: '.kimi'`

## 3. 文档

- [x] 3.1 更新 `docs/supported-tools.md`，添加 Kimi CLI 行，明确说明无命令适配器
- [x] 3.2 更新 `docs/commands.md`，记录通过 `/skill:openspec-*` 使用 Kimi CLI
- [x] 3.3 更新 `docs/cli.md`，使支持的 `--tools` 列表包含 `kimi`

## 4. 测试

- [x] 4.1 在无适配器命令生成下，为 `--tools kimi` 添加针对性的 init 回归测试

## 5. 验证

- [x] 5.1 使用 `openspec validate` 验证变更产物
- [x] 5.2 运行针对性测试并修复任何回归
