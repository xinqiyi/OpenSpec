# CLI archive 命令 - 变更

## 修改后的需求

### 需求：spec 更新过程

在将变更移至 archive 之前，命令应将 delta 更改应用到主要 spec，以反映已部署的实际情况。

#### 场景：应用 delta 更改

- **WHEN** archive 带基于 delta spec 的变更时
- **THEN** 解析并应用 openspec-conventions 中定义的 delta 更改
- **AND** 在应用之前验证所有操作

#### 场景：验证 delta 更改

- **WHEN** 处理 delta 更改时
- **THEN** 执行 openspec-conventions 中指定的验证
- **AND** 如果验证失败，显示具体错误并中止

#### 场景：冲突检测

- **WHEN** 应用 delta 会导致重复的需求标题
- **THEN** 中止并显示显示冲突的错误消息
- **AND** 建议手动解决

## 新增需求

### 需求：显示输出

命令应提供关于 delta 操作的清晰反馈。

#### 场景：显示 delta 应用

- **WHEN** 应用 delta 更改时
- **THEN** 为每个 spec 显示：
 - 新增的需求数量
 - 修改的需求数量
 - 移除的需求数量
 - 重命名的需求数量
- **AND** 使用 openspec-conventions 中定义的标准输出符号（+ ~ - →）：
 ```
 正在将变更应用到 specs/user-auth/spec.md：
 + 2 个新增
 ~ 3 个修改
 - 1 个移除
 → 1 个重命名
 ```
