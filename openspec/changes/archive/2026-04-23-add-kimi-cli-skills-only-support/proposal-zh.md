## 原因

OpenSpec 已有用户对 Kimi CLI 支持的需求，但之前的上游尝试停滞不前，因为它假设 Kimi 需要一个命令适配器。对 Kimi CLI 代码库的本地审查显示了一个不同的集成面：Kimi 从 `.kimi/skills/` 发现 `SKILL.md` 文件，并通过 `/skill:<name>` 暴露它们，但它没有像 Claude Code 或 Codex 那样提供稳定的、基于文件的自定义命令目录。

OpenSpec 已经支持安装 skill 而无需命令适配器的工具。Trae 和 ForgeCode 是现有的例子。Kimi 应遵循相同的 schema，而不是引入未记录的 `.kimi/commands/...` 行为。

## 变更内容

- 在 `AI_TOOLS` 中添加 Kimi CLI 作为受支持的工具，包含 `skillsDir: '.kimi'`
- 在支持工具和命令使用文档中，将 Kimi CLI 记录为纯 skill 集成
- 调整变更 spec，使 `cli-init` 明确允许选中的带有 `skillsDir` 但无注册命令适配器的工具

## 能力

### 新增能力

_无。_

### 修改的能力

- `ai-tool-paths`：为 Kimi CLI 定义 `.kimi` skill 根目录
- `cli-init`：澄清无适配器工具仍然是有效选择，并跳过命令文件生成，附带信息性消息

## 影响范围

- `src/core/config.ts` - 添加 Kimi CLI 工具元数据
- `docs/supported-tools.md` - 添加 Kimi CLI 行和工具 ID
- `docs/commands.md` - 记录 Kimi CLI 的 `/skill:openspec-*` 用法
- `docs/cli.md` - 在支持的 `--tools` 列表中包含 `kimi`
- `test/core/init.test.ts` - 覆盖 init 期间作为无适配器工具的 Kimi CLI

## 非目标

- 添加 `src/core/command-generation/adapters/kimi.ts`
- 定义 `.kimi/commands/...` 输出路径
- 更改 `delivery=commands` 下无适配器工具的更广泛交付模型

更广泛的能力感知交付工作已在 `add-tool-command-surface-capabilities` 中单独探索。此变更保持狭窄，并遵循现有的 Trae/ForgeCode schema。
