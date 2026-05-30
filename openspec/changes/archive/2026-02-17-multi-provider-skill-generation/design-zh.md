## 上下文

`artifact-experimental-setup` 命令为 AI 编码助手生成 skill 文件和 opsx 斜杠命令。目前它硬编码了到 `.claude/skills` 和 `.claude/commands/opsx` 的路径。

`config.ts` 中现有的 `AI_TOOLS` 数组列出了 22 个 AI 工具，但缺少路径信息。另外还有一个现有的 `SlashCommandConfigurator` 系统用于旧的 workflow 命令，但它与旧的 3 个命令（proposal、apply、archive）紧密耦合，无法轻松扩展以支持 9 个 opsx 命令。

每个 AI 工具都有：
- 不同的 skill 目录约定（`.claude/skills/`、`.cursor/skills/` 等）
- 不同的命令文件路径（`.claude/commands/opsx/`、`.cursor/commands/` 等）
- 不同的 frontmatter 格式（YAML 键，结构因工具而异）

## 目标 / 非目标

**目标：**
- 支持任何遵循 Agent Skills spec 的 AI 工具的 skill 生成
- 支持通过适配器进行工具特定格式的命令生成
- 需要显式工具选择（无默认值）
- 创建通用的、可扩展的命令生成系统

**非目标：**
- 为除 Codex 以外的工具进行全局路径安装（Codex 目前使用绝对适配器路径）
- 在单个命令中多工具生成（未来增强）
- 与现有的 SlashCommandConfigurator 统一（目前保持独立系统）

## 决策

### 1. 向 `AIToolOption` 接口添加 `skillsDir`

**决策**：向现有接口添加单个 `skillsDir` 字段。不添加 `commandsDir` 或 `globalSkillsDir`。

```typescript
interface AIToolOption {
 name: string;
 value: string;
 available: boolean;
 successLabel?: string;
 skillsDir?: string; // 例如 '.claude' - /skills 后缀遵循 Agent Skills spec
}
```

**理由**：
- skill 遵循 Agent Skills spec：`<toolDir>/skills/` - 后缀是标准化的
- 命令需要每种工具的格式化，由适配器处理（而不是简单的路径）
- 支持全局路径——Codex 适配器通过 os.homedir() 返回绝对路径

### 2. 命令生成的策略/适配器 schema

**决策**：创建带有工具特定适配器的通用命令生成系统。

```text
┌─────────────────────────────────────────────────────────────────┐
│ CommandContent │
│ （工具无关：id、name、description、category、tags、body） │
└─────────────────────────────────────────────────────────────────┘
 │
 ▼
┌─────────────────────────────────────────────────────────────────┐
│ generateCommand(content, adapter) │
└─────────────────────────────────────────────────────────────────┘
 │
 ┌───────────────┼───────────────┐
 ▼ ▼ ▼
 ┌──────────┐ ┌──────────┐ ┌──────────┐
 │ Claude │ │ Cursor │ │ Windsurf │
 │ 适配器 │ │ 适配器 │ │ 适配器 │
 └──────────┘ └──────────┘ └──────────┘
```

**接口：**

```typescript
// 工具无关的命令数据
interface CommandContent {
 id: string; // 例如 'explore', 'new', 'apply'
 name: string; // 例如 'OpenSpec Explore'
 description: string; // 例如 '进入探索 schema...'
 category: string; // 例如 'OpenSpec'
 tags: string[]; // 例如 ['openspec', 'explore']
 body: string; // 命令指令
}

// 每种工具的格式化策略
interface ToolCommandAdapter {
 toolId: string;
 getFilePath(commandId: string): string;
 formatFile(content: CommandContent): string;
}
```

**理由**：
- 将"生成什么"与"如何格式化"分离
- 每种工具的 frontmatter 特性封装在其适配器中
- 通过实现适配器接口轻松添加新工具
- 主体内容在所有工具间共享

**考虑的替代方案**：扩展现有的 SlashCommandConfigurator
- 已拒绝：与旧 3 个命令紧密耦合，需要重大重构

### 3. 适配器注册表 schema

**决策**：创建类似于现有 `SlashCommandRegistry` 的 `CommandAdapterRegistry`。

```typescript
class CommandAdapterRegistry {
 private static adapters: Map<string, ToolCommandAdapter> = new Map();

 static get(toolId: string): ToolCommandAdapter | undefined;
 static getAll(): ToolCommandAdapter[];
}
```

**理由**：
- 与现有代码库 schema 一致
- 通过工具 ID 轻松查找
- 集中注册

### 4. 必需的 tool 标志

**决策**：需要 `--tool` 标志——如果省略则报错。

**理由**：
- 显式工具选择避免假设
- 与项目不提供默认值的约定一致
- 用户必须有意识地选择目标工具

## 风险 / 权衡

**[风险] 适配器维护负担** → 每个新工具都需要一个适配器。通过简单接口缓解——大多数适配器约 20 行代码。

**[风险] Frontmatter 格式漂移** → 工具可能更改其格式。通过将格式封装在适配器中缓解——单个更新点。

**[权衡] 两个命令系统** → 旧的 SlashCommandConfigurator 和新的 CommandAdapterRegistry 共存。目前可以接受——如果需要，以后可以统一。

**[权衡] skillsDir 可选** → 未配置 skillsDir 的工具将报错。可以接受——我们在测试工具时添加路径。

## 实施方法

1. 向 `AIToolOption` 添加 `skillsDir` 并为已知工具填充
2. 创建 `CommandContent` 和 `ToolCommandAdapter` 接口
3. 为 Claude、Cursor、Windsurf 实现适配器（从 3 个开始）
4. 创建 `CommandAdapterRegistry`
5. 创建 `generateCommand()` 函数
6. 更新 `artifact-experimental-setup` 以使用新系统
7. 添加带有验证的 `--tool` 标志
