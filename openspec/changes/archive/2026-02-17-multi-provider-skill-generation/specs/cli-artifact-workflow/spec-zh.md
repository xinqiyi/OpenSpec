# cli-artifact-workflow 增量规范

## 目的

为 `artifact-experimental-setup` 命令添加 `--tool` 标志，以支持多提供商。

## 新增需求

### 需求：工具选择标志

`artifact-experimental-setup` 命令应接受 `--tool <tool-id>` 标志以指定目标 AI 工具。

#### 场景：通过标志指定工具

- **当** 用户运行 `openspec artifact-experimental-setup --tool cursor`
- **那么** 技能文件生成在 `.cursor/skills/` 中
- **并且** 命令文件使用 Cursor 的 frontmatter 格式生成

#### 场景：缺少工具标志

- **当** 用户运行 `openspec artifact-experimental-setup` 时未带 `--tool`
- **那么** 系统显示错误，要求提供 `--tool` 标志
- **并且** 在错误消息中列出有效的工具 ID

#### 场景：未知的工具 ID

- **当** 用户运行 `openspec artifact-experimental-setup --tool unknown-tool`
- **并且** 该工具 ID 不在 `AI_TOOLS` 中
- **那么** 系统显示错误，列出有效的工具 ID

#### 场景：没有 skillsDir 的工具

- **当** 用户指定的工具没有配置 `skillsDir`
- **那么** 系统显示错误，指示该工具不支持技能生成

#### 场景：没有命令适配器的工具

- **当** 用户指定的工具有 `skillsDir` 但没有注册命令适配器
- **那么** 技能文件生成成功
- **并且** 命令生成被跳过并显示信息性消息

### 需求：输出消息

设置命令应显示关于生成了什么的清晰输出。

#### 场景：在输出中显示目标工具

- **当** 设置命令成功运行
- **那么** 输出包含目标工具名称（例如"正在为 Cursor 设置..."）

#### 场景：显示生成的路径

- **当** 设置命令完成时
- **那么** 输出列出所有生成的技能文件路径
- **并且** 列出所有生成的命令文件路径（如果适用）

#### 场景：显示跳过的命令消息

- **当** 由于缺少适配器而跳过命令生成
- **那么** 输出包含消息："命令生成已跳过 - 没有适用于 <tool> 的适配器"
