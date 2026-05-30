## 新增需求

### 需求：workspace 设置命令
CLI artifact workflow 应在创建变更之前提供 workspace 设置命令。

#### 场景：在变更前准备 workspace planning
- **WHEN** 用户需要跨 repository 或文件夹准备 workspace planning 时
- **THEN** CLI 应提供用于设置、列出、链接、重新链接和诊断 workspace 的命令
- **AND** 这些命令不应要求有活动的 workspace 变更

#### 场景：使用简短命令列出 workspace
- **WHEN** 用户需要简洁的 workspace 列表命令时
- **THEN** CLI 应支持 `openspec workspace ls`
- **AND** 其行为应与 `openspec workspace list` 相同

#### 场景：将设置与 agent 启动分离
- **WHEN** 用户完成 workspace 设置时
- **THEN** 设置 workflow 应将 agent 启动和 workspace 打开行为留给后续 workflow
- **AND** 设置不应要求首选 agent 选择

#### 场景：避免公开直接创建
- **WHEN** 用户在首次 workspace 设置流程中创建 workspace 时
- **THEN** CLI 应使用 `openspec workspace setup`
- **AND** 不应将 `openspec workspace create` 暴露为公开创建路径
