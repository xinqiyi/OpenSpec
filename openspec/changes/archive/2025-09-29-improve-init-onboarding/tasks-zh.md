## 1. planning 与 spec 更新
- [x] 1.1 确认与 `add-multi-agent-init` 的重叠，并协调扩展 schema 流程
- [x] 1.2 更新 `openspec/specs/cli-init/spec.md` 以包含多选入门需求

## 2. 实现
- [x] 2.1 在 `openspec init` 提示中添加多选支持，包括现有工具配置的指示
- [x] 2.2 增强成功消息，总结每个工具已创建/刷新的资源
- [x] 2.3 确保共享指令 template 一致应用（CLAUDE.md、AGENTS.md、斜杠命令）

## 3. 质量
- [x] 3.1 扩展针对 init/update 流程的单元测试，覆盖多选和摘要
- [x] 3.2 在临时目录中执行 `openspec init` 冒烟测试（记录输出）
