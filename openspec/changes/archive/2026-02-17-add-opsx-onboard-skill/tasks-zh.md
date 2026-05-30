## 1. 添加 skill template

- [x] 1.1 在 `src/core/templates/skill-templates.ts` 中添加 `getOnboardSkillTemplate()` 函数，包含涵盖所有阶段（预检、欢迎、任务选择、探索演示、变更创建、proposal、spec、设计、任务、应用、archive、回顾）的完整入门指导文本
- [x] 1.2 包含用于建议入门级任务的代码分析指令（TODO/FIXME、缺失的错误处理、缺失的测试、type:any、console.log、缺失的验证）
- [x] 1.3 包含解说 schema 指令（在关键过渡点：解释 → 执行 → 展示 → 暂停）
- [x] 1.4 包含范围防护指令，用于引导用户远离过大的任务
- [x] 1.5 包含优雅退出处理指令（用户中途停止、用户只想要命令参考）

## 2. 添加命令 template

- [x] 2.1 在 `src/core/templates/skill-templates.ts` 中添加 `getOpsxOnboardCommandTemplate()` 函数，返回与 skill 相同指令内容的 CommandTemplate

## 3. 注册 template

- [x] 3.1 在 `src/core/shared/skill-generation.ts` 的 `getSkillTemplates()` 数组中添加入门 skill，dirName 为 `openspec-onboard`
- [x] 3.2 在 `src/core/shared/skill-generation.ts` 的 `getCommandTemplates()` 数组中添加入门命令，id 为 `onboard`

## 4. 验证

- [x] 4.1 运行 `pnpm run build` 确保 TypeScript 编译通过
- [x] 4.2 通过在测试目录中运行 `openspec init` 测试 skill 生成，验证入门 skill/命令文件已创建
