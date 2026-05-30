# 更新 OpenSpec 代理指令

## 为什么

当前的 OpenSpec 代理指令需要更新，以遵循 AI 助手指令的最佳实践（简洁、清晰、消除歧义），确保 CLI 命令与实际实现保持同步，并正确记录代理应遵循的三阶段工作流模式。

## 变更内容

### 核心结构改进
- **将三阶段工作流前置**作为主要心智模型：
  1. 创建变更提案（proposal.md、规范差异、design.md、tasks.md）
  2. 实施变更提案：
     - 首先阅读 proposal.md 以了解变更内容
     - 如果存在 design.md，阅读它以获取技术背景
     - 阅读 tasks.md 以获取实施检查清单
     - 逐个完成任务
     - 每完成一个任务立即标记完成
  3. 归档变更提案（部署后使用 archive 命令）
- **将指令长度减少 50%**，同时保留所有关键信息
- **按清晰层级重构**：核心工作流 → 快速入门 → 命令 → 详情 → 边界情况

### 决策清晰度增强
- **添加清晰的决策树**用于常见场景（缺陷 vs 功能、是否需要提案）
- **移除模糊条件**，避免混淆代理的决策
- **添加"执行任何任务之前"检查清单**用于上下文收集
- **添加"创建规范之前"规则** - 始终先检查现有规范，避免重复

### CLI 文档更新
- **完整的命令文档**，包含所有当前功能：
  - `openspec init [path]` - 在项目中初始化 OpenSpec
  - `openspec list` - 列出所有活跃变更（默认）
  - `openspec list --specs` - 列出所有规范
  - `openspec show [item]` - 显示变更或规范（自动检测）
  - `openspec show` - 交互式选择模式
  - `openspec diff [change]` - 显示变更的规范差异
  - `openspec validate [item]` - 验证变更或规范
  - `openspec archive [change]` - 部署后归档已完成的变更
  - `openspec update [path]` - 更新 OpenSpec 指令文件
- **记录所有标志和选项**：
  - `--json` 输出格式，用于程序化使用
  - `--type change|spec` 用于消除歧义
  - `--skip-specs` 用于仅工具归档
  - `--strict` 用于严格验证模式
  - `--no-interactive` 用于禁用交互提示
- **移除已弃用的命令引用**（名词优先模式，如 `openspec change show`）
- **为每个命令变体添加具体示例**
- **记录调试命令**：
  - `openspec show [change] --json --deltas-only` 用于检查差异
  - `openspec validate [change] --strict` 用于全面验证

### 规范文件结构文档
- **完整的规范文件示例**展示正确的结构：
  ```markdown
  ## ADDED Requirements
  ### Requirement: 明确的需求陈述
  系统应提供该功能...

  #### Scenario: 描述性场景名称
  - **WHEN** 条件发生时
  - **THEN** 预期结果
  - **AND** 附加结果
  ```
- **场景格式要求**（关键 - 最常见的错误）：
  - 必须使用 `#### Scenario:` 标题（4 个井号）
  - 不能使用项目符号列表或粗体文本
  - 每个需求必须至少有一个场景
- **差异文件位置** - 清晰说明：
  - 规范文件放在 `changes/{name}/specs/` 目录下
  - 差异从这些文件中自动提取
  - 使用操作前缀：ADDED、MODIFIED、REMOVED、RENAMED

### 故障排查部分
- **常见错误和解决方案**：
  - "Change must have at least one delta" → 检查 specs/ 目录是否存在且包含 .md 文件
  - "Requirement must have at least one scenario" → 检查场景是否使用 `#### Scenario:` 格式
  - 静默场景解析失败 → 验证确切的标题格式
- **差异检测调试**：
  - 使用 `openspec show [change] --json --deltas-only` 检查解析的差异
  - 检查规范文件是否包含操作前缀（## ADDED Requirements）
  - 验证 specs/ 子目录结构
- **验证最佳实践**：
  - 始终使用 `--strict` 标志进行全面检查
  - 使用 JSON 输出进行调试：`--json | jq '.deltas'`

### 代理特定改进
- **实施工作流** - 清晰的分步过程：
  1. 阅读 proposal.md 了解要构建的内容
  2. 阅读 design.md（如果存在）了解技术决策
  3. 阅读 tasks.md 获取实施检查清单
  4. 按顺序逐个实施任务
  5. 立即标记每个任务完成：`- [x] 任务完成`
  6. 绝不跳过或批量标记任务完成
- **规范发现工作流** - 创建新规范前始终检查现有规范：
  - 使用 `openspec list --specs` 查看所有当前规范
  - 创建前检查能力是否已存在
  - 优先修改现有规范而非创建重复规范
- **工具选择矩阵** - 何时使用 Grep vs Glob vs Read
- **错误恢复模式** - 如何处理常见失败
- **上下文管理指南** - 开始任务前应阅读的内容
- **验证工作流** - 如何确认变更是正确的

### 最佳实践部分
- **简洁** - 适当时使用一行回答
- **具体** - 使用确切的文件路径和行号（file.ts:42）
- **从简单开始** - 默认少于 100 行、单文件实现
- **证明复杂性** - 任何优化都需要数据/指标

## 影响

- 受影响的规范：无（这是工具/文档变更）
- 受影响的代码：
  - `src/core/templates/claude-template.ts` - 更新 CLAUDE.md 模板
- 受影响的文档：
  - `openspec/README.md` - 主要 OpenSpec 指令
  - 由 `openspec init` 命令生成的 CLAUDE.md 文件

注意：这是工具/基础设施变更，不需要规范更新。归档时，使用 `openspec archive update-agent-instructions --skip-specs`。
