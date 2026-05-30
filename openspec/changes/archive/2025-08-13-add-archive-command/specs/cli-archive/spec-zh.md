# CLI Archive 命令 spec

## 目的
archive 命令将已完成的变更从活跃变更目录移至 archive 文件夹，并使用基于日期的命名，遵循 OpenSpec 约定。

## 命令语法
```bash
openspec archive [change-name] [--yes|-y]
```

选项：
- `--yes`, `-y`：跳过确认提示（用于自动化）

## 行为

### 变更选择
当未提供 change-name 时
则显示可用变更的交互式列表（排除 archive/）
并且允许用户选择一个

当提供了 change-name 时
则直接使用该变更
并且验证它存在

### 任务完成检查
命令应扫描变更的 tasks.md 文件以查找未完成任务（标记为 `- [ ]`）

当发现未完成任务时
则向用户显示所有未完成任务
并且提示确认是否继续
并且出于安全考虑默认选择"否"

当所有任务已完成或 tasks.md 不存在时
则继续 archive 而不提示

### archive 流程
archive 操作应：
1. 如果 archive/ 目录不存在则创建
2. 使用当前日期生成目标名称 `YYYY-MM-DD-[change-name]`
3. 检查目标目录是否已存在
4. 从变更的未来状态 spec 更新主 spec（见下面的 spec 更新流程）
5. 将整个变更目录移至 archive 位置

当目标 archive 已存在时
则失败并显示错误消息
并且不覆盖现有 archive

当移动成功时
则显示成功消息，包含 archive 名称和已更新的 spec 列表

### spec 更新流程
在将变更移至 archive 之前，命令应更新主 spec 以反映已部署的现实：

当变更包含 `changes/[name]/specs/` 中的 spec 时
则：
1. 通过与现有 spec 比较分析哪些 spec 将受影响
2. 向用户显示 spec 更新摘要（见下面的确认行为）
3. 除非提供了 `--yes` 标志，否则提示确认
4. 如果确认，对于变更目录中的每个能力 spec：
 - 将 spec 从 `changes/[name]/specs/[capability]/spec.md` 复制到 `openspec/specs/[capability]/spec.md`
 - 如果目标目录结构不存在则创建
 - 覆盖现有 spec 文件（spec 代表当前现实，变更 spec 是新的现实）
 - 跟踪哪些 spec 已更新用于成功消息

当变更中不存在 spec 时
则跳过 spec 更新步骤
并且继续 archive

### 确认行为
spec 更新确认应：
- 显示清晰摘要，展示：
 - 哪些 spec 将被创建（新能力）
 - 哪些 spec 将被更新（现有能力）
 - 每个 spec 的源路径
- 将确认提示格式化为：
 ```
 以下 spec 将被更新：
 
 要创建的新 spec：
 - cli-archive（来自 changes/add-archive-command/specs/cli-archive/spec.md）
 
 要更新的现有 spec：
 - cli-init（来自 changes/update-init-command/specs/cli-init/spec.md）
 
 更新 2 个 spec 并将 'add-archive-command' archive？[y/N]：
 ```
- 出于安全考虑默认选择"否"（需要显式的 "y" 或 "yes"）
- 当提供 `--yes` 或 `-y` 标志时跳过确认

当用户拒绝确认时
则中止整个 archive 操作
并且显示消息："archive 已取消。未进行任何更改。"
并且以非零状态码退出

## 错误处理

应处理以下错误情况：
- 缺少 openspec/changes/ 目录
- 未找到变更
- archive 目标已存在
- 文件系统权限问题

## 为何做出这些决策

**交互式选择**：减少输入并帮助用户查看可用变更
**任务检查**：防止意外 archive 未完成的工作
**日期前缀**：保持时间顺序并防止命名冲突
**不覆盖**：保护历史 archive 并防止数据丢失
**archive 前更新 spec**：主目录中的 spec 代表当前现实；当变更已部署并 archive 时，其未来状态 spec 成为新的现实，必须替换主 spec
**spec 更新确认**：提供将要变更的内容的可见性，防止意外覆盖，确保用户在 spec 被修改前了解影响
**用于自动化的 --yes 标志**：允许 CI/CD 管道在无需交互提示的情况下 archive，同时对手动使用保持默认安全
