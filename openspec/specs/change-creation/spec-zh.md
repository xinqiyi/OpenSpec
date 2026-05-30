# change-creation spec

## 目的
提供用于编程创建和验证 OpenSpec 变更目录的实用工具。

## 需求
### 需求：变更创建
系统应提供以编程方式创建新变更目录的函数。

#### 场景：创建变更
- **WHEN** 调用 `createChange(projectRoot, 'add-auth')`
- **THEN** 系统创建 `openspec/changes/add-auth/` 目录

#### 场景：拒绝重复变更
- **WHEN** 调用 `createChange(projectRoot, 'add-auth')` 且 `openspec/changes/add-auth/` 已存在
- **THEN** 系统抛出错误，指示该变更已存在

#### 场景：必要时创建父目录
- **WHEN** 调用 `createChange(projectRoot, 'add-auth')` 且 `openspec/changes/` 不存在
- **THEN** 系统创建完整路径，包括父目录

#### 场景：拒绝无效变更名称
- **WHEN** 使用无效名称调用 `createChange(projectRoot, 'Add Auth')`
- **THEN** 系统抛出验证错误

### 需求：变更名称验证
系统应验证变更名称遵循 kebab-case 约定。

#### 场景：接受有效的 kebab-case 名称
- **WHEN** 验证类似 `add-user-auth` 的变更名称时
- **THEN** 验证返回 `{ valid: true }`

#### 场景：接受数字后缀
- **WHEN** 验证类似 `add-feature-2` 的变更名称时
- **THEN** 验证返回 `{ valid: true }`

#### 场景：接受单个单词
- **WHEN** 验证类似 `refactor` 的变更名称时
- **THEN** 验证返回 `{ valid: true }`

#### 场景：拒绝大写字符
- **WHEN** 验证类似 `Add-Auth` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

#### 场景：拒绝空格
- **WHEN** 验证类似 `add auth` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

#### 场景：拒绝下划线
- **WHEN** 验证类似 `add_auth` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

#### 场景：拒绝特殊字符
- **WHEN** 验证类似 `add-auth!` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

#### 场景：拒绝前导连字符
- **WHEN** 验证类似 `-add-auth` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

#### 场景：拒绝尾随连字符
- **WHEN** 验证类似 `add-auth-` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

#### 场景：拒绝连续连字符
- **WHEN** 验证类似 `add--auth` 的变更名称时
- **THEN** 验证返回 `{ valid: false, error: "..." }`

### 需求：workspace 感知的变更创建
变更创建应支持 repository 本地和 workspace planning 主目录。

#### 场景：从 workspace 根目录创建变更
- **GIVEN** 命令从 OpenSpec workspace 根目录运行
- **WHEN** 用户创建新变更时
- **THEN** OpenSpec 应在 workspace planning 路径下创建变更
- **AND** 不应在链接 repository 的 `openspec/changes/` 目录下创建变更
- **AND** 当未提供显式 schema 时，应使用 `workspace-planning` schema

#### 场景：从 workspace 内部创建变更
- **GIVEN** 命令从 OpenSpec workspace planning 主目录的子目录中运行
- **WHEN** 用户创建新变更时
- **THEN** OpenSpec 应将当前 workspace 解析为 planning 主目录
- **AND** 应在该 workspace 的 planning 路径下创建变更
- **AND** 当未提供显式 schema 时，应使用 `workspace-planning` schema

#### 场景：从链接 repository 内部创建变更
- **GIVEN** repository 或文件夹被注册为 workspace 链接
- **AND** 命令从该链接 repository 或文件夹内部（而非 workspace planning 主目录）运行
- **WHEN** 用户创建新变更且未显式选择 workspace 时
- **THEN** OpenSpec 应为该位置保留 repository 本地变更创建行为
- **AND** 不应仅仅因为该位置被注册为 workspace 链接就创建 workspace 范围的变更

#### 场景：保留 repository 本地变更创建
- **GIVEN** 命令在 OpenSpec workspace 外部运行
- **WHEN** 用户在 repository 本地的 OpenSpec 项目中创建新变更时
- **THEN** OpenSpec 应继续在 `openspec/changes/` 下创建变更

#### 场景：拒绝无效的 workspace 影响领域
- **GIVEN** workspace 变更创建请求包含影响领域名称
- **WHEN** 一个或多个名称不是已注册的 workspace 链接时
- **THEN** OpenSpec 应拒绝这些无效的影响领域
- **AND** 应列出有效的 workspace 链接名称

#### 场景：无影响领域创建
- **GIVEN** 用户仍在探索范围
- **WHEN** 用户创建不带影响领域的 workspace 变更时
- **THEN** OpenSpec 应创建 workspace 变更
- **AND** 应允许稍后识别影响领域
