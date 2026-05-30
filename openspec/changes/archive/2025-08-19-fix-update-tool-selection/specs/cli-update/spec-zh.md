## 新增需求

### 需求：工具无关的更新

update 命令应仅更新现有的 AI 工具配置文件，且不应创建新文件。

#### 场景：更新现有工具文件

- **当** 用户运行 `openspec update`
- **则** 更新每个存在的 AI 工具配置文件（例如 CLAUDE.md、COPILOT.md）
- **且** 不创建缺失的工具配置文件
- **且** 保留 OpenSpec 标记之外的用户内容

### 需求：核心文件始终更新

update 命令应始终更新核心 OpenSpec 文件并显示 ASCII 安全成功消息。

#### 场景：成功更新

- **当** 更新成功完成时
- **则** 用最新模板替换 `openspec/README.md`
- **且** 更新标记内的现有 AI 工具配置文件
- **且** 显示消息："Updated OpenSpec instructions"
