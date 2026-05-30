## 为什么

OpenSpec 安装路径目前不一致：

- 大多数技能和命令写入项目本地目录。
- Codex 命令已经是全局的（`$CODEX_HOME/prompts` 或 `~/.codex/prompts`）。
- 用户无法跨工具选择一致的安装范围策略。

这给偏好用户级设置并期望工具构件默认全局管理的用户带来了摩擦。

## 变更内容

### 1. 添加带有遗留安全默认值的安装范围偏好

引入一个全局安装范围设置，有两种模式：

- `global`（新创建配置的默认值）
- `project`

该设置存储在全局配置中，并可在每次命令运行时覆盖。
对于架构演进而 `installScope` 缺失的旧配置，有效默认值保持为 `project`，直到用户选择加入全局范围。

### 2. 为技能和命令添加能感知范围的路径解析

重构路径解析，使 `init` 和 `update` 都从以下内容计算安装目标：

- 选定的范围偏好（`global` 或 `project`）
- 工具能力元数据（每个工具/界面支持哪些范围）
- 运行时上下文（项目根目录、主目录、环境覆盖）

### 3. 添加每个工具的范围支持能力元数据

扩展工具元数据，为每个界面显式声明范围支持：

- 技能范围支持
- 命令范围支持

当首选范围对于某个工具/界面不受支持时，系统使用确定性的回退规则，并在输出中报告有效范围。

### 4. 使命令生成能感知上下文

扩展命令适配器路径解析，使适配器接收安装上下文（范围 + 环境上下文），而不仅仅是命令 ID。这移除了特殊情况处理，并允许跨工具实现一致的范围行为。

### 5. 更新 init/update UX 和行为

- `openspec init`：
  - 接受范围覆盖标志
  - 使用配置的范围或迁移感知默认值（新配置默认全局；旧配置在迁移前保留 project）
  - 应用能感知范围的生成和清理规划
- `openspec update`：
  - 应用当前范围偏好
  - 在有效范围内按工具/界面同步构件
  - 跟踪每个工具/界面上次成功的有效范围，用于确定性的范围漂移检测
  - 清晰报告有效范围决策

### 6. 扩展配置 UX 和文档

- 在 `openspec config profile` 交互流程中添加安装范围控制。
- 扩展 `openspec config list` 输出，显示安装范围来源（`explicit`、`new-default`、`legacy-default`）。
- 添加显式迁移指导和提示路径，使旧用户可以选择加入 `global` 范围。
- 更新受支持的工具和 CLI 文档，解释范围行为和回退规则。

### 7. 与命令界面能力交付规则协调

`cli-init` 和 `cli-update` 规划应组合：

- 安装范围（`global | project`）
- 交付模式（`both | skills | commands`）
- 命令界面能力（`adapter | skills-invocable | none`）

此提案仍然专注于范围解析，但实施和测试覆盖应包括混合工具案例，以避免与 `add-tool-command-surface-capabilities` 结合时出现回归。

## 能力

### 新能力

- `installation-scope`：范围偏好模型和工具构件安装的有效范围解析。

### 修改的能力

- `global-config`：通过架构演进默认值持久化安装范围偏好。
- `cli-config`：配置和检查安装范围偏好。
- `ai-tool-paths`：添加工具级范围支持元数据和路径策略。
- `command-generation`：通过安装上下文实现能感知范围的适配器路径解析。
- `cli-init`：能感知范围的初始化规划和输出。
- `cli-update`：能感知范围的更新同步、漂移检测和输出。
- `migration`：能感知范围的迁移扫描，带有安装范围感知的工作流查找。

## 影响

- `src/core/global-config.ts` - 新的安装范围字段和默认值
- `src/core/config-schema.ts` - 安装范围配置键的验证支持
- `src/commands/config.ts` - 安装范围的交互式配置文件/配置 UX 添加
- `src/core/config.ts` - 工具范围能力元数据
- `src/core/available-tools.ts` 和 `src/core/shared/tool-detection.ts` - 能感知范围的已配置检测
- `src/core/command-generation/types.ts` 和适配器实现 - 能感知上下文的文件路径解析
- `src/core/init.ts` - 能感知范围的生成/移除规划
- `src/core/update.ts` - 能感知范围的同步/移除/漂移规划
- `src/core/migration.ts` - 能感知范围的工作流扫描支持
- `docs/supported-tools.md` 和 `docs/cli.md` - 安装范围行为文档
- `test/core/init.test.ts`、`test/core/update.test.ts`、适配器测试、配置测试 - 范围覆盖
