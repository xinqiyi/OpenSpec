## 新增需求

### 需求：Diff 命令增强

diff 命令应在显示差异之前验证变更结构。

#### 场景：在 diff 之前验证

- **WHEN** 执行 `openspec diff change-name`
- **THEN** 验证变更结构
- **AND** 如果存在则显示验证警告
- **AND** 继续显示 diff
