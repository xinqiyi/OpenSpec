## 为什么

ArtifactGraph（切片 1）和 InstructionLoader（切片 3）提供了基于工件的工作流管理的编程 API。用户目前没有 CLI 接口来：
- 查看变更的工件完成状态
- 发现哪些工件已准备好创建
- 获取创建工件的增强说明
- 使用适当的验证创建新变更

此提案添加 CLI 命令，向用户和代理公开工件工作流功能。

## 变更内容

- **新增**：`openspec status --change <id>` 显示工件完成状态
- **新增**：`openspec next --change <id>` 显示已准备好创建的工件
- **新增**：`openspec instructions <artifact> --change <id>` 输出增强模板
- **新增**：`openspec templates [--schema <name>]` 显示已解析的模板路径
- **新增**：`openspec new change <name>` 创建一个新的变更目录

所有命令都是顶级结构，提供流畅的用户体验。它们与现有核心模块集成：
- 使用 instruction-loader 中的 `loadChangeContext()`、`formatChangeStatus()`、`generateInstructions()`
- 使用 artifact-graph 中的 `ArtifactGraph`、`detectCompleted()`
- 使用 change-utils 中的 `createChange()`、`validateChangeName()`

**实验性隔离**：所有命令在单个文件中实现（`src/commands/artifact-workflow.ts`），以便在功能不成功时易于移除。帮助文本将其标记为实验性。

## 影响

- 受影响的规范：新增 `cli-artifact-workflow` 能力
- 受影响的代码：
  - `src/cli/index.ts` - 注册新命令
  - `src/commands/artifact-workflow.ts` - 新命令实现
- 不更改现有命令或规范
- 建立在已完成的切片 1、2 和 3 实现之上
