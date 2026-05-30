## 背景

目前 `openspec init` 和 `openspec experimental` 是两个独立的命令，具有不同的用途：

- **init**：创建 `openspec/` 目录，生成 `AGENTS.md`/`project.md`，配置工具配置文件（`CLAUDE.md` 等），生成旧的斜杠命令（`/openspec:proposal` 等）
- **experimental**：生成技能（每个工具 9 个），生成 opsx 斜杠命令（`/opsx:new` 等），创建 `config.yaml`

基于技能的工作流（experimental）是我们未来的方向，因此我们通过将其合并到 `init` 中使其成为默认行为。

## 目标 / 非目标

**目标：**
- 单一的 `openspec init` 命令，设置完整的基于技能的工作流
- 为具有遗留制品的现有用户提供清晰的迁移路径
- 移除所有与配置文件和旧斜杠命令相关的代码
- 保留 experimental 的精美 UX（动画欢迎界面、可搜索多选）

**非目标：**
- 同时支持两种工作流
- 提供使用旧工作流的选项
- 对 `/openspec:*` 命令的向后兼容（破坏性变更）

## 决策

### 决策 1：合并到 init，而非 experimental

**选择**: 重写 `init` 使其执行 `experimental` 的功能，然后删除 `experimental`。

**理由**: `init` 是规范的设置命令。用户期望 `init` 设置项目。`experimental` 始终是临时的。

**考虑过的替代方案**：
- 保留 `experimental` 作为主要命令 → 作为默认行为名称令人困惑
- 创建新命令 → 不必要，`init` 已存在

### 决策 2：带 Y/N 提示的遗留清理

**选择**: 检测遗留制品，显示发现的内容，提示"检测到遗留文件。升级并清理？[Y/n]"，确认后移除。

**理由**: 用户应知道正在移除什么。一个 Y/N 简单且果断。无需多个选项。

**考虑过的替代方案**：
- 多个选项（保留/移除/取消）→ 过于复杂
- 静默移除 → 用户可能会感到意外
- 仅警告而不移除 → 留下垃圾

### 决策 3：精确移除遗留内容

**选择**: 对于混合内容的文件（OpenSpec 标记 + 用户内容），仅移除 OpenSpec 标记块。对于 100% OpenSpec 内容的文件，删除整个文件。

**理由**: 尊重用户自定义。CLAUDE.md 可能包含 OpenSpec 之外的其他指令。

**边界情况**：
- **混合内容的配置文件**: 仅移除 `<!-- OPENSPEC:START -->` 到 `<!-- OPENSPEC:END -->` 块
- **100% OpenSpec 内容的配置文件**: 完全删除文件（检查标记外内容是否为空/空白）
- **旧的斜杠命令目录**（`.claude/commands/openspec/`）: 删除整个目录（我们的）
- **`openspec/AGENTS.md`**: 删除（我们的）
- **根目录 `AGENTS.md`**: 仅移除 OpenSpec 标记块，保留其余内容

### 决策 6：保留 project.md 并显示迁移提示

**选择**: 不要自动删除 `openspec/project.md`。保留它并显示消息，引导用户手动将内容迁移到 `config.yaml` 的 `context:` 字段。

**理由**：
- `project.md` 可能包含有价值的用户编写的项目文档
- 新工作流使用 `config.yaml.context` 实现相同目的（自动注入到制品中）
- 自动删除会丢失用户内容；自动迁移很复杂（需要 LLM 压缩）
- 用户可以手动迁移或使用 `/opsx:explore` 获取 AI 帮助

**迁移路径**：
1. 在遗留清理期间，检测 `openspec/project.md` 但不删除
2. 在输出中显示："openspec/project.md 仍然存在 - 将内容迁移到 config.yaml 的 context: 字段，然后删除"
3. 用户手动迁移或在探索模式下询问 Claude："帮我将 project.md 迁移到 config.yaml"
4. 用户在准备好时删除 project.md

**为什么不自动迁移？**
- `project.md` 冗长（章节、标题、占位符）
- `config.yaml.context` 应简洁且密集
- LLM 压缩是理想的但增加了 init 的复杂性和不确定性
- 手动迁移让用户决定什么真正重要

### 决策 4：experimental 的隐藏别名

**选择**: 保留 `openspec experimental` 作为委托给 `init` 的隐藏命令。

**理由**: 学习过 `experimental` 的用户在过渡期间仍可使用它。隐藏意味着它不会显示在帮助中。

### 决策 5：重用现有基础设施

**选择**: 重用 experimental 中的技能模板、命令适配器、欢迎界面和多选。

**理由**: 已经构建并可工作。只需从 init 而非 experimental 中调用它们。

## 风险 / 权衡

