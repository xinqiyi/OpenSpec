# legacy-cleanup 规范

## 目的
定义初始化和更新工作流期间检测和清理遗留 OpenSpec 工件的功能。

## 需求
### 需求：遗留工件检测

系统应检测来自先前 init 版本的遗留 OpenSpec 工件。

#### 场景：检测遗留配置文件

- **当** 在现有项目上运行 `openspec init`
- **则** 系统应检查带有 OpenSpec 标记的配置文件：
  - `CLAUDE.md`
  - `.cursorrules`
  - `.windsurfrules`
  - `.clinerules`
  - `.kilocode_rules`
  - `.github/copilot-instructions.md`
  - `.amazonq/instructions.md`
  - `CODEBUDDY.md`
  - `IFLOW.md`
  - 以及来自遗留 ToolRegistry 的所有其他工具配置文件

#### 场景：检测遗留斜杠命令目录

- **当** 在现有项目上运行 `openspec init`
- **则** 系统应检查旧的斜杠命令目录：
  - `.claude/commands/openspec/`
  - `.cursor/commands/openspec/`（注意：旧格式在 commands 根目录使用 `openspec-*.md`）
  - `.windsurf/workflows/openspec-*.md`
  - 以及遗留 SlashCommandRegistry 中所有工具的等效目录

#### 场景：检测遗留 OpenSpec 结构文件

- **当** 在现有项目上运行 `openspec init`
- **则** 系统应检查：
  - `openspec/AGENTS.md`
  - `openspec/project.md`（仅用于迁移消息，不删除）
  - 带有 OpenSpec 标记的根目录 `AGENTS.md`

### 需求：遗留清理确认

系统应在移除遗留工件前提示确认。

#### 场景：检测到遗留时提示清理

- **当** 检测到遗留工件
- **则** 系统应展示发现的内容
- **且** 提示："检测到遗留文件。升级并清理？[Y/n]"
- **且** 如果用户按回车键，默认为是

#### 场景：用户确认清理

- **当** 用户响应 Y 或按回车键
- **则** 系统应移除遗留工件
- **且** 继续基于技能的设置

#### 场景：用户拒绝清理

- **当** 用户响应 N
- **则** 系统应中止初始化
- **且** 显示消息，建议手动清理或使用 `--force` 标志

#### 场景：非交互模式

- **当** 使用 `--no-interactive` 运行或在 CI 环境中
- **且** 检测到遗留工件
- **则** 系统应以退出码 1 中止
- **且** 显示检测到的遗留工件
- **且** 建议以交互方式运行或使用 `--force` 标志

### 需求：配置文件内容的精准移除

系统应在从配置文件中移除 OpenSpec 标记时保留用户内容。

#### 场景：仅包含 OpenSpec 内容的配置文件

- **当** 配置文件仅包含 OpenSpec 标记块（外部空白可以接受）
- **则** 系统应移除 OpenSpec 标记块
- **且** 保留文件（即使为空或仅包含空白）
- **且** 不删除文件（配置文件属于用户的项目根目录）

#### 场景：包含混合内容的配置文件

- **当** 配置文件包含 OpenSpec 标记之外的内容
- **则** 系统应仅移除 `<!-- OPENSPEC:START -->` 到 `<!-- OPENSPEC:END -->` 之间的块
- **且** 保留标记前后的所有内容
- **且** 清理由此产生的双重空行

#### 场景：包含混合内容的根目录 AGENTS.md

- **当** 根目录 `AGENTS.md` 同时包含 OpenSpec 标记和其他内容
- **则** 系统应仅移除 OpenSpec 标记块
- **且** 保留文件的其他部分

### 需求：遗留目录移除

系统应完全移除遗留的斜杠命令目录。

#### 场景：移除旧的斜杠命令目录

- **当** 遗留斜杠命令目录存在（例如 `.claude/commands/openspec/`）
- **则** 系统应删除整个目录及其内容
- **且** 不删除父目录（例如 `.claude/commands/` 保留）

#### 场景：移除遗留 AGENTS.md

- **当** `openspec/AGENTS.md` 存在
- **则** 系统应删除该文件
- **且** 不删除 `openspec/` 目录本身

### 需求：project.md 迁移提示

系统应保留 project.md 并显示迁移提示，而非删除它。

#### 场景：升级期间 project.md 存在

- **当** 遗留清理期间 `openspec/project.md` 存在
- **则** 系统不应删除该文件
- **且** 系统应在输出中显示迁移提示：
  ```
  需要手动迁移：
    → openspec/project.md 仍然存在
      将有用的内容移动到 config.yaml 的 "context:" 字段，然后删除
  ```

#### 场景：project.md 迁移理由

- **给定** project.md 可能包含用户编写的项目文档
- **且** config.yaml 的 context 字段提供相同的目的（自动注入到工件中）
- **当** 显示迁移提示时
- **则** 用户可以手动迁移或使用 `/opsx:explore` 获得 AI 帮助

### 需求：清理报告

系统应报告已清理的内容。

#### 场景：显示清理摘要

- **当** 遗留清理完成
- **则** 系统应显示摘要部分：
  ```
  已清理的遗留文件：
    ✓ 已从 CLAUDE.md 移除 OpenSpec 标记
    ✓ 已移除 .claude/commands/openspec/（已替换为 /opsx:*）
    ✓ 已移除 openspec/AGENTS.md（不再需要）
  ```
- **且如果** `openspec/project.md` 存在
- **则** 系统应显示单独的迁移部分：
  ```
  需要手动迁移：
    → openspec/project.md 仍然存在
      将有用的内容移动到 config.yaml 的 "context:" 字段，然后删除
  ```

#### 场景：未检测到遗留

- **当** 未找到遗留工件
- **则** 系统不应显示清理部分
- **且** 直接进行技能设置
