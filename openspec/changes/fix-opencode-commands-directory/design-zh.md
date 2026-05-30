## 上下文

`src/core/command-generation/adapters/opencode.ts` 中的 OpenCode 适配器当前在 `.opencode/command/opsx-<id>.md`（单数 `command`）生成命令文件。OpenCode 的官方文档使用 `.opencode/commands/`（复数），并且代码库中的每个其他适配器都遵循复数约定用于命令目录。`src/core/legacy-cleanup.ts` 中的遗留清理模块也引用了单数形式用于检测旧工件。

## 目标 / 非目标

**目标：**
- 将 OpenCode 适配器路径与 OpenCode 官方 `.opencode/commands/` 约定对齐
- 将旧的单数路径 `.opencode/command/` 添加到遗留清理中，以便正确清理现有安装
- 更新文档以反映修正后的路径
- 更新测试断言以匹配新路径

**非目标：**
- 更改 OpenCode 技能路径（`.opencode/skills/`）—— 已经正确
- 修改任何其他适配器的目录结构
- 添加迁移提示或交互式升级流程

## 决策

### 1. 适配器中的直接路径重命名

**决策：** 将适配器 `getFilePath` 方法中的 `path.join('.opencode', 'command', ...)` 改为 `path.join('.opencode', 'commands', ...)`。

**理由：** 这是一个单行更改，与所有其他适配器的既定模式对齐。无需抽象或间接层。

**考虑的替代方案：**
- 为目录名添加配置选项 —— 因过度设计而被拒绝，这只是一个错误修复
- 保留单数并添加复数作为别名 —— 因会在哪个是规范上造成歧义而被拒绝

### 2. 通过现有常量映射进行遗留清理

**决策：** 将 `'opencode'` 的 `LEGACY_SLASH_COMMAND_PATHS` 条目从 `'.opencode/command/openspec-*.md'` 更新为 `'.opencode/command/opsx-*.md'`（旧的单数路径成为遗留模式），并确保当前命令生成管道处理新路径。

**理由：** 现有的遗留清理基础设施使用 `LEGACY_SLASH_COMMAND_PATHS` 作为显式查找。旧的单数路径模式已经匹配遗留格式（旧 SlashCommandRegistry 时代的 `openspec-*` 前缀）。当前命令生成使用 `opsx-*` 前缀，因此我们还需要为旧单数目录中的 `opsx-*` 文件添加遗留模式。

**考虑的替代方案：**
- 添加单独的迁移脚本 —— 被拒绝；现有的遗留清理机制可以处理此场景

### 3. 文档更新

**决策：** 将 `docs/supported-tools.md` 中 OpenCode 的表格条目从 `.opencode/command/opsx-<id>.md` 更新为 `.opencode/commands/opsx-<id>.md`。

**理由：** 文档必须与实际生成的路径匹配。

## 风险 / 权衡

- **[现有安装在旧路径有文件]** —— 通过遗留清理检测 `.opencode/command/` 工件来缓解。下次运行 `openspec init` 时，旧文件被清理，新文件写入 `.opencode/commands/`。
- **[用户在其自定义脚本中引用旧路径]** —— 风险较低。旧的路径本身就不符合 OpenCode 的规范，因此自定义引用已经不对齐。