| 风险 | 缓解措施 |
|------|------------|
| 具有自定义 `/openspec:*` 命令的用户会丢失它们 | 在发布说明中记录；旧命令在 git 历史中 |
| 混合内容检测可能不完美 | 保守方法：如果不确定，保留文件并警告 |
| 用户因缺少配置文件感到困惑 | 在 init 输出中清晰说明更改内容 |
| `openspec update` 可能损坏 | 审查并更新 `update` 命令以适配新结构 |

## 架构

### init 创建的内容（合并后）

```
openspec/
  ├── config.yaml           # 模式设置（来自 experimental）
  ├── specs/                # 空，用于用户的规范
  └── changes/              # 空，用于用户的变更
      └── archive/

.<tool>/skills/             # 每个选定工具 9 个技能
  ├── openspec-explore/SKILL.md
  ├── openspec-new-change/SKILL.md
  ├── openspec-continue-change/SKILL.md
  ├── openspec-apply-change/SKILL.md
  ├── openspec-ff-change/SKILL.md
  ├── openspec-verify-change/SKILL.md
  ├── openspec-sync-specs/SKILL.md
  ├── openspec-archive-change/SKILL.md
  └── openspec-bulk-archive-change/SKILL.md

.<tool>/commands/opsx/      # 每个选定工具 9 个斜杠命令
  ├── explore.md
  ├── new.md
  ├── continue.md
  ├── apply.md
  ├── ff.md
  ├── verify.md
  ├── sync.md
  ├── archive.md
  └── bulk-archive.md
```

### init 不再创建的内容

- `CLAUDE.md`、`.cursorrules`、`.windsurfrules` 等（配置文件）
- `openspec/AGENTS.md`
- `openspec/project.md`
- 根目录 `AGENTS.md` 存根
- `.claude/commands/openspec/`（旧斜杠命令）

### 遗留检测目标

| 制品类型 | 检测方法 | 移除方法 |
|--------------|------------------|----------------|
| 配置文件（CLAUDE.md 等） | 文件存在且包含 OpenSpec 标记 | 移除标记块；之后若为空则删除文件 |
| 旧斜杠命令目录 | 目录存在于 `.<tool>/commands/openspec/` | 删除整个目录 |
| openspec/AGENTS.md | 文件存在于 `openspec/AGENTS.md` | 删除文件 |
| openspec/project.md | 文件存在于 `openspec/project.md` | **保留** - 仅显示迁移提示 |
| 根目录 AGENTS.md | 文件存在于 `AGENTS.md` 且包含 OpenSpec 标记 | 移除标记块；之后若为空则删除文件 |

### 要移除的代码

- `src/core/configurators/` - 整个目录（ToolRegistry、所有配置生成器）
- `src/core/configurators/slash/` - 整个目录（SlashCommandRegistry、旧命令生成器）
- `src/core/templates/slash-command-templates.ts` - 旧的 `/openspec:*` 内容
- `src/core/templates/claude-template.ts`
- `src/core/templates/cline-template.ts`
- `src/core/templates/costrict-template.ts`
- `src/core/templates/agents-template.ts`
- `src/core/templates/agents-root-stub.ts`
- `src/core/templates/project-template.ts`
- `src/commands/experimental/` - 整个目录（合并到 init）
- 相关的测试文件

### 要迁移到 init 的代码

- 动画欢迎界面（`src/ui/welcome-screen.ts`）- 保留，从 init 调用
- 可搜索多选（`src/prompts/searchable-multi-select.ts`）- 保留，从 init 调用
- 技能模板（`src/core/templates/skill-templates.ts`）- 保留
- 命令生成（`src/core/command-generation/`）- 保留
- 工具状态检测（来自 `experimental/setup.ts`）- 移至 init

## 未决问题

1. **`openspec update` 会怎样？** - 已解决

   **当前行为**：通过 `ToolRegistry` 更新 `openspec/AGENTS.md`、配置文件（`CLAUDE.md` 等），以及通过 `SlashCommandRegistry` 更新旧的斜杠命令（`/openspec:*`）。

   **新行为**：重写为刷新技能和 opsx 命令：
   - 检测哪些工具已安装技能（检查 `.claude/skills/openspec-*/` 等）
   - 使用 `skill-templates.ts` 刷新每个已安装工具的所有 9 个技能文件
   - 使用 `command-generation/` 适配器刷新每个已安装工具的所有 9 个 opsx 命令文件
   - 移除对 `ToolRegistry`、`SlashCommandRegistry`、`agentsTemplate` 的导入
   - 更新输出消息以反映技能/命令而非配置文件

   **关键原则**：与当前 update 相同 - 仅刷新现有工具，不添加新工具。

2. **是否应保留 `openspec schemas` 和其他 experimental 子命令？** - 已解决

   **决策**：是的，保留它们。从所有子命令（status、instructions、schemas 等）中移除"[Experimental]"标签。参见任务 4.3。
