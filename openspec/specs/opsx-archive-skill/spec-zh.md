# OPSX Archive Skill spec

## 目的

定义 `/opsx:archive` skill 的预期行为，包括就绪检查、spec 同步提示、archive 执行和面向用户的输出。

## 需求

### 需求：OPSX Archive skill

系统应提供 `/opsx:archive` skill，用于在实验性 workflow 中 archive 已完成的变更。

#### 场景：archive 所有 artifact 已完成的变更

- **WHEN** agent 使用变更名称执行 `/opsx:archive`
- **AND** schema 中的所有 artifact 都已完成
- **AND** 所有任务都已完成
- **THEN** agent 将变更移至 `openspec/changes/archive/YYYY-MM-DD-<name>/`
- **AND** 显示成功消息及 archive 位置

#### 场景：变更选择提示

- **WHEN** agent 执行 `/opsx:archive` 但未指定变更
- **THEN** agent 提示用户从可用变更中选择
- **AND** 仅显示活跃变更（排除 archive/）

### 需求：artifact 完成检查

该 skill 应在 archive 前使用 artifact 图检查 artifact 完成状态。

#### 场景：不完整 artifact 警告

- **WHEN** agent 检查 artifact 状态
- **AND** 一个或多个 artifact 状态不是 `done`
- **THEN** 显示列出不完整 artifact 的警告
- **AND** 提示用户确认是否继续
- **AND** 如果用户确认则继续

#### 场景：所有 artifact 已完成

- **WHEN** agent 检查 artifact 状态
- **AND** 所有 artifact 状态均为 `done`
- **THEN** 继续执行，不发出警告

### 需求：任务完成检查

该 skill 应在 archive 前从 tasks.md 检查任务完成状态。

#### 场景：发现未完成任务

- **WHEN** agent 读取 tasks.md
- **AND** 发现未完成任务（标记为 `- [ ]`）
- **THEN** 显示包含未完成任务数量的警告
- **AND** 提示用户确认是否继续
- **AND** 如果用户确认则继续

#### 场景：所有任务已完成

- **WHEN** agent 读取 tasks.md
- **AND** 所有任务均已完成（标记为 `- [x]`）
- **THEN** 继续执行，不发出任务相关警告

#### 场景：无任务文件

- **WHEN** tasks.md 不存在
- **THEN** 继续执行，不发出任务相关警告

### 需求：spec 同步提示

该 skill 应在 archive 前提示同步 delta spec（如果存在 spec）。

#### 场景：存在 delta spec

- **WHEN** agent 检查 delta spec
- **AND** 变更中存在 `specs/` 目录且包含 spec 文件
- **THEN** 提示用户："此变更包含 delta spec。是否要在 archive 前将其同步到主 spec？"
- **AND** 如果用户确认，执行 `/opsx:sync` 逻辑
- **AND** 无论同步选择如何，继续执行 archive

#### 场景：无 delta spec

- **WHEN** agent 检查 delta spec
- **AND** 不存在 `specs/` 目录或没有 spec 文件
- **THEN** 继续执行，不提示同步

### 需求：archive 流程

该 skill 应将变更移至带有日期前缀的 archive 文件夹。

#### 场景：成功 archive

- **WHEN** archive 一个变更
- **THEN** 如果 `archive/` 目录不存在则创建
- **AND** 使用当前日期生成目标名称 `YYYY-MM-DD-<change-name>`
- **AND** 将整个变更目录移至 archive 位置
- **AND** 在 archive 的变更中保留 `.openspec.yaml` 文件

#### 场景：archive 已存在

- **WHEN** 目标 archive 目录已存在
- **THEN** 失败并显示错误消息
- **AND** 建议重命名现有 archive 或使用不同日期

### 需求：skill 输出

该 skill 应提供关于 archive 操作的清晰反馈。

#### 场景：archive 完成（已同步）

- **WHEN** 同步 spec 后完成 archive
- **THEN** 显示摘要：
 - 已同步的 spec（来自 `/opsx:sync` 输出）
 - 变更已 archive 至位置
 - 所使用的 schema

#### 场景：archive 完成（未同步）

- **WHEN** 未同步 spec 即完成 archive
- **THEN** 显示摘要：
 - 说明 spec 未同步（如适用）
 - 变更已 archive 至位置
 - 所使用的 schema

#### 场景：archive 完成（带警告）

- **WHEN** archive 完成但存在不完整的 artifact 或任务
- **THEN** 包含关于哪些内容不完整的说明
- **AND** 建议检查 archive 是否是有意的
