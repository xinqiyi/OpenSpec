## 背景

Kimi CLI 不是另一个 Claude/Codex 风格的适配器目标。它的扩展模型围绕发现的 skill 构建，而不是外部命令文件：

- skill 从 `.kimi/skills/` 发现
- skill 以 `/skill:<name>` 形式暴露
- 在 Kimi CLI 代码库中未发现稳定的 `.kimi/commands/` 或提示文件加载机制

OpenSpec 的现有架构已经可以表示这种形态：

- `AI_TOOLS` 可以声明 `skillsDir`
- `init` 可以为任何选中的带有 `skillsDir` 的工具安装 skill
- 当尝试为没有适配器的工具生成命令时，OpenSpec 已经记录了 `commandsSkipped`

## 目标

- 使用与 Trae 相同的狭窄 `skills-only` schema 添加 Kimi CLI
- 保持实现小巧：元数据、文档和一个针对性的回归测试
- 使 spec 文本匹配当前无适配器工具的代码路径

## 非目标

- 在没有上游支持的情况下设计 Kimi 特定命令适配器
- 在整个生成管道中更改工具能力建模
- 为所有无适配器工具重做 `delivery=commands` 行为

## 决策

### 1. 将 Kimi CLI 表示为使用 `.kimi` 的无适配器工具

新增 `AI_TOOLS` 条目：

```ts
{ name: 'Kimi CLI', value: 'kimi', available: true, successLabel: 'Kimi CLI', skillsDir: '.kimi' }
```

这与 Kimi CLI 的项目本地 skill 根目录匹配，并允许现有的 init/update 检测路径将其视为受支持的工具。

### 2. 不添加 Kimi 命令适配器

不会添加 `src/core/command-generation/adapters/kimi.ts` 文件，命令适配器注册表将保持不变。

理由：

- Kimi CLI 动态地将 skill 暴露为 `/skill:<name>`
- 先前的上游 PR 停滞不前，正是因为找不到合法的适配器目标
- 添加虚假的 `.kimi/commands/...` 路径会创建 OpenSpec 无法对照上游 Kimi CLI 行为证明其合理性的行为

### 3. 通过 Kimi 的实际调用方式记录

OpenSpec 中的 Kimi 文档必须使用 Kimi 的实际 skill 调用形式：

- supported-tools：无生成的命令文件，使用 `/skill:openspec-*`
- commands 文档：示例如 `/skill:openspec-propose`

文档不得声称 Kimi 可以生成 `opsx-*` 文件或 `/openspec-*` 直接调用。

### 4. 保持变更与现有 Trae 风格行为兼容

此变更有意遵循代码库中现有的无适配器工具行为：

- 当交付包含 skill 时创建 skill
- 当没有适配器存在时跳过命令生成
- init 输出报告 `Commands skipped for: kimi (no adapter)`

这使 Kimi 变更保持小巧，并避免与已在 `add-tool-command-surface-capabilities` 中捕获的实现工作重叠。

## 测试策略

在 `test/core/init.test.ts` 中添加一个针对性的回归测试：

- 配置 `delivery=both`
- 使用 `--tools kimi` 运行 init
- 验证 Kimi skill 在 `.kimi/skills/...` 下创建
- 验证 init 报告了 `kimi` 的跳过命令生成路径

这个测试对于这个狭窄的变更来说已经足够，因为：

- 无适配器更新行为已有通用覆盖
- CLI 工具 ID 渲染源自 `AI_TOOLS`
- 没有引入命令适配器或路径格式化逻辑

## 风险 / 权衡

主要的权衡是范围：Kimi 将继承当前无适配器工具的行为，包括 `delivery=commands` 对于可 skill 调用的工具尚未具备能力感知的广泛限制。对于此变更是可接受的，因为它匹配现有的 Trae/ForgeCode 模型，并使实现与已验证的 Kimi CLI 行为保持一致。
