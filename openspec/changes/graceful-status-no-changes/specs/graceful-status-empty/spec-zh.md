## 新增需求

### 需求：Status 命令在无变更时优雅退出
`statusCommand` 函数应在调用 `validateChangeExists` 之前，通过 `getAvailableChanges` 检查可用变更。当未提供 `--change` 选项且不存在变更目录时，应打印友好的信息提示消息并以退出码 0 退出，而不是进入 `validateChangeExists` 并传播致命错误。

#### 场景：无变更存在，文本模式
- **当** 用户运行 `openspec status` 且未指定 `--change`，并且 `openspec/changes/` 下不存在变更目录时
- **则** CLI 打印 `No active changes. Create one with: openspec new change <name>` 到标准输出并以退出码 0 退出

#### 场景：无变更存在，JSON 模式
- **当** 用户运行 `openspec status --json` 且未指定 `--change`，并且不存在变更目录时
- **则** CLI 输出 `{"changes":[],"message":"No active changes."}` 作为有效 JSON 到标准输出并以退出码 0 退出

### 需求：保留现有的状态验证行为
`validateChangeExists` 中适用于 status 命令的其他错误路径应继续像以前一样抛出错误。`status` 之外使用 `validateChangeExists` 的命令应不受影响。

#### 场景：变更存在但未指定 --change
- **当** 用户运行 `openspec status` 且未指定 `--change`，并且存在一个或多个变更目录时
- **则** CLI 抛出错误，列出可用变更，消息为 `Missing required option --change. Available changes: ...`

#### 场景：指定的变更不存在
- **当** 用户运行 `openspec status --change non-existent` 时
- **则** CLI 抛出错误，消息为 `Change 'non-existent' not found`

#### 场景：其他命令不受影响
- **当** 用户运行 `openspec show` 或 `openspec instructions` 且未指定 `--change`，并且不存在变更时
- **则** CLI 抛出原始的 `No changes found` 错误（行为无变化）
