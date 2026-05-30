## 修改后的需求

### 需求：稳定的 workspace 名称
OpenSpec 应使用一个 kebab-case 的 workspace 名称，贯穿 workspace 标识、托管存储和本地注册表。

#### 场景：使用统一的 workspace 名称
- **WHEN** OpenSpec 创建或记录托管 workspace 时
- **THEN** workspace 名称应存储在 `.openspec-workspace/workspace.yaml` 中
- **AND** 同一名称应作为默认的托管 workspace 文件夹名称
- **AND** 同一名称应作为本地注册表名称

#### 场景：拒绝无效的 workspace 名称
- **WHEN** OpenSpec 接受 workspace 名称时
- **THEN** 应要求使用 kebab-case 命名，仅限小写字母、数字和单个连字符分隔符
- **AND** 应拒绝空名称、点名称、以连字符开头或结尾的名称、重复连字符、大写字母、空格、下划线、点和路径分隔符
- **AND** 设置流程应清晰报告操作系统级别的文件夹创建失败

### 需求：稳定的链接名称
OpenSpec 应使用稳定的文件夹式链接名称来引用 workspace planning 中的 repository 和文件夹。

#### 场景：在 workspace planning 中引用 repository 或文件夹
- **WHEN** workspace 状态或后续 workspace planning artifact 引用已链接的 repository 或文件夹时
- **THEN** 应使用稳定的链接名称
- **AND** 即使本地检出路径不同，同一链接名称仍应保持有效

#### 场景：跨机器复用链接名称
- **WHEN** workspace 在另一台机器上使用时
- **THEN** 链接名称应保持稳定
- **AND** 该机器上的本地检出路径可以不同

#### 场景：拒绝无效的链接名称
- **WHEN** OpenSpec 接受 workspace 链接名称时
- **THEN** 应拒绝空名称、`.` 或 `..`，以及包含路径分隔符的名称
- **AND** 链接名称应在 workspace 内唯一
- **AND** 链接名称不要求使用 workspace 名称的 kebab-case 格式
