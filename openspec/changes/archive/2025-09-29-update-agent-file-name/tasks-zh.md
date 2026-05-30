# 更新 agent 指令文件名 - 任务

## 1. 重命名指令文件
- [x] 将 `openspec/README.md` 重命名为 `openspec/AGENTS.md`
- [x] 更新根引用指向新路径

## 2. 更新 template
- [x] 将 `src/core/templates/readme-template.ts` 重命名为 `agents-template.ts`
- [x] 将导出的常量从 `readmeTemplate` 更新为 `agentsTemplate`

## 3. 调整 CLI 命令
- [x] 修改 `openspec init` 以生成 `AGENTS.md`
- [x] 更新 `openspec update` 以刷新 `AGENTS.md`
- [x] 确保 CLAUDE.md 标记链接到 `@openspec/AGENTS.md`

## 4. 更新 spec
- [x] 修改 `cli-init` spec 以引用 `AGENTS.md`
- [x] 修改 `cli-update` spec 以引用 `AGENTS.md`
- [x] 修改 `openspec-conventions` spec 以在项目结构中包含 `AGENTS.md`

## 5. 验证
- [x] `pnpm test`
