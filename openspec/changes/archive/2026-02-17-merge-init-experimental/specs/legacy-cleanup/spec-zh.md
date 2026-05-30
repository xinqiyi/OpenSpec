## 新增需求

### 需求：遗留产物检测

系统应能检测来自早期 init 版本的遗留 OpenSpec 产物。

#### 场景：检测遗留配置文件

- **WHEN** 在现有项目上运行 `openspec init`
- **THEN** 系统应检查带有 OpenSpec 标记的配置文件：
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

- **WHEN** 在现有项目上运行 `openspec init`
- **THEN** 系统应检查旧的斜杠命令目录：
 - `.claude/commands/openspec/`
 - `.cursor/commands/openspec/`（注意：旧格式在 commands 根目录使用 `openspec-*.md`）
 - `.windsurf/workflows/openspec-*.md`
 - 以及遗留 SlashCommandRegistry 中所有工具的等效目录

#### 场景：检测遗留 OpenSpec 结构文件

- **WHEN** 在现有项目上运行 `openspec init`
- **THEN** 系统应检查：
 - `openspec/AGENTS.md`
 - `openspec/project.md`（仅用于迁移提示，不删除）
 - 带有 OpenSpec 标记的根目录 `AGENTS.md`

### 需求：遗留清理确认

系统在移除遗留产物前应提示确认。

#### 场景：检测到遗留时提示清理

- **WHEN** 检测到遗留产物
- **THEN** 系统应显示发现的内容
- **AND** 提示："检测到遗留文件。升级并清理？[Y/n]"
- **AND** 默认值为是（用户按回车键）

#### 场景：用户确认清理

- **WHEN** 用户回复 Y 或按回车键
- **THEN** 系统应移除遗留产物
- **AND** 继续进行基于 skill 的设置

#### 场景：用户拒绝清理

- **WHEN** 用户回复 N
- **THEN** 系统应中止初始化
- **AND** 显示消息建议手动清理或使用 `--force` 标志

#### 场景：非交互 schema

- **WHEN** 使用 `--no-interactive` 或在 CI 环境中运行
- **AND** 检测到遗留产物
- **THEN** 系统应以退出码 1 中止
- **AND** 显示检测到的遗留产物
- **AND** 建议以交互方式运行或使用 `--force` 标志

### 需求：配置文件内容的精准移除

系统在从配置文件中移除 OpenSpec 标记时应保留用户内容。

#### 场景：仅包含 OpenSpec 内容的配置文件

- **WHEN** 配置文件仅包含 OpenSpec 标记块（外部空白可接受）
- **THEN** 系统应移除 OpenSpec 标记块
- **AND** 保留文件（即使为空或仅包含空白）
- **AND** 不删除文件（配置文件属于用户项目根目录）

#### 场景：包含混合内容的配置文件

- **WHEN** 配置文件包含 OpenSpec 标记之外的内容
- **THEN** 系统应仅移除 `<!-- OPENSPEC:START -->` 到 `<!-- OPENSPEC:END -->` 之间的块
- **AND** 保留标记之前和之后的所有内容
- **AND** 清理由此产生的多余空行

#### 场景：包含混合内容的根目录 AGENTS.md

- **WHEN** 根目录 `AGENTS.md` 包含 OpenSpec 标记和其他内容
- **THEN** 系统应仅移除 OpenSpec 标记块
- **AND** 保留文件的其余部分

### 需求：遗留目录移除

系统应完整移除遗留斜杠命令目录。

#### 场景：移除旧的斜杠命令目录

- **WHEN** 遗留斜杠命令目录存在（例如 `.claude/commands/openspec/`）
- **THEN** 系统应删除整个目录及其内容
- **AND** 不删除父目录（例如 `.claude/commands/` 保持不变）

#### 场景：移除遗留 AGENTS.md

- **WHEN** `openspec/AGENTS.md` 存在
- **THEN** 系统应删除该文件
- **AND** 不删除 `openspec/` 目录本身

### 需求：project.md 迁移提示

系统应保留 project.md 并显示迁移提示，而不是删除它。

#### 场景：升级过程中 project.md 存在

- **WHEN** 遗留清理期间 `openspec/project.md` 存在
- **THEN** 系统应不删除该文件
- **AND** 系统应在输出中显示迁移提示：
 ```
 需要手动迁移：
 → openspec/project.md 仍然存在
 将有用内容移至 config.yaml 的 "context:" 字段，然后删除
 ```

#### 场景：project.md 迁移理由

- **鉴于** project.md 可能包含用户编写的项目文档
- **AND** config.yaml 的 context 字段服务于相同目的（自动注入到产物中）
- **WHEN** 显示迁移提示时
- **THEN** 用户可以手动迁移或使用 `/opsx:explore` 获取 AI 辅助

### 需求：清理报告

系统应报告已清理的内容。

#### 场景：显示清理摘要

- **WHEN** 遗留清理完成
- **THEN** 系统应显示摘要部分：
 ```
 清理了遗留文件：
 ✓ 已从 CLAUDE.md 中移除 OpenSpec 标记
 ✓ 已移除 .claude/commands/openspec/（已由 /opsx:* 替代）
 ✓ 已移除 openspec/AGENTS.md（不再需要）
 ```
- **并且如果** `openspec/project.md` 存在
- **THEN** 系统应显示单独的迁移部分：
 ```
 需要手动迁移：
 → openspec/project.md 仍然存在
 将有用内容移至 config.yaml 的 "context:" 字段，然后删除
 ```

#### 场景：未检测到遗留文件

- **WHEN** 未找到遗留产物
- **THEN** 系统应不显示清理部分
- **AND** 直接继续执行 skill 设置
