## 新增需求

### 需求：workspace 感知的变更创建
变更创建应同时支持 repository 本地和 workspace planning 目录。

#### 场景：从 workspace 根目录创建变更
- **GIVEN** 命令从 OpenSpec workspace 根目录运行
- **WHEN** 用户创建新变更时
- **THEN** OpenSpec 应在 workspace planning 路径下创建变更
- **AND** 不应在链接 repository 的 `openspec/changes/` 目录下创建变更
- **AND** 当未提供显式 schema 时，应使用 `workspace-planning` schema

#### 场景：从 workspace 内部创建变更
- **GIVEN** 命令从 OpenSpec workspace planning 目录的子目录运行
- **WHEN** 用户创建新变更时
- **THEN** OpenSpec 应将当前 workspace 解析为 planning 目录
- **AND** 应在此 workspace 的 planning 路径下创建变更
- **AND** 当未提供显式 schema 时，应使用 `workspace-planning` schema

#### 场景：从链接 repository 内部创建变更
- **GIVEN** repository 或文件夹已注册为 workspace 链接
- **AND** 命令从该链接 repository 或文件夹内部运行，而非 workspace planning 目录
- **WHEN** 用户创建新变更但未显式选择 workspace
- **THEN** OpenSpec 应为该位置保留 repository 本地变更创建行为
- **AND** 不应仅因为该位置注册为 workspace 链接就创建 workspace 范围的变更

#### 场景：保留 repository 本地变更创建
- **GIVEN** 命令在 OpenSpec workspace 外部运行
- **WHEN** 用户在 repository 本地 OpenSpec 项目中创建新变更
- **THEN** OpenSpec 应继续在 `openspec/changes/` 下创建变更

#### 场景：拒绝无效的 workspace 影响区域
- **GIVEN** workspace 变更创建请求包含影响区域名称
- **WHEN** 一个或多个名称不是已注册的 workspace 链接
- **THEN** OpenSpec 应拒绝这些无效的影响区域
- **AND** 应列出有效的 workspace 链接名称

#### 场景：无影响区域创建
- **GIVEN** 用户仍在探索范围
- **WHEN** 用户创建 workspace 变更时没有影响区域
- **THEN** OpenSpec 应创建 workspace 变更
- **AND** 应允许稍后识别影响区域
