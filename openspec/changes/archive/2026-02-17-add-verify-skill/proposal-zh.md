# 变更：添加 /opsx:verify 技能

## 原因

用户需要一种方法来验证他们的实现与实际请求是否匹配，然后才能归档变更。目前，没有系统化的方式来检查：
- 所有任务是否真正完成
- 实现是否覆盖了所有规范需求和场景
- 实现是否遵循了设计决策
- 代码是否连贯且合理

有用户请求："我们能否有一个 :verify 来确保实现与请求的内容匹配？"

## 变更内容

- 在 `skill-templates.ts` 中添加 `getVerifyChangeSkillTemplate()` 函数
- 在 `skill-templates.ts` 中添加 `getOpsxVerifyCommandTemplate()` 函数
- 将 verify 技能集成到 `artifact-workflow.ts` 的 `artifactExperimentalSetupCommand` 中
- 在设置命令的 skills 和 commands 数组中添加 verify
- 更新帮助文本，在可用命令列表中包含 `/opsx:verify`
- 创建 `opsx-verify-skill` 能力规范

## 验证维度

该技能从三个维度进行验证：

1. **完整性** - 所有任务是否完成？所有规范是否已处理？
2. **正确性** - 实现是否与规范匹配？场景是否已覆盖？
3. **连贯性** - 实现是否合理？是否遵循了 design.md？

## 输出格式

生成优先级报告，包含：
- 摘要评分卡（任务、规范、设计遵循度）
- 关键问题优先（归档前必须修复）
- 警告其次（应该修复）
- 建议最后（最好有）
- 针对每个问题的可操作修复建议

## 影响范围

- 受影响的规范：新的 `opsx-verify-skill` 规范
- 受影响的代码：
  - `src/core/templates/skill-templates.ts` - 新增 2 个模板函数
  - `src/commands/artifact-workflow.ts` - 将 verify 集成到实验性设置中
- 生成的产物：用户运行 `openspec artifact-experimental-setup` 时：
  - 创建 `.claude/skills/openspec-verify-change/SKILL.md`
  - 创建 `.claude/commands/opsx/verify.md`
- 相关技能：与 `/opsx:apply` 配合使用，在 `/opsx:archive` 之前
