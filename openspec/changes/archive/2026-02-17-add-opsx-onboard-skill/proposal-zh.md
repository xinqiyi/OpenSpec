## 为什么

运行 `openspec init` 的用户只留下了文件，但没有使用该系统的清晰路径。"我已经设置好 OpenSpec"和"我理解 workflow"之间存在差距。入门 skill 将引导用户在其实代码库中的真实任务上完成第一个完整的变更周期，通过实践来教学 workflow。

## 变更内容

- 添加新的 `/opsx:onboard` skill，引导用户完成他们的第一个 OpenSpec 变更
- 为编辑器集成添加对应的斜杠命令 template
- 该 skill 将：
 - 分析用户的代码库以建议范围适中的入门级任务
 - 贯穿整个 workflow（探索 → 新建 → proposal → spec → 设计 → 任务 → 应用 → archive）
 - 在每一步发生时提供解说
 - 结果是用户代码库中的一个真实的、已实现的变更

## 能力

### 新能力
- `opsx-onboard-skill`：引导用户通过解说和代码库感知的任务建议完成第一个完整 OpenSpec workflow 周期的入门 skill

### 被修改的能力
<!-- 没有现有 spec 被修改——这纯粹是新增内容 -->

## 影响

- `src/core/templates/skill-templates.ts`：添加 `getOnboardSkillTemplate()` 和 `getOpsxOnboardCommandTemplate()` 函数
- `src/core/shared/skill-generation.ts`：在 `getSkillTemplates()` 和 `getCommandTemplates()` 中注册新的 skill 和命令 template
- 运行 `openspec init` 或 `openspec update` 的用户将获得新的 skill/命令文件生成
