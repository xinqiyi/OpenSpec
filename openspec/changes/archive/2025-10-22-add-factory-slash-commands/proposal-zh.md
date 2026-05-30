## 为什么
Factory 的 Droid CLI 最近推出了自定义斜杠命令，与其他原生助手集成类似。使用 OpenSpec 的团队希望获得与 Cursor、Windsurf 等其他工具相同的托管 workflow，以便 init/update 能够配置和刷新 Factory 命令，而无需手动设置。

## 变更内容
- 扩展原生工具注册表，使 Factory/Droid 在 `openspec init` 期间与其他斜杠命令集成一起出现。
- 添加共享 template，生成三个 Factory 自定义命令（proposal、应用、archive），并用 OpenSpec 标记包裹以便安全刷新。
- 更新 init 和 update 命令流程，使其在选择或已存在该工具时创建或刷新 Factory 命令文件。
- 刷新 CLI spec 以记录 Factory 支持并对齐验证预期。

## 影响范围
- 受影响的 spec：`specs/cli-init`、`specs/cli-update`
- 受影响的代码（预期）：工具注册表、斜杠命令 template 管理器、init/update 命令辅助函数、文档片段
