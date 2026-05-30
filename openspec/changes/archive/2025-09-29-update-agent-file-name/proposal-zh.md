# 更新代理指令文件名

## 问题
代理指令位于 `openspec/README.md`，这与传统的项目 README 用法冲突，给工具和贡献者造成混淆。

## 解决方案
将代理指令文件重命名为 `openspec/AGENTS.md`，并更新 OpenSpec 工具以使用新文件名：
- `openspec init` 生成 `AGENTS.md` 而不是 `README.md`
- 模板和代码引用 `AGENTS.md`
- 规范和文档相应更新

## 好处
- 与项目文档清晰分离
- 与其他代理指令文件的命名一致
- 简化工具和项目入门

## 实施
- 重命名指令文件和模板
- 更新 CLI 命令（`init`、`update`）以读/写 `AGENTS.md`
- 调整规范和文档以引用新路径

## 风险
- 现有项目可能仍依赖 `README.md`
- 工具可能遗漏对旧文件名的残留引用

## 成功指标
- `openspec init` 创建 `openspec/AGENTS.md`
- `openspec update` 刷新 `AGENTS.md`
- 所有规范引用 `openspec/AGENTS.md`
