## 原因

并行变更常常触及相同的能力和 `cli-init`/`cli-update` 行为，但当前缺乏机器可读的方式来表达排序、依赖关系或预期的合并顺序。

这导致了三个反复出现的问题：

- 团队无法判断哪个变更应该先落地
- 大型变更难以拆分为安全的可合并片段
- 并行工作可能意外重新引入已被其他变更移除的假设

我们需要轻量级的 planning 元数据和 CLI 指导，以便贡献者能够安全地将计划叠加在一起。

## 变更内容

### 1. 为变更添加轻量级堆叠元数据

扩展变更元数据以支持排序和分解上下文，例如：

- `dependsOn`：必须先落地的变更
- `provides`：此变更暴露的能力标记
- `requires`：此变更所需的能力标记
- `touches`：可能影响的能力/spec 领域（仅供参考；警告信号，非硬性依赖）
- `parent`：用于拆分工作的可选父变更

元数据是可选的，并且向后兼容现有变更。

排序语义：

- `dependsOn` 是执行/archive 排序的权威依据
- `provides`/`requires` 是用于验证和 planning 可见性的能力契约
- `provides`/`requires` 不创建隐式依赖边；作者仍必须通过 `dependsOn` 声明所需的排序

### 2. 添加堆叠感知验证

增强变更验证以尽早发现 planning 问题：

- 缺少依赖项
- 依赖循环
- archive 排序违规（例如，试图在 `dependsOn` 前置变更 archive 之前 archive 某个变更）
- 不匹配的能力标记（例如，活动历史中不存在提供者的 `requires` 标记发出非阻塞警告）
- 当活动变更触及相同能力时发出重叠警告

验证应仅对确定性阻塞因素（例如循环或缺少必需依赖项）失败，并将重叠检查保留为可操作的警告。

### 3. 添加排序可视化命令

添加轻量级 CLI 支持以检查和执行计划顺序：

- `openspec change graph` 显示依赖 DAG/顺序
- `openspec change graph` 首先验证循环；当存在循环时，失败并显示与堆叠感知验证相同的确定性循环错误
- `openspec change next` 建议准备好实施/archive 的无阻塞变更

### 4. 为大型变更添加拆分脚手架

添加辅助 workflow 以将大型 proposal 分解为可堆叠的片段：

- `openspec change split <change-id>` 使用 `parent` + `dependsOn` 搭建子变更脚手架
- 为每个子片段生成最小的 proposal/任务存根
- 将源变更转换为父 planning 容器（不包含重复的子实施任务）
- 对已拆分的源变更重新运行 split 返回确定性的可操作错误，除非传递了 `--overwrite`（别名 `--force`）
- `--overwrite` / `--force` 完全重新生成托管子脚手架存根和元数据链接，替换先前的脚手架内容

### 5. 记录堆叠优先 workflow

更新文档以描述：

- 如何对依赖关系和父/子片段进行建模
- 何时拆分大型变更
- 如何在并行开发期间使用 graph/next 验证信号
- `openspec/changes/IMPLEMENTATION_ORDER.md` 的迁移指导：
 - 机器可读的变更元数据成为 spec 性依赖来源
 - `IMPLEMENTATION_ORDER.md` 在过渡期间保持为可选的叙述性上下文

## 能力

### 新增能力

- `change-stacking-workflow`：用于变更 planning 的依赖感知排序和拆分脚手架

### 修改的能力

- `cli-change`：添加 graph/next/split planning 命令和堆叠感知验证消息
- `change-creation`：在创建或拆分变更时支持父/依赖元数据
- `openspec-conventions`：为变更 proposal 定义可选的堆叠元数据约定

## 影响范围

- `src/core/project-config.ts` 及相关的变更元数据加载解析/验证工具
- `src/core/config-schema.ts`（或专门的变更 schema）用于堆叠元数据验证
- `src/commands/change.ts` 和/或 `src/core/list.ts` 用于 graph/next/split 命令行为
- `src/core/validation/*` 用于依赖循环和重叠检查
- `docs/cli.md`、`docs/concepts.md` 和贡献者指导，用于堆叠感知 workflow
- 元数据解析、图排序、下一项建议和拆分脚手架的测试
