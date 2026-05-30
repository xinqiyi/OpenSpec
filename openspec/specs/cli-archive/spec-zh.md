# CLI Archive 命令 spec

## 目的
archive 命令将已完成的变更从活动变更目录移动到 archive 文件夹，采用基于日期的命名，遵循 OpenSpec 约定。

## 命令语法
```bash
openspec archive [change-name] [--yes|-y]
```

选项：
- `--yes`、`-y`：跳过确认提示（用于自动化）
## 需求
### 需求：变更选择

该命令应支持交互式和直接变更选择方法。

#### 场景：交互式选择

- **WHEN** 未提供 change-name 时
- **THEN** 显示可用变更的交互式列表（排除 archive/）
- **AND** 允许用户选择一个

#### 场景：直接选择

- **WHEN** 提供了 change-name 时
- **THEN** 直接使用该变更
- **AND** 验证其是否存在

### 需求：任务完成检查

该命令应在 archive 前验证任务完成状态，以防止过早 archive。

#### 场景：发现未完成任务

- **WHEN** 发现未完成任务时（标记为 `- [ ]`）
- **THEN** 向用户显示所有未完成任务
- **AND** 提示确认是否继续
- **AND** 为安全起见默认"否"

#### 场景：所有任务完成

- **WHEN** 所有任务都完成或没有 tasks.md 时
- **THEN** 无需提示直接进行 archive

### 需求：archive 过程

archive 操作应遵循结构化的过程，以安全地将变更移动到 archive。

#### 场景：执行 archive

- **WHEN**archive 一个变更时
- **THEN** 执行以下步骤：
 1. 如果 archive/ 目录不存在则创建
 2. 使用当前日期生成目标名称 `YYYY-MM-DD-[change-name]`
 3. 检查目标目录是否已存在
 4. 从变更的未来状态 spec 更新主 spec（参见下面的 spec 更新过程）
 5. 将整个变更目录移动到 archive 位置

#### 场景：archive 已存在

- **WHEN** 目标 archive 已存在时
- **THEN** 失败并显示错误消息
- **AND** 不覆盖现有 archive

#### 场景：成功 archive

- **WHEN** 移动成功时
- **THEN** 显示成功消息，包含 archive 名称和已更新的 spec 列表

### 需求：spec 更新过程

在将变更移动到 archive 之前，该命令应将 delta 更改应用于主 spec，以反映部署后的实际情况。

#### 场景：应用 delta 更改

- **WHEN**archive 具有基于 delta 的 spec 的变更时
- **THEN** 按照 openspec-conventions 中的定义解析并应用 delta 更改
- **AND** 在应用前验证所有操作

#### 场景：验证 delta 更改

- **WHEN** 处理 delta 更改时
- **THEN** 按照 openspec-conventions 中的规定执行验证
- **AND** 如果验证失败，显示具体错误并中止

#### 场景：冲突检测

- **WHEN** 应用 delta 会创建重复的需求标题时
- **THEN** 中止并显示显示冲突的错误消息
- **AND** 建议手动解决

### 需求：确认行为

spec 更新确认应在更改应用前提供清晰的可见性。

#### 场景：显示确认

- **WHEN** 提示确认时
- **THEN** 显示清晰的摘要，显示：
 - 将创建哪些 spec（新能力）
 - 将更新哪些 spec（现有能力）
 - 每个 spec 的来源路径
- **AND** 将确认提示格式化为：
 ```
 将更新以下 spec：
 
 将创建的新 spec：
 - cli-archive（来自 changes/add-archive-command/specs/cli-archive/spec.md）
 
 将更新的现有 spec：
 - cli-init（来自 changes/update-init-command/specs/cli-init/spec.md）
 
 更新 2 个 spec 并 archive 'add-archive-command'？[y/N]：
 ```
#### 场景：处理确认响应

- **WHEN** 等待用户确认时
- **THEN** 为安全起见默认"否"（需要显式的"y"或"yes"）
- **AND** 当提供了 `--yes` 或 `-y` 标志时跳过确认

#### 场景：用户拒绝确认

- **WHEN** 用户拒绝确认时
- **THEN** 中止整个 archive 操作
- **AND** 显示消息："archive 已取消。未进行任何更改。"
- **AND** 以非零状态码退出

### 需求：错误条件

该命令应优雅地处理各种错误条件。

#### 场景：处理错误

- **WHEN** 发生错误时
- **THEN** 处理以下情况：
 - 缺少 openspec/changes/ 目录
 - 未找到变更
 - archive 目标已存在
 - 文件系统权限问题

### 需求：跳过 spec 选项

archive 命令应支持 `--skip-specs` 标志，该标志跳过所有 spec 更新操作并直接进行 archive。

#### 场景：使用标志跳过 spec 更新

- **WHEN** 执行 `openspec archive <change> --skip-specs` 时
- **THEN** 跳过 spec 发现和更新确认
- **AND** 直接进行将变更移动到 archive
- **AND** 显示指示 spec 已被跳过的消息

### 需求：非阻塞确认

当用户拒绝 spec 更新时，archive 操作应继续进行，而不是取消整个操作。

#### 场景：用户拒绝 spec 更新确认

- **WHEN** 用户拒绝 spec 更新确认时
- **THEN** 跳过 spec 更新
- **AND** 继续进行 archive 操作
- **AND** 显示指示 spec 未更新的成功消息

### 需求：显示输出

该命令应提供关于 delta 操作的清晰反馈。

#### 场景：显示 delta 应用

- **WHEN** 应用 delta 更改时
- **THEN** 为每个 spec 显示：
 - 添加的需求数量
 - 修改的需求数量
 - 移除的需求数量
 - 重命名的需求数量
- **AND** 使用 openspec-conventions 中定义的标准输出符号（+ ~ - →）：
 ```
 正在将更改应用到 specs/user-auth/spec.md：
 + 2 个已添加
 ~ 3 个已修改
 - 1 个已移除
 → 1 个已重命名
 ```

### 需求：archive 验证

archive 命令应在应用更改前验证变更，以确保数据完整性。

#### 场景：archive 前验证

- **WHEN** 执行 `openspec archive change-name` 时
- **THEN** 首先验证变更结构
- **AND** 仅当验证通过时才继续
- **AND** 如果验证失败，显示验证错误

#### 场景：不带验证的强制 archive

- **WHEN** 执行 `openspec archive change-name --no-validate` 时
- **THEN** 跳过验证（不安全 schema）
- **AND** 显示关于跳过验证的警告

## 为何做出这些决策

**交互式选择**：减少输入并帮助用户查看可用的变更
**任务检查**：防止意外 archive 未完成的工作
**日期前缀**：维护时间顺序并防止命名冲突
**不覆盖**：保留历史 archive 并防止数据丢失
**archive 前 spec 更新**：主目录中的 spec 代表当前实际情况；当变更被部署和 archive 时，其未来状态 spec 成为新的实际情况，必须替换主 spec
**spec 更新确认**：提供将要更改的内容的可见性，防止意外覆盖，并确保用户在 spec 被修改前了解影响
**用于自动化的 --yes 标志**：允许 CI/CD 管道在无需交互式提示的情况下 archive，同时默认为手动使用保持安全性
