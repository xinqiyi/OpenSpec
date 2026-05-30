# specs-sync-skill spec

## 目的
定义用于将变更的 delta spec 同步到主 spec 的 agent skill。

## 需求

### 需求：Specs Sync skill
系统应提供 `/opsx:sync` skill，用于将变更的 delta spec 同步到主 spec。

#### 场景：将 delta spec 同步到主 spec
- **WHEN** agent 使用变更名称执行 `/opsx:sync`
- **THEN** agent 从 `openspec/changes/<name>/specs/` 读取 delta spec
- **AND** 从 `openspec/specs/` 读取对应的主 spec
- **AND** 协调主 spec 以匹配 delta 所描述的内容

#### 场景：幂等操作
- **WHEN** agent 对同一变更多次执行 `/opsx:sync`
- **THEN** 结果与运行一次相同
- **AND** 不会创建重复的需求

#### 场景：变更选择提示
- **WHEN** agent 执行 `/opsx:sync` 时未指定变更
- **THEN** agent 提示用户从可用变更中选择
- **AND** 显示具有 delta spec 的变更

### 需求：delta 协调逻辑
agent 应使用 delta 操作标题协调主 spec 与 delta spec。

#### 场景：新增需求
- **WHEN** delta 包含 `## 新增需求` 及一个需求
- **AND** 该需求在主 spec 中不存在
- **THEN** 将该需求添加到主 spec

#### 场景：新增需求已存在
- **WHEN** delta 包含 `## 新增需求` 及一个需求
- **AND** 主 spec 中已存在同名需求
- **THEN** 更新现有需求以匹配 delta 版本

#### 场景：修改后的需求
- **WHEN** delta 包含 `## 修改后的需求` 及一个需求
- **AND** 该需求在主 spec 中存在
- **THEN** 用 delta 版本替换主 spec 中的需求

#### 场景：移除的需求
- **WHEN** delta 包含 `## 移除的需求` 及一个需求名称
- **AND** 该需求在主 spec 中存在
- **THEN** 从主 spec 中移除该需求

#### 场景：重命名的需求
- **WHEN** delta 包含 `## 重命名的需求` 且格式为 FROM:/TO:
- **AND** FROM 中的需求在主 spec 中存在
- **THEN** 将需求重命名为 TO 中的名称

#### 场景：新的能力 spec
- **WHEN** delta spec 中存在主 spec 中没有的能力
- **THEN** 在 `openspec/specs/<能力名称>/spec.md` 创建新的主 spec 文件

### 需求：skill 输出
skill 应提供关于已应用内容的清晰反馈。

#### 场景：显示已应用的更改
- **WHEN** 协调成功完成
- **THEN** 显示按能力分类的更改摘要：
 - 新增需求数量
 - 修改需求数量
 - 移除需求数量
 - 重命名需求数量

#### 场景：无需更改
- **WHEN** 主 spec 已与 delta spec 匹配
- **THEN** 显示"spec 已同步 - 无需更改"
