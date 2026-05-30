# CLI Archive 命令 spec

## 目的
archive 命令将已完成的变更从活跃变更目录移动到 archive 文件夹，采用基于日期的命名，遵循 OpenSpec 约定。

## 命令语法
```bash
openspec archive [change-name] [--yes|-y] [--skip-specs]
```

选项：
- `--yes`、`-y`：跳过确认提示（用于自动化）
- `--skip-specs`：完全跳过 spec 更新操作（适用于没有 spec 修改的变更）

## 行为

### 需求：变更选择

命令应同时支持交互式和直接变更选择方法。

#### 场景：交互式选择

- **WHEN** 未提供变更名称
- **THEN** 显示可用变更的交互式列表（排除 archive/）
- **AND** 允许用户选择一个

#### 场景：直接选择

- **WHEN** 提供了变更名称
- **THEN** 直接使用该变更
- **AND** 验证其存在

### 需求：任务完成检查

命令应在 archive 前验证任务完成状态，以防止过早 archive。

#### 场景：发现未完成的任务

- **WHEN** 发现未完成的任务（标记为 `- [ ]`）
- **THEN** 向用户显示所有未完成的任务
- **AND** 提示确认是否继续
- **AND** 出于安全考虑默认选择"否"

#### 场景：所有任务完成

- **WHEN** 所有任务完成或不存在 tasks.md
- **THEN** 无需提示继续执行 archive

### 需求：archive 过程

archive 操作应遵循结构化过程，安全地将变更移至 archive。

#### 场景：执行 archive

- **WHEN** archive 一个变更
- **THEN** 执行以下步骤：
 1. 如果 archive/ 目录不存在则创建
 2. 使用当前日期生成目标名称 `YYYY-MM-DD-[change-name]`
 3. 检查目标目录是否已存在
 4. 除非提供了 `--skip-specs`，否则从变更的未来状态 spec 更新主 spec（见下面的 spec 更新过程）
 5. 将整个变更目录移动到 archive 位置

#### 场景：archive 已存在

- **WHEN** 目标 archive 已存在
- **THEN** 失败并显示错误消息
- **AND** 不覆盖现有 archive

#### 场景：成功 archive

- **WHEN** 移动成功
- **THEN** 显示成功消息，包含 archive 名称和已更新的 spec 列表（如果有）

### 需求：spec 更新过程

在将变更移至 archive 之前，命令应更新主 spec 以反映已部署的现实，除非提供了 `--skip-specs` 标志。

#### 场景：跳过 spec 更新

- **WHEN** 提供了 `--skip-specs` 标志
- **THEN** 跳过所有 spec 发现和更新操作
- **AND** 直接进入将变更移至 archive
- **AND** 显示指示已跳过 spec 的消息

#### 场景：从变更更新 spec

- **WHEN** 变更在 `changes/[name]/specs/` 中包含 spec AND 未提供 `--skip-specs`
- **THEN** 执行以下步骤：
 1. 通过与现有 spec 比较分析哪些 spec 将受影响
 2. 向用户显示 spec 更新摘要（见下面的确认行为）
 3. 除非提供了 `--yes` 标志，否则提示确认
 4. 如果确认，对于变更目录中的每个能力 spec：
 - 将 spec 从 `changes/[name]/specs/[capability]/spec.md` 复制到 `openspec/specs/[capability]/spec.md`
 - 如果目标目录结构不存在则创建
 - 覆盖现有的 spec 文件（spec 代表当前现实，变更 spec 是新现实）
 - 跟踪哪些 spec 已更新以用于成功消息

#### 场景：变更中没有 spec

- **WHEN** 变更中不存在 spec AND 未提供 `--skip-specs`
- **THEN** 跳过 spec 更新步骤
- **AND** 继续执行 archive

### 需求：确认行为

spec 更新确认应在应用之前提供对变更的清晰可见性。

#### 场景：显示确认

- **WHEN** 提示确认 AND 未提供 `--skip-specs`
- **THEN** 显示清晰的摘要：
 - 哪些 spec 将被创建（新能力）
 - 哪些 spec 将被更新（现有能力）
 - 每个 spec 的源路径
- **AND** 确认提示格式如下：
 ```
 The following specs will be updated:
 
 NEW specs to be created:
 - cli-archive (from changes/add-archive-command/specs/cli-archive/spec.md)
 
 EXISTING specs to be updated:
 - cli-init (from changes/update-init-command/specs/cli-init/spec.md)
 
 Update 2 specs and archive 'add-archive-command'? [y/N]:
 ```

#### 场景：处理确认响应

- **WHEN** 等待用户确认
- **THEN** 默认选择"否"以确保安全（需要显式输入 "y" 或 "yes"）
- **AND** 当提供 `--yes` 或 `-y` 标志时跳过确认
- **AND** 当提供 `--skip-specs` 标志时跳过整个 spec 确认

#### 场景：用户拒绝 spec 更新确认

- **WHEN** 用户拒绝 spec 更新确认
- **THEN** 跳过 spec 更新操作
- **AND** 显示消息："Skipping spec updates. Proceeding with archive."
- **AND** 继续执行 archive 操作
- **AND** 显示指示 spec 未更新的成功消息

## 错误处理

### 需求：错误条件

命令应优雅地处理各种错误条件。

#### 场景：处理错误

- **WHEN** 发生错误
- **THEN** 处理以下情况：
 - 缺失 openspec/changes/ 目录
 - 未找到变更
 - archive 目标已存在
 - 文件系统权限问题

## 为什么这些决策

**交互式选择**：减少输入并帮助用户查看可用变更
**任务检查**：防止意外 archive 未完成的工作
**日期前缀**：保持时间顺序并防止命名冲突
**不覆盖**：保留历史 archive 并防止数据丢失
**archive 前更新 spec**：主目录中的 spec 代表当前现实；当变更被部署和 archive 时，其未来状态 spec 成为新现实，必须替换主 spec
**spec 更新确认**：提供对变更内容的可见性，防止意外覆盖，确保用户在 spec 被修改前了解影响
**非阻塞确认**：拒绝 spec 更新不会取消 archive - 用户可以审阅 spec 并选择在需要时单独更新
**自动化 --yes 标志**：允许 CI/CD 管道在没有交互提示的情况下 archive，同时在手动使用时默认保持安全
**--skip-specs 标志**：允许 archive 不修改 spec 的变更（如基础设施、工具或文档变更），无需不必要的 spec 更新提示或操作

## 新增需求

### 需求：跳过 spec 选项

archive 命令应支持 `--skip-specs` 标志，跳过所有 spec 更新操作并直接进入 archive。

#### 场景：使用标志跳过 spec 更新

- **WHEN** 执行 `openspec archive <change> --skip-specs`
- **THEN** 跳过 spec 发现和更新确认
- **AND** 直接进入将变更移至 archive
- **AND** 显示指示已跳过 spec 的消息

### 需求：非阻塞确认

当用户拒绝 spec 更新时，archive 操作应继续执行，而不是取消整个操作。

#### 场景：用户拒绝 spec 更新确认

- **WHEN** 用户拒绝 spec 更新确认
- **THEN** 跳过 spec 更新
- **AND** 继续执行 archive 操作
- **AND** 显示指示 spec 未更新的成功消息
