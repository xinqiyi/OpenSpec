## 上下文

OpenSpec 使用 workflow 架构来定义变更 proposal 的 artifact 序列。目前，架构从三个位置解析（项目 → 用户 → 包），但管理自定义架构需要手动创建文件，没有工具支持。解析器基础设施存在（`src/core/artifact-graph/resolver.ts`），但没有用于架构管理操作的 CLI 暴露。

想要自定义 workflow 的用户必须：
1. 在 `openspec/schemas/<name>/` 下手动创建目录结构
2. 复制并修改 `schema.yaml` 文件，没有验证
3. 通过直接检查文件系统来调试解析问题

这给架构自定义带来了摩擦，并导致架构格式错误时的运行时错误。

## 目标 / 非目标

**目标：**
- 为常见的架构管理操作提供 CLI 命令
- 支持带有引导提示的交互式架构创建
- 允许派生现有架构作为自定义起点
- 在运行时之前暴露架构验证错误
- 帮助调试发生影子时的架构解析顺序

**非目标：**
- 架构编辑（用户直接编辑 YAML 或通过 `$EDITOR`）
- 架构发布或共享机制
- 架构版本控制或迁移工具
- 验证 template 文件内容（仅检查存在性）
- 超出简单派生的架构继承或组合

## 决策

### 1. 命令结构：`openspec schema <subcommand>`

添加一个新的命令组，遵循 `openspec config` 和 `openspec completion` 使用的现有 schema。

**理由：** 将相关命令分组到名词（schema）下符合已建立的 CLI schema，并为未来的架构操作提供自然的命名空间。

**考虑的替代方案：**
- 扁平命令（`openspec schema-init`、`openspec schema-fork`）：已拒绝，因为它污染了顶层命名空间且不易扩展。
- 扩展现有命令（`openspec init --schema`）：已拒绝，因为架构管理与项目初始化不同。

### 2. 实施位置

新文件 `src/commands/schema.ts`，包含一个 `registerSchemaCommand(program: Command)` 函数，用于注册 `schema` 命令组和所有子命令。

**理由：** 遵循 `config.ts` 建立的 schema，匹配其他命令组的组织方式。

### 3. 架构验证方法

验证检查：
1. `schema.yaml` 存在且是有效的 YAML
2. 成功针对 `types.ts` 中的 Zod 架构解析
3. 所有引用的 template 文件在架构目录中存在
4. artifact 依赖图无循环（使用现有拓扑排序）

**理由：** 重用现有验证基础设施（`schema.ts` 中的 `parseSchema`）并扩展 template 存在性检查。这能捕获最常见的错误，而无需重复验证逻辑。

**考虑的替代方案：**
- 深度 template 验证（检查 frontmatter、语法）：已拒绝，属于过度设计。template 内容是自由格式的 markdown。

### 4. `schema init` 的交互式提示

使用 `@inquirer/prompts`（已经是依赖项）：
- 架构名称输入，带 kebab-case 验证
- 架构描述输入
- 用于 artifact 选择的多选，带有描述
- 可选：设置为项目默认

**理由：** 匹配 `openspec init` 和 `openspec config reset` 建立的用户体验。在保持向导轻量级的同时提供引导式体验。

### 5. Fork 来源解析

`schema fork <source>` 使用现有的 `getSchemaDir()` 函数解析来源架构，尊重完整的解析顺序（项目 → 用户 → 包）。这允许从任何可访问的架构派生。

目标始终是项目本地：`openspec/schemas/<name>/`

**理由：** 派生到项目范围是有意义的，因为：
- 自定义架构是项目特定的决策
- 用户全局架构可以在需要时手动添加
- 保持命令简单，具有清晰的默认值

### 6. 输出格式一致性

所有命令支持 `--json` 标志，用于机器可读的输出：
- `schema init`：输出 `{ "created": true, "path": "...", "schema": "..." }`
- `schema fork`：输出 `{ "forked": true, "source": "...", "destination": "..." }`
- `schema validate`：输出匹配现有 validate 命令格式的验证报告
- `schema which`：输出 `{ "name": "...", "source": "project|user|package", "path": "..." }`

文本输出使用 ora 旋转器显示进度和清晰的成功/错误消息。

**理由：** 与现有的 OpenSpec 命令一致，并支持脚本编写/自动化。

### 7. Schema `which` 命令设计

显示架构名称的解析详情：
- 从哪个位置解析（project/user/package）
- 架构目录的完整路径
- 是否遮蔽了其他低优先级级别的架构

**理由：** 对于调试"为什么我的架构没有被使用？"的场景至关重要，特别是当多个同名架构存在时。

## 风险 / 权衡

**[template 脚手架可能过时]** → `schema init` 命令将脚手架的默认 artifact 集（proposal、specs、design、tasks）。如果内置架构 schema 演变，这些 template 可能不反映最佳实践。
- *缓解措施*：记录 `init` 创建的是最小的起点。用户可以 `fork` 内置架构以获取最新 schema。

**[CI 环境中的交互式提示]** → 带有提示的 `schema init` 可能在非交互式环境中挂起。
- *缓解措施*：支持 `--name`、`--description` 和 `--artifacts` 标志用于非交互式使用。检测 TTY，并在提示可能挂起时显示有用的错误。

**[验证不能捕获所有错误]** → 架构验证检查结构，但无法验证语义正确性（例如，与其 artifact 目的不匹配的 template）。
- *缓解措施*：这是可以接受的。完整的语义验证需要理解 template 意图，这超出了范围。

**[派生覆盖而不警告]** → 如果目标架构已存在，`fork` 可能覆盖它。
- *缓解措施*：检查现有架构，并在覆盖前需要 `--force` 标志或交互式确认。
