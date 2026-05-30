# CLI 更新 spec 差异

## 修改后的需求

### 需求：斜杠命令更新
更新命令应刷新已配置工具的现有斜杠命令文件而不创建新文件，并确保 OpenCode archive 命令接受变更 ID 参数。

#### 场景：更新 OpenCode 的斜杠命令
- **WHEN** `.opencode/command/` 包含 `openspec-proposal.md`、`openspec-apply.md` 和 `openspec-archive.md` 时
- **THEN** 使用共享 template 刷新每个文件
- **AND** 确保 template 包含相关 workflow 阶段的说明
- **AND** 确保 archive 命令在前置元数据中包含 `$ARGUMENTS` 占位符以接受变更 ID 参数

### 需求：archive 命令参数支持
archive 斜杠命令 template 应支持可选的变更 ID 参数，适用于支持 `$ARGUMENTS` 占位符的工具。

#### 场景：带变更 ID 参数的 archive 命令
- **WHEN** 用户使用变更 ID 调用 `/openspec:archive <change-id>` 时
- **THEN**template 应指示 AI 根据 `openspec list` 验证提供的变更 ID
- **AND** 如果有效，使用提供的变更 ID 进行 archive
- **AND** 如果提供的变更 ID 与可 archive 的变更不匹配，快速失败

#### 场景：无参数的 archive 命令（向后兼容）
- **WHEN** 用户调用 `/openspec:archive` 而未提供变更 ID 时
- **THEN**template 应指示 AI 从上下文中识别变更 ID，或通过运行 `openspec list` 来识别
- **AND** 按现有行为继续（保持向后兼容性）

#### 场景：OpenCode archive template 生成
- **WHEN** 生成 OpenCode archive 斜杠命令文件时
- **THEN** 在前置元数据中包含 `$ARGUMENTS` 占位符
- **AND** 将其包裹在清晰的结构中，如 `<ChangeId>\n $ARGUMENTS\n</ChangeId>`，以指示预期的参数
- **AND** 在 template 主体中包含验证步骤以检查变更 ID 是否有效
