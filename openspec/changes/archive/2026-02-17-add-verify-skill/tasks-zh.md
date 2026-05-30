# 任务：添加 /opsx:verify skill

## 1. skill template 函数
- [x] 1.1 在 skill-templates.ts 中添加 `getVerifyChangeSkillTemplate()`
- [x] 1.2 在 skill-templates.ts 中添加 `getOpsxVerifyCommandTemplate()`

## 2. 与 artifact-experimental-setup 集成
- [x] 2.1 在 artifact-workflow.ts 中导入 verify template 函数
- [x] 2.2 在 artifactExperimentalSetupCommand 的 skills 数组中添加 verify
- [x] 2.3 在 artifactExperimentalSetupCommand 的 commands 数组中添加 verify
- [x] 2.4 在帮助文本输出中添加 verify

## 3. 验证（构建和测试）
- [x] 3.1 验证 TypeScript 编译成功
- [x] 3.2 验证现在包含全部 8 个 skill（之前是 7 个，现在是 8 个）
