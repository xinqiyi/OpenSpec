# 上下文存储首次运行和清理 UX 证据

## 手动 Beta 源注释

手动 beta 测试发现：

- 无参数的 `openspec context-store setup` 感觉应该启动交互式设置；
- 意外的设置之前在当前仓库下创建了一个存储，然后管理的默认值才被纠正；
- 清理没有 CLI 路径，需要手动删除文件并编辑注册表；
- Git 初始化使共享文件处于未跟踪状态，没有告诉用户或代理下一步该做什么。

## 初始建议

保持上下文存储首次运行 UX 小而本地化：

- 仅提示本地设置选项；
- 从不隐式推送、拉取、提交、创建远程仓库或删除文件；
- 保持 JSON 输出足够明确，以便代理安全继续；
- 将团队同步策略留给后续的共享协调加固工作。

## 实施结果

- 当未提供 id 时，`openspec context-store setup` 现在在交互式终端中运行引导式设置。
- 非交互式和 `--json` 设置需要显式输入，并在缺少 id 时以结构化的 setup-id 诊断失败。
- 另一个 Git 仓库内部的显式设置路径在非交互模式下被阻止，在交互模式下需要显式确认。
- `context-store unregister <id>` 仅移除本地注册表条目。
- `context-store remove <id>` 移除本地注册表条目，并仅在确认或 `--yes` 后删除本地文件夹；拒绝删除没有匹配上下文存储元数据的文件夹。
- 人类的成功输出故意保持紧凑；JSON 输出携带确切的注册表、文件和 Git 状态，没有 `next_commands`。

验证：

- `pnpm build`
- `pnpm lint`
- `pnpm vitest run test/commands/context-store.test.ts test/core/context-store/registry.test.ts`
- `pnpm test`
