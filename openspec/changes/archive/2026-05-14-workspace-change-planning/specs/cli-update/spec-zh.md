## 新增需求

### 需求：repository 更新从 workspace planning 主目录重定向
repository 本地的 `openspec update` 命令不应将 workspace planning 主目录静默视为 repository 本地的 OpenSpec 项目。

#### 场景：从 workspace 根目录运行更新
- **GIVEN** 命令从 OpenSpec workspace 根目录运行
- **WHEN** 用户运行 `openspec update`
- **THEN** OpenSpec 不应在 workspace 根目录生成 repository 本地项目文件
- **AND** 应告知用户运行 `openspec workspace update`

#### 场景：从 workspace planning 目录内部运行更新
- **GIVEN** 命令从 OpenSpec workspace planning 主目录的子目录运行
- **WHEN** 用户运行 `openspec update`
- **THEN** OpenSpec 不应执行 repository 本地更新行为
- **AND** 应告知用户运行 `openspec workspace update`

#### 场景：从 repository 本地项目运行更新
- **GIVEN** 命令从 repository 本地的 OpenSpec 项目内部运行
- **WHEN** 用户运行 `openspec update`
- **THEN** OpenSpec 应保留现有的 repository 本地更新行为
