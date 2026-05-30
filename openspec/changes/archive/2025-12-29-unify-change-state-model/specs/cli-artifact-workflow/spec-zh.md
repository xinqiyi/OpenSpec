# cli-artifact-workflow spec delta

## 已修改需求

### 需求：Status 命令

系统应显示变更的 artifact 完成状态，包括已搭建（空）的变更。

> **修复了 Bug**：之前通过 `getActiveChangeIds()` 要求 `proposal.md` 必须存在。

#### 场景：显示所有状态

- **WHEN** 用户运行 `openspec status --change <id>`
- **THEN** 系统显示每个 artifact 及其状态指示符：
 - `[x]` 表示已完成的 artifact
 - `[ ]` 表示就绪的 artifact
 - `[-]` 表示被阻塞的 artifact（列出缺失的依赖）

#### 场景：Status 显示完成摘要

- **WHEN** 用户运行 `openspec status --change <id>`
- **THEN** 输出包含完成百分比和计数（例如 "2/4 个 artifact 已完成"）

#### 场景：Status JSON 输出

- **WHEN** 用户运行 `openspec status --change <id> --json`
- **THEN** 系统输出 JSON，包含 changeName、schemaName、isComplete 和 artifacts 数组

#### 场景：已搭建变更的 Status

- **WHEN** 用户对没有 artifact 的变更运行 `openspec status --change <id>`
- **THEN** 系统显示所有 artifact 及其状态
- **AND** 根 artifact（无依赖）显示为就绪 `[ ]`
- **AND** 依赖 artifact 显示为被阻塞 `[-]`

#### 场景：缺少变更参数

- **WHEN** 用户运行 `openspec status` 而不带 `--change`
- **THEN** 系统显示错误，并列出可用变更
- **AND** 包括已搭建的变更（没有 proposal.md 的目录）

#### 场景：未知变更

- **WHEN** 用户运行 `openspec status --change unknown-id`
- **AND** 目录 `openspec/changes/unknown-id/` 不存在
- **THEN** 系统显示错误，列出所有可用的变更目录

### 需求：Next 命令

系统应显示哪些 artifact 可以创建，包括已搭建的变更。

#### 场景：显示就绪的 artifact

- **WHEN** 用户运行 `openspec next --change <id>`
- **THEN** 系统列出其依赖均已满足的 artifact

#### 场景：无就绪 artifact

- **WHEN** 所有 artifact 要么已完成要么被阻塞
- **THEN** 系统指示没有就绪的 artifact（附带说明）

#### 场景：所有 artifact 已完成

- **WHEN** 变更中的所有 artifact 均已完成
- **THEN** 系统指示该变更已完成

#### 场景：Next JSON 输出

- **WHEN** 用户运行 `openspec next --change <id> --json`
- **THEN** 系统输出就绪 artifact ID 的 JSON 数组

#### 场景：已搭建变更的 Next

- **WHEN** 用户对没有 artifact 的变更运行 `openspec next --change <id>`
- **THEN** 系统显示根 artifact（例如"proposal"）为可创建的就绪状态

### 需求：Instructions 命令

系统应输出用于创建 artifact 的增强指令，包括已搭建的变更。

#### 场景：显示增强指令

- **WHEN** 用户运行 `openspec instructions <artifact> --change <id>`
- **THEN** 系统输出：
 - artifact 元数据（ID、输出路径、描述）
 - template 内容
 - 依赖状态（已完成/缺失）
 - 解锁的 artifact（完成后什么变得可用）

#### 场景：Instructions JSON 输出

- **WHEN** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **THEN** 系统输出与 ArtifactInstructions 接口匹配的 JSON

#### 场景：未知 artifact

- **WHEN** 用户运行 `openspec instructions unknown-artifact --change <id>`
- **THEN** 系统显示错误，列出该 schema 的有效 artifact ID

#### 场景：具有未满足依赖的 artifact

- **WHEN** 用户请求被阻塞 artifact 的指令
- **THEN** 系统显示指令，并附带关于缺失依赖的警告

#### 场景：已搭建变更的 Instructions

- **WHEN** 用户对已搭建的变更运行 `openspec instructions proposal --change <id>`
- **THEN** 系统输出用于创建 proposal 的 template 和元数据
- **AND** 不要求任何 artifact 已存在
