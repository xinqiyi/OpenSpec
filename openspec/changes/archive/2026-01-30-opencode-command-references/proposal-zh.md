## 为什么

OpenCode 使用连字符命令语法（`/opsx-new`），但我们的 template 包含冒号引用（`/opsx:new`）。这导致生成的命令文件和 skill 文件包含与实际命令调用语法不匹配的引用，使 AI 和用户都感到困惑。

## 变更内容

- 创建一个共享的转换工具（`transformToHyphenCommands`），用于将 `/opsx:` 转换为 `/opsx-`
- 更新 OpenCode 命令适配器，使用此工具转换正文文本
- 向 `generateSkillContent()` 添加可选的 `transformInstructions` 回调参数
- 更新 `init.ts` 和 `update.ts`，在为 OpenCode 生成 skill 时传递转换器

## 能力

### 新增能力

无 - 这是一个错误修复，而非新增能力。

### 修改的能力

无 - 无 spec 级别的行为变更。这是 OpenCode 适配器和 skill 生成中的实现修复，不改变任何外部需求或合同。

## 影响

- **代码**：
 - `src/utils/command-references.ts`（新文件）
 - `src/utils/index.ts`（导出）
 - `src/core/shared/skill-generation.ts`（添加回调参数）
 - `src/core/command-generation/adapters/opencode.ts`（使用转换器）
 - `src/core/init.ts`（为 OpenCode 传递转换器）
 - `src/core/update.ts`（为 OpenCode 传递转换器）
- **用户**：OpenCode 用户将在生成的命令文件和 skill 文件中看到正确的 `/opsx-` 命令引用
- **其他工具**：无影响 - 转换仅适用于 OpenCode
