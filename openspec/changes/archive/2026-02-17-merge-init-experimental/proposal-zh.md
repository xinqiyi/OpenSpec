## 为什么

当前的设置有两个独立的命令（`openspec init` 和 `openspec experimental`），它们配置 OpenSpec 工作流的不同部分。这导致了对运行哪个命令的混淆、部分设置以及维护两套并行系统（配置文件 + 旧斜杠命令 vs 技能 + opsx 命令）。将基于技能的工作流设为默认，简化了入门流程，并建立了使用 OpenSpec 的单一一致方式。

## 变更内容

- **破坏性变更**：`openspec init` 现在生成技能和 `/opsx:*` 命令，而非配置文件和 `/openspec:*` 命令
- **破坏性变更**：不再生成配置文件（`CLAUDE.md`、`.cursorrules` 等）
- **破坏性变更**：不再生成旧的斜杠命令（`/openspec:proposal`、`/openspec:apply`、`/openspec:archive`）
- **破坏性变更**：不再生成 `openspec/AGENTS.md` 和 `openspec/project.md`
- 将 `experimental` 命令功能合并到 `init` 中
- 添加遗留检测和自动清理，带 Y/N 确认
- 保留 `openspec experimental` 作为隐藏别名，以保持向后兼容
- 统一后的 init 使用 experimental 的动画欢迎界面

## 能力

### 新能力

- `legacy-cleanup`：在 init 期间检测并移除遗留的 OpenSpec 制品（配置文件、旧斜杠命令、AGENTS.md）

### 修改的能力

- `cli-init`：完全重写 - 生成技能和 opsx 命令而非配置文件和旧斜杠命令；移除 AGENTS.md/project.md 生成；添加遗留清理；使用 experimental 的动画欢迎界面

## 影响

- **代码移除**：ToolRegistry、SlashCommandRegistry、配置文件生成器、旧斜杠命令模板、AGENTS.md/project.md 模板
- **代码迁移**：将技能生成和命令适配器逻辑从 `experimental/setup.ts` 移至 `init.ts`
- **受影响的命令**：`init`（重写）、`experimental`（变为隐藏别名）、`update`（可能需要调整）
- **用户迁移**：运行 `init` 的现有用户将被提示清理遗留文件
- **对以下用户构成破坏性变更**：依赖配置文件进行被动触发的用户、使用 `/openspec:*` 命令的用户
