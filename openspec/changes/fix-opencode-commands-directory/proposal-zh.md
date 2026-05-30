## 为什么

OpenCode 适配器对其命令目录使用 `.opencode/command/`（单数），但 OpenCode 的官方文档指定使用 `.opencode/commands/`（复数）。代码库中的每个其他适配器也使用复数目录名（`.claude/commands/`、`.cursor/commands/`、`.factory/commands/` 等）。这种不一致是在 2025 年 10 月引入的，没有记录理由。修复 [#748](https://github.com/Fission-AI/OpenSpec/issues/748)。

## 变更内容

- OpenCode 适配器路径从 `.opencode/command/` 改为 `.opencode/commands/`
- 遗留清理添加 `.opencode/command/`（旧单数路径）以实现向后兼容
- 更新文档以反映新的复数路径

## 能力

### 新能力

_无。_

### 修改的能力

- `command-generation`：OpenCode 适配器路径从单数 `command/` 改为复数 `commands/`，以匹配 OpenCode 的官方目录约定

## 影响

- `src/core/command-generation/adapters/opencode.ts` — 适配器路径
- `src/core/legacy-cleanup.ts` — 遗留清理 schema + 添加旧单数路径
- `docs/supported-tools.md` — 文档表格
- `test/core/command-generation/adapters.test.ts` — 测试断言
