## 为什么

OpenSpec 目前假设命令交付直接映射到命令适配器。这个假设并不适用于所有工具。

Trae 是一个具体的例子：它通过 skill 条目（例如 `/openspec-new-change`）而非适配器生成的命令文件来调用 OpenSpec workflow。在这种 schema 下，skill 就是命令表面。

目前，这造成了行为上的差距：

- `delivery=commands` 可能会移除 skill
- 没有适配器的工具会跳过命令生成
- 结果：选中的工具（如 Trae）可能最终没有可调用的 workflow artifact

这不仅仅是提示层面的用户体验问题，因为非交互式和 CI 流程会绕过交互式指导。我们需要在核心生成逻辑中建立一个能力感知模型。

## 变更内容

### 1. 添加显式的命令表面能力元数据

在工具元数据中添加一个可选字段，描述工具如何暴露命令：

- `adapter`：命令文件通过命令适配器生成
- `skills-invocable`：skill 可直接作为命令调用
- `none`：无 OpenSpec 命令表面

该字段应为可选的。默认行为从适配器注册表存在性推断：有已注册适配器的工具解析为 `adapter`；没有适配器注册且没有显式注解的工具解析为 `none`。
能力值使用 kebab-case 字符串标记，以与序列化元数据约定保持一致。

初始显式覆盖：

- Trae -> `skills-invocable`

### 2. 使交付行为具有能力感知

更新 `init` 和 `update`，根据以下因素计算每个工具的有效 artifact 操作：

- 全局交付（`both | skills | commands`）
- 工具命令表面能力

行为矩阵：

- `both`：
 - 为所有有 `skillsDir` 的工具生成 skill（包括 `skills-invocable`）
 - 仅为 `adapter` 工具生成命令文件
 - `none`：无 artifact 操作；可以发出兼容性警告
- `skills`：
 - 为所有有 `skillsDir` 的工具生成 skill（包括 `skills-invocable`）
 - 移除适配器生成的命令文件
 - `none`：无 artifact 操作；可以发出兼容性警告
- `commands`：
 - `adapter`：生成命令，移除 skill
 - `skills-invocable`：生成（或保持最新）skill 作为命令表面；不移除它们
 - `none`：快速失败，带有清晰错误

### 3. 添加预检验证和更清晰的输出

在写入/移除 artifact 之前，验证选中/已配置的工具与交付 schema：

- 交互式流程：在确认前显示清晰的兼容性说明
- 非交互式流程：以确定性错误失败，列出不兼容的工具和支持的替代方案

更新摘要，显示每个工具有效交付结果（例如，当 commands schema 仍为 skills-invocable 工具安装 skill 时）。

### 4. 更新文档和测试

- 记录能力模型和 Trae 在交付 schema 下的行为
- 确保 CLI 文档和支持工具文档反映有效行为
- 添加测试覆盖：
 - `init --tools trae` 配合 `delivery=commands`
 - `update` 配合在 `delivery=commands` 下配置的 Trae
 - 所有交付 schema 下的混合选择（`claude + trae`）
 - 在 `delivery=commands` 下无命令表面工具的显式错误路径

### 5. 与安装范围行为协调

当与 `add-global-install-scope` 组合时，init/update planning 必须组合：

- 安装范围（`global | project`）
- 交付 schema（`both | skills | commands`）
- 命令表面能力（`adapter | skills-invocable | none`）

实现测试应覆盖混合工具矩阵，确保两个变更都激活时的确定性行为。

## 能力

### 新能力

- `tool-command-surface`：将工具分类为 `adapter`、`skills-invocable` 或 `none` 以驱动交付行为的能力模型

### 被修改的能力

- `cli-init`：交付处理变为工具能力感知，带预检兼容性验证
- `cli-update`：交付同步变为工具能力感知，具有一致的兼容性验证和消息
- `supported-tools-docs`：记录非适配器工具的命令表面语义

## 影响

- `src/core/config.ts` - 添加可选的命令表面元数据和 Trae 覆盖
- `src/core/command-generation/registry.ts`（或共享辅助函数）- 从适配器存在性推断能力
- `src/core/init.ts` - 能力感知的生成/移除 planning + 兼容性验证 + 摘要消息
- `src/core/update.ts` - 能力感知的同步/移除 planning + 兼容性验证 + 摘要消息
- `src/core/shared/tool-detection.ts` - 包含能力感知检测，使 `skills-invocable` 工具在 `delivery=commands` 下仍可检测，`none` 工具从命令表面 artifact 检测中排除
- `docs/supported-tools.md` 和 `docs/cli.md` - 记录交付行为和兼容性说明
- `test/core/init.test.ts` 和 `test/core/update.test.ts` - 添加 skills-invocable 行为和混合工具交付场景的覆盖

## 排序说明

- 此变更旨在通过为 init/update 添加 delta 的、能力特定的需求，与 `simplify-skill-installation` 安全堆叠。
- 如果 `simplify-skill-installation` 先合并，此变更应进行变基，并将能力感知规则作为 `delivery=commands` 对 `skills-invocable` 工具行为的真相来源。
- 如果此变更先合并，`simplify-skill-installation` 分支应进行变基，以避免重新引入全局性的"仅命令 schema 意味着所有工具都没有 skill"的假设。
- 如果 `add-global-install-scope` 先合并，此变更应进行变基，在该变更的范围解析路径决策之上组合能力感知行为。
- 如果此变更先合并，`add-global-install-scope` 应进行变基，以保留第 5 节的组合规则（`安装范围` + `交付 schema` + `命令表面能力`），而不覆盖能力感知的命令表面结果。
