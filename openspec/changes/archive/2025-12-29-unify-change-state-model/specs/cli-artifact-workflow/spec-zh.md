# cli-artifact-workflow 规范增量

## 已修改需求

### 需求：Status 命令

系统应显示变更的工件完成状态，包括已搭建（空）的变更。

> **修复了 Bug**：之前通过 `getActiveChangeIds()` 要求 `proposal.md` 必须存在。

#### 场景：显示所有状态

- **当** 用户运行 `openspec status --change <id>`
- **则** 系统显示每个工件及其状态指示符：
  - `[x]` 表示已完成的工件
  - `[ ]` 表示就绪的工件
  - `[-]` 表示被阻塞的工件（列出缺失的依赖）

#### 场景：Status 显示完成摘要

- **当** 用户运行 `openspec status --change <id>`
- **则** 输出包含完成百分比和计数（例如 "2/4 个工件已完成"）

#### 场景：Status JSON 输出

- **当** 用户运行 `openspec status --change <id> --json`
- **则** 系统输出 JSON，包含 changeName、schemaName、isComplete 和 artifacts 数组

#### 场景：已搭建变更的 Status

- **当** 用户对没有工件的变更运行 `openspec status --change <id>`
- **则** 系统显示所有工件及其状态
- **并且** 根工件（无依赖）显示为就绪 `[ ]`
- **并且** 依赖工件显示为被阻塞 `[-]`

#### 场景：缺少变更参数

- **当** 用户运行 `openspec status` 而不带 `--change`
- **则** 系统显示错误，并列出可用变更
- **并且** 包括已搭建的变更（没有 proposal.md 的目录）

#### 场景：未知变更

- **当** 用户运行 `openspec status --change unknown-id`
- **并且** 目录 `openspec/changes/unknown-id/` 不存在
- **则** 系统显示错误，列出所有可用的变更目录

### 需求：Next 命令

系统应显示哪些工件可以创建，包括已搭建的变更。

#### 场景：显示就绪的工件

- **当** 用户运行 `openspec next --change <id>`
- **则** 系统列出其依赖均已满足的工件

#### 场景：无就绪工件

- **当** 所有工件要么已完成要么被阻塞
- **则** 系统指示没有就绪的工件（附带说明）

#### 场景：所有工件已完成

- **当** 变更中的所有工件均已完成
- **则** 系统指示该变更已完成

#### 场景：Next JSON 输出

- **当** 用户运行 `openspec next --change <id> --json`
- **则** 系统输出就绪工件 ID 的 JSON 数组

#### 场景：已搭建变更的 Next

- **当** 用户对没有工件的变更运行 `openspec next --change <id>`
- **则** 系统显示根工件（例如"proposal"）为可创建的就绪状态

### 需求：Instructions 命令

系统应输出用于创建工件的增强指令，包括已搭建的变更。

#### 场景：显示增强指令

- **当** 用户运行 `openspec instructions <artifact> --change <id>`
- **则** 系统输出：
  - 工件元数据（ID、输出路径、描述）
  - 模板内容
  - 依赖状态（已完成/缺失）
  - 解锁的工件（完成后什么变得可用）

#### 场景：Instructions JSON 输出

- **当** 用户运行 `openspec instructions <artifact> --change <id> --json`
- **则** 系统输出与 ArtifactInstructions 接口匹配的 JSON

#### 场景：未知工件

- **当** 用户运行 `openspec instructions unknown-artifact --change <id>`
- **则** 系统显示错误，列出该模式的有效工件 ID

#### 场景：具有未满足依赖的工件

- **当** 用户请求被阻塞工件的指令
- **则** 系统显示指令，并附带关于缺失依赖的警告

#### 场景：已搭建变更的 Instructions

- **当** 用户对已搭建的变更运行 `openspec instructions proposal --change <id>`
- **则** 系统输出用于创建提案的模板和元数据
- **并且** 不要求任何工件已存在
