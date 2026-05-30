## 新增需求

### 需求：archive 验证

archive 命令应在应用变更之前进行验证，以确保数据完整性。

#### 场景：archive 前验证

- **WHEN** 执行 `openspec archive change-name`
- **THEN** 首先验证变更结构
- **AND** 仅在验证通过时继续执行
- **AND** 如果验证失败则显示验证错误

#### 场景：跳过验证强制 archive

- **WHEN** 执行 `openspec archive change-name --no-validate`
- **THEN** 跳过验证（不安全 schema）
- **AND** 显示关于跳过验证的警告
