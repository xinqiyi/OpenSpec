## 新增需求

### 需求：仓库更新从工作区规划主目录重定向
仓库本地的 `openspec update` 命令不应将工作区规划主目录静默视为仓库本地的 OpenSpec 项目。

#### 场景：从工作区根目录运行更新
- **给定** 命令从 OpenSpec 工作区根目录运行
- **当** 用户运行 `openspec update`
- **则** OpenSpec 不应在工作区根目录生成仓库本地项目文件
- **并且** 应告知用户运行 `openspec workspace update`

#### 场景：从工作区规划目录内部运行更新
- **给定** 命令从 OpenSpec 工作区规划主目录的子目录运行
- **当** 用户运行 `openspec update`
- **则** OpenSpec 不应执行仓库本地更新行为
- **并且** 应告知用户运行 `openspec workspace update`

#### 场景：从仓库本地项目运行更新
- **给定** 命令从仓库本地的 OpenSpec 项目内部运行
- **当** 用户运行 `openspec update`
- **则** OpenSpec 应保留现有的仓库本地更新行为
