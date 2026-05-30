## 原因

`artifact-experimental-setup` 命令目前将技能输出路径硬编码为 `.claude/skills` 和 `.claude/commands/opsx`。这阻止了其他 AI 编码工具（Cursor、Windsurf、Codex 等）的用户使用 OpenSpec 的技能生成功能。我们需要支持多样化的 AI 编码助手生态系统，每个助手都有自己的技能/指令文件位置和命令 frontmatter 格式约定。

## 变更内容

- 在 `config.ts` 的现有 `AIToolOption` 接口中添加 `skillsDir` 路径配置
- 向 `artifact-experimental-setup` 命令添加必需的 `--tool <tool-id>` 标志
- 使用策略/适配器模式创建通用的命令生成系统：
  - `CommandContent`：工具无关的命令数据（id、name、description、body）
  - `ToolCommandAdapter`：每种工具的格式化（文件路径、frontmatter 格式）
  - `CommandGenerator`：使用 content + adapter 编排生成
- 为清晰起见，需要显式工具选择（无默认值）

## 能力

### 新能力

- `ai-tool-paths`：将 AI 工具 ID 映射到其项目本地技能目录路径的配置
- `command-generation`：具有工具适配器的通用命令生成系统，用于处理格式化差异

### 修改的能力

- `cli-artifact-workflow`：在 setup 命令中添加 `--tool` 标志用于提供商选择

## 影响

- **修改的文件**：
  - `src/core/config.ts` - 用 `skillsDir` 字段扩展 `AIToolOption` 接口
  - `src/commands/artifact-workflow.ts` - 添加 `--tool` 标志，使用提供商路径和适配器
- **新文件**：
  - `src/core/command-generation/types.ts` - CommandContent、ToolCommandAdapter 接口
  - `src/core/command-generation/generator.ts` - 通用命令生成器
  - `src/core/command-generation/adapters/*.ts` - 每种工具的适配器
- **向后兼容性**：现有工作流不受影响——这是一个新的命令设置功能
- **面向用户**：`artifact-experimental-setup` 命令上必需的 `--tool` 标志，用于显式工具选择
