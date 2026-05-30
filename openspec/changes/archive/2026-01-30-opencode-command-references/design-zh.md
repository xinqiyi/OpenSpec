## 背景

OpenCode 是众多受支持的 AI 工具之一。每个工具都有：
- 一个**命令适配器**（位于 `src/core/command-generation/adapters/`），用于生成特定于工具的命令文件
- 通过 `src/core/shared/skill-generation.ts` 中的 `generateSkillContent()` 生成的**skill**

目前：
- 命令通过适配器系统处理，可以按工具转换内容
- skill 使用单一的共享函数，没有针对特定工具的转换

`src/core/templates/skill-templates.ts` 中的 template 使用 Claude 的冒号格式（`/opsx:new`）作为 spec 格式。使用不同格式的工具需要在生成时进行转换。

## 目标 / 非目标

**目标：**
- 为 OpenCode 在命令和 skill 中将所有 `/opsx:` 命令引用转换为 `/opsx-`
- 创建一个共享的、可复用的转换工具
- 通过回调参数保持转换的可选性（非硬编码工具检测）

**非目标：**
- 修改 spec template 格式（template 保持使用 `/opsx:`）
- 对其他工具应用转换（目前仅限 OpenCode）
- 为 skill 创建完整的适配器系统（当前需求无需过度设计）

## 决策

### 决策 1：共享工具函数

**选择**：在 `src/utils/command-references.ts` 中创建 `transformToHyphenCommands()`

**理由**：
- 转换逻辑的单一真实来源
- 命令适配器和 skill 生成均可使用
- 易于独立测试
- 遵循代码库中现有的 utils schema

**考虑的替代方案**：
- 在每个位置内联转换 - 逻辑重复，难以维护

### 决策 2：skill 生成的回调参数

**选择**：向 `generateSkillContent()` 添加可选的 `transformInstructions?: (instructions: string) => string` 参数

**理由**：
- 灵活 - 调用者定义转换，而非生成函数
- 无耦合 - `generateSkillContent()` 无需了解工具格式
- 可扩展 - 未来可支持其他转换
- 遵循控制反转原则

**考虑的替代方案**：
- 添加工具 ID 参数并根据其进行切换 - 产生耦合，难以扩展
- 创建与命令平行的 skill 适配器系统 - 当前需求过度设计
- 直接在 template 中转换 - 破坏单一真实来源原则

### 决策 3：在生成点应用

**选择**：在 `tool.value === 'opencode'` 时，在 `init.ts` 和 `update.ts` 中传递转换器

**理由**：
- 这是唯一两个生成 skill 的位置
- 简单的条件检查，无需新的抽象
- 如果需要，未来易于扩展到其他工具

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|----------|
| 存在不应转换的其他 `/opsx:` schema | template 中的所有出现都是命令调用 - 通过检查验证 |
| 未来工具可能需要相同的转换 | 工具是共享的且易于复用；可以添加到其他工具的生成中 |
| 回调增加了函数签名的复杂度 | 可选参数，带有合理的默认值（不进行转换） |
