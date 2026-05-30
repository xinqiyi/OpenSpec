# Agent 交接输出和交付优化

## 状态

从手动 Beta 实际测试中提出。

此工作项捕获了比更广泛的 `initiative next` 讨论更小但仍然对 Beta 流程重要的剩余 Agent 交接和交付输出差距。

## 事实来源

手动 Beta 记录：

- `../11-manual-beta-reality-pass/notes.md`，特别是关于设置后 Agent 指导、相对路径 `created_files` 和面向命令的交付警告的发现。

相关工作：

- `../proposed-initiative-next-agent-handoff-ux/`
- `../14-workspaces-beta-guide-split/`
- `../15-context-store-project-roots-and-schema-led-initiatives/`

## 存在的理由

Beta 测试表明，如果 Agent 知道要运行哪个命令，它们可以成功，但首次交接仍然过于隐晦。设置输出、JSON 收据、文档和生成的交付产物应使下一步操作显而易见，而无需用户粘贴隐性知识。

此工作项特意比 `initiative next` 命令更狭窄。它优化现有的命令输出和交付语义，使新 Agent 可以安全继续。

## 目标

- 使设置和倡议创建输出指向下一个有用的 Agent 操作。
- 确保 Agent 可读的 JSON 返回路径，在实际可行时无需路径重构即可直接使用。
- 澄清面向命令的交付，使"workflow 命令"不意味着"Agent 接收不到任何 OpenSpec 指导"。
- 当选中的工具无法接收 workflow 斜杠命令时清晰警告。
- 将基础 OpenSpec 素养与 workflow 入口点分开。

## 非目标

- 在此切片中不实现 `initiative next` 命令。
- 不添加进度仪表板或工作状态汇总。
- 不在设置输出中自动创建倡议、变更或 workspace。
- 如果现有兼容性需要，不使每个相对路径字段消失；而是添加直接绝对路径字段。

## 输出方向

创建或准备 OpenSpec 共享上下文的命令应在人类输出中包含一个小型交接块：

```text
为你的 Agent 准备的下一步：
 让你的编码 Agent 在 team-context 中创建或更新一个倡议。
```

JSON 输出应优先同时提供稳定的相对名称和 Agent 需要写入文件时的直接绝对路径：

```json
{
 "created_files": ["initiative.yaml", "brief.md"],
 "created_paths": [
 "/path/to/store/initiatives/billing-launch/initiative.yaml",
 "/path/to/store/initiatives/billing-launch/brief.md"
 ],
 "next_commands": {}
}
```

交付文案应区分：

- 基础 OpenSpec 指导或素养；
- workflow 入点，例如 skill 或斜杠命令。

如果用户为没有命令适配器的工具选择面向命令的交付，输出应警告 workflow 斜杠命令不可用，同时在工具支持时仍安装或推荐基础指导。

## 完成条件

- 新 Agent 可以在上下文存储设置或倡议创建后，使用命令输出和文档继续，而无需猜测路径或 Beta 命令名称。
- JSON 收据为创建的倡议产物暴露直接路径，或解释为什么只有相对名称可用。
- 面向命令的交付输出清晰报告安装、跳过或不可用的指导和 workflow 入点。
- 更广泛的 `initiative next` proposal 可以基于这些输出构建，而不是从头解决首次运行交接。
