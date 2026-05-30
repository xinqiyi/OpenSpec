## 为什么

一旦 repository 可见且 agent 具有 workspace 上下文，用户应该能够在实施开始前 planning 跨 repository 的变更，而无需创建 repository 本地 artifact。

用户的目标是：

```text
探索跨 repository 的产品目标。
决定范围。
创建一个识别受影响区域的 workspace 级 proposal。
```

planning 应是承诺点。仅 repository 可见性应保持轻量级。

## 什么变更

添加 workspace 级变更 planning：

- 从 workspace 根目录安装和刷新 OpenSpec agent skill，使 agent 能够从 planning 主目录操作
- 使用活动的全局 workflow 配置文件决定在 workspace 中安装哪些 workflow skill
- 保持 `--tools` 专注于哪些 agent 接收这些 workspace 本地 skill
- 为 workspace 变更添加 workspace 特定的 planning schema
- 从协调根目录创建 workspace 变更
- 一次性捕获产品目标
- 在适用时通过已注册的 workspace 链接名称识别受影响的区域
- 让 agent 在承诺受影响的区域或交付切片之前进行探索
- 保持 workspace 作为 planning 的真实源
- 更新 workflow skill 说明，使用 CLI 报告的 artifact 路径而不是硬编码的 repository 本地路径

此切片应避免将创建 repository 本地 artifact 作为 planning 的副作用。不应仅仅因为存在 workspace 变更就创建 repository 本地 artifact。

workspace 设置和更新可能会向 workspace 根目录写入 agent skill 文件，例如 `.codex/skills/` 或 `.claude/skills/`，因为这些文件使 workspace planning 主目录对 agent 可用。该设置工作不得将 OpenSpec artifact 或 agent skill 文件写入链接的 repository 或文件夹。

交互式设置应询问哪些 agent 应在此 workspace 中获得 OpenSpec skill，并在首选打开程序支持 skill 时预选它。workspace 更新应让用户稍后刷新或更改这些已安装的 agent skill，包括从 workspace 内部运行时。

workspace 设置和更新应将全局配置文件视为 workflow 选择源。对于此切片，workspace 设置和更新是仅限 skill 的，即使全局交付为 `commands` 或 `both`；workspace 的命令生成被推迟。

`openspec config profile` 应保持全局性，但当它在 OpenSpec workspace 内部运行并更改全局配置文件或交付设置时，它应提供通过运行 `openspec workspace update` 将新的 workflow 选择应用到当前 workspace 的选项。

workspace 本地 skill 选择应为机器本地状态：设置记录哪些 agent 接收了 skill，更新默认刷新该存储的选择，显式的 `--tools` 更改存储的选择。OpenSpec 应检测 workspace 本地 skill 何时与当前全局配置文件有差异，并给出清晰的更新指导。

选中的配置文件 workflow 中尚未完全实现 workspace 范围变更的仍应是安全的。生成的 skill 和 CLI 指导必须保护不受支持的 workspace 操作，而不是回退到 repository 本地行为或隐式编辑链接的 repository。

workspace 帮助、文档和补全应使区别清晰可辨：`openspec update` 保持为 repository/项目同步，而 `openspec workspace update` 同步 workspace 本地 agent skill。

planning 依赖：

- 依赖于 `workspace-open-agent-context`。

## 能力

### 新能力

- `workspace-change-planning`：创建和管理用于跨 repository 目标的 workspace 级 proposal。

### 修改的能力

- `workspace-links`：为 workspace 本地 agent skill 安装添加 workspace 设置/更新行为。
- `cli-config`：使 `openspec config profile` 感知 workspace 根目录，并能够将全局配置文件更改应用到当前 workspace。
- `change-creation`：添加 workspace 感知的变更创建语义和受影响区域识别。
- `cli-artifact-workflow`：丰富 workflow 状态和说明，使 agent 能够发现 planning 上下文和 artifact 路径，而无需硬编码的 repository 本地假设。
- `artifact-graph`：为 workspace 范围的变更添加内置的 workspace planning schema。
- `schema-resolution`：确保 workspace 范围的变更创建和 workflow 命令能够解析 workspace planning schema。
- `openspec-conventions`：定义 workspace 级 planning 与 repository 本地实施工作之间的关系。

## 影响

- workspace 变更创建。
- workspace 特定的 planning schema 和 template。
- 受影响的区域元数据和验证。
- 在 workspace 根目录安装或刷新 agent skill 的 workspace 设置和更新行为。
- 全局配置文件集成，用于 workspace 本地 skill workflow 选择。
- workspace 感知的 `openspec config profile` 应用提示行为。
- workspace 本地 agent skill 选择状态和差异检测。
- 在此切片中未实现 workspace 行为的配置文件 workflow 的受保护 workflow 指导。
- workspace skill 更新行为的文档、帮助和补全。
- 用于提议跨 repository 变更的 agent 说明，无需硬编码的变更路径。
- 测试验证在变更创建前已注册的 repository 可见，以及创建变更不意味着创建 repository 本地 artifact。
