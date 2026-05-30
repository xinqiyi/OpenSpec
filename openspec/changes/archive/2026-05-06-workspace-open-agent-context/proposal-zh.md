## 为什么

用户创建 workspace 并链接 repository 或文件夹后，他们需要用首选 agent 或编辑器打开该 workspace，并立即可用工作集。

workspace 应提供 repository 和文件夹位置、链接名称以及区分 planning 与实施的上下文。

## 什么变更

添加 workspace 打开体验：

```text
打开此 workspace。
默认使用我的首选打开程序，并遵守显式的打开程序覆盖。
打开程序看到 workspace 位置、链接的 repository 或文件夹、当前变更和相关说明。
```

链接是 planning 上下文。本地注册表是在当前机器上查找已知 workspace 的 workspace 发现索引。

预期的用户表面：

```bash
openspec workspace open
openspec workspace open platform
openspec workspace open --agent codex
openspec workspace open platform --agent github-copilot
openspec workspace open --editor
```

`workspace open` 在从 workspace 内部运行时，应打开当前 workspace；在 workspace 外部运行时，自动选择唯一已知的 workspace；在有多个已知 workspace 时，显示交互式选择器。用户可以在想要显式选择时，将 workspace 名称作为位置参数传递。

workspace 设置应询问并存储机器本地 workspace 状态中的首选打开程序。`workspace open` 默认使用该偏好。`--agent <tool>` 是一次会话的覆盖，保持保存的偏好不变。

`--editor` 将 workspace 作为编辑器 workspace 打开。这与 `--agent github-copilot` 相关但不同：GitHub Copilot 需要编辑器 workspace 支持加上 agent 提示上下文，而纯编辑器打开应专注于打开链接的工作集。

workspace 指导应尽可能存在于持久的 workspace 文件中：

- 稳定行为属于 workspace 级别的 `AGENTS.md`
- 特定于打开程序的启动提示在必要时保持最小
- 在变更存在之前，链接的 repository 或文件夹可见，用于探索和 planning

此切片支持通过文档化的打开程序形式进行根 workspace 启动。公共预览（`--prepare-only`）和机器可读上下文（`--json`）表面属于未来的上下文/查询设计，如果出现明确的用户需求。

此切片专注于根 workspace 打开行为。变更范围的会话需要来自 workspace 变更 planning 的目标模型，然后才能被清晰地指定。

planning 依赖：

- 依赖于 `workspace-create-and-register-repos`。

## 能力

### 新能力

- `workspace-open`：通过首选 agent 或 VS Code 编辑器打开 workspace，链接的 repository 或文件夹可用于探索和 planning。

### 修改的能力

- `workspace-foundation`：使用首选打开程序和可维护的可打开 workspace 表面，扩展机器本地 workspace 状态和设置/链接/重新链接行为。

## 影响

- `openspec workspace open`
- workspace 设置首选打开程序提示和本地偏好存储。
- workspace 提示、编辑器 workspace 和 agent 启动上下文。
- 生成或提交的 workspace schema agent 指导。
- 测试涵盖：在 workspace 内部打开、自动选择一个已知 workspace、从多个已知 workspace 中选择、按 workspace 名称打开、一次会话 agent 覆盖和编辑器打开。
