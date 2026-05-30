# 设计：添加 /opsx:verify 技能

## 架构决策：通过设置命令动态生成

### 背景

所有现有的 opsx 实验性技能（explore、new、continue、apply、ff、sync、archive）都是在用户运行 `openspec artifact-experimental-setup` 时动态生成的。它们不是手动创建并检入仓库的静态文件。

### 决策

**将 verify 集成到现有的 artifact-experimental-setup 系统中，而不是创建静态技能文件。**

### 理由

1. **一致性**：所有现有的 7 个 opsx 技能都遵循此模式。将 verify 作为第 8 个技能添加应遵循相同的架构。

2. **可维护性**：`skill-templates.ts` 中的模板函数是单一事实来源。对技能定义的更改会在用户重新运行设置时自动传播给所有用户。

3. **分发**：用户在运行 `openspec artifact-experimental-setup` 时会自动获得 verify 技能，就像所有其他 opsx 技能一样。无需特殊安装步骤。

4. **版本管理**：技能从已安装的 npm 包版本生成，确保 CLI 版本和技能行为之间的一致性。

### 实现方案

#### 1. 模板函数

在 `src/core/templates/skill-templates.ts` 中添加两个模板函数：

```typescript
export function getVerifyChangeSkillTemplate(): SkillTemplate
export function getOpsxVerifyCommandTemplate(): CommandTemplate
```

这两个函数分别返回技能定义（用于 Agent Skills）和斜杠命令定义（用于显式调用）。

#### 2. 设置集成

更新 `src/commands/artifact-workflow.ts` 中的 `artifactExperimentalSetupCommand()`：

- 导入两个模板函数
- 将 verify 添加到 `skills` 数组（第 8 位）
- 将 verify 添加到 `commands` 数组（第 8 位）
- 更新帮助文本以列出 `/opsx:verify`

#### 3. 生成的产物

当用户运行 `openspec artifact-experimental-setup` 时，该命令会创建：

- `.claude/skills/openspec-verify-change/SKILL.md` - Agent Skills 格式
- `.claude/commands/opsx/verify.md` - 斜杠命令格式

两者都从模板函数生成，并自动添加 YAML frontmatter。

### 考虑的替代方案

**替代方案 1：仓库中的静态技能文件**

在 OpenSpec 仓库中创建 `.claude/skills/openspec-verify-change/SKILL.md` 作为静态文件。

**被拒绝的原因：**
- 与所有其他 opsx 技能不一致
- 要求用户手动复制/更新文件
- 版本管理变得复杂（仓库版本 vs 已安装包版本）
- 打破了既定模式

**替代方案 2：独立的 verify 设置命令**

添加 `openspec setup-verify` 作为独立命令。

**被拒绝的原因：**
- 碎片化设置体验
- 用户需要运行多个命令
- 如果将来添加更多技能，不具备可扩展性
- 违背了"一次设置，获取全部"的理念

### 权衡

**优点：**
- 与现有架构一致
- 用户零额外设置负担
- 易于更新和维护
- 自动版本兼容

**缺点：**
- 初始实现稍显复杂（模板函数 + 集成）
- 需要理解设置系统（但这已有文档说明）

### 验证

如果满足以下条件，则实现正确遵循本设计：

1. 两个模板函数存在于 `skill-templates.ts` 中
2. verify 同时出现在 `artifact-workflow.ts` 的 skills 和 commands 数组中
3. 帮助文本提及 `/opsx:verify`
4. 运行 `openspec artifact-experimental-setup` 生成技能和命令文件
5. 构建成功，无 TypeScript 错误
