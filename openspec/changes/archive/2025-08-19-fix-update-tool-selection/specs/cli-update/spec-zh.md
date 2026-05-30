## 新增需求

### 需求：工具无关的更新

update 命令应仅更新现有的 AI 工具配置文件，且不应创建新文件。

#### 场景：更新现有工具文件

- **WHEN** 用户运行 `openspec update`
- **THEN** 更新每个存在的 AI 工具配置文件（例如 CLAUDE.md、COPILOT.md）
- **AND** 不创建缺失的工具配置文件
- **AND** 保留 OpenSpec 标记之外的用户内容

### 需求：核心文件始终更新

update 命令应始终更新核心 OpenSpec 文件并显示 ASCII 安全成功消息。

#### 场景：成功更新

- **WHEN** 更新成功完成时
- **THEN** 用最新 template 替换 `openspec/README.md`
- **AND** 更新标记内的现有 AI 工具配置文件
- **AND** 显示消息："Updated OpenSpec instructions"
