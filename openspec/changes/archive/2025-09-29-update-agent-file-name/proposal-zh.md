# 更新 agent 指令文件名

## 问题
agent 指令位于 `openspec/README.md`，这与传统的项目 README 用法冲突，给工具和贡献者造成混淆。

## 解决方案
将 agent 指令文件重命名为 `openspec/AGENTS.md`，并更新 OpenSpec 工具以使用新文件名：
- `openspec init` 生成 `AGENTS.md` 而不是 `README.md`
- template 和代码引用 `AGENTS.md`
- spec 和文档相应更新

## 好处
- 与项目文档清晰分离
- 与其他 agent 指令文件的命名一致
- 简化工具和项目入门

## 实施
- 重命名指令文件和 template
- 更新 CLI 命令（`init`、`update`）以读/写 `AGENTS.md`
- 调整 spec 和文档以引用新路径

## 风险
- 现有项目可能仍依赖 `README.md`
- 工具可能遗漏对旧文件名的残留引用

## 成功指标
- `openspec init` 创建 `openspec/AGENTS.md`
- `openspec update` 刷新 `AGENTS.md`
- 所有 spec 引用 `openspec/AGENTS.md`
