## 上下文

artifact workflow 概念验证的第 4 个切片。核心功能（ArtifactGraph、InstructionLoader、change-utils）已完成。此切片添加 CLI 命令以向用户公开 artifact workflow。

**关键约束**：这是实验性的。命令必须隔离放置，以便在功能不成功时易于移除。

## 目标/非目标

- **目标：**
 - 通过 CLI 公开 artifact workflow 状态和说明
 - 提供流畅的用户体验，使用顶级动词命令
 - 支持人类可读和 JSON 两种输出格式
 - 使 agent 能够以编程方式查询 workflow 状态
 - 保持实现隔离以便于移除

- **非目标：**
 - 交互式 artifact 创建向导（未来工作）
 - Schema 管理命令（推迟）
 - 自动检测活跃变更（CLI 是确定性的，agent 进行推断）

## 决策

### 命令结构：顶级动词

命令是顶级结构以实现最大流畅度：

```
openspec status --change <id>
openspec next --change <id>
openspec instructions <artifact> --change <id>
openspec templates [--schema <name>]
openspec new change <name>
```

**理由：**
- 最流畅的用户体验 - 按键次数最少
- 命令足够独特以避免冲突
- 用户心智模型简单

**接受的权衡：** 轻微命名空间污染，但命令是独特的，可以干净地移除。

### 实验性隔离

所有 artifact workflow 命令都在单个文件中实现：

```
src/commands/artifact-workflow.ts
```

**移除该功能的方法：**
1. 删除 `src/commands/artifact-workflow.ts`
2. 从 `src/cli/index.ts` 中移除约 5 行代码

无需接触其他文件，不会对稳定功能造成风险。

### 带显式 `--change` 的确定性 CLI

所有变更特定命令都需要 `--change <id>`：

```bash
openspec status --change add-auth # 显式，有效
openspec status # 错误：缺少 --change
```

**理由：**
- CLI 是纯粹的、可测试的，没有隐藏状态
- agent 从对话中推断变更并显式传递
- 没有跟踪"活跃变更"的配置文件
- 与概念验证设计理念一致

### 新变更命令结构

创建变更使用显式子命令：

```bash
openspec new change add-feature
```

**理由：**
- `openspec new <name>` 有歧义（新的什么？）
- `openspec new change <name>` 清晰且可扩展
- 将来如果需要，可以添加 `openspec new spec <name>`

### 输出格式

- **默认**：带视觉指示器的人类可读文本
 - 状态：`[x]` 完成，`[ ]` 就绪，`[-]` 阻塞
 - 颜色：绿色（完成）、黄色（就绪）、红色（阻塞）
- **JSON**（`--json`）：机器可读，适用于脚本和 agent

### 错误处理

- 缺失 `--change`：列出可用变更的错误
- 未知变更：带建议的错误
- 未知 artifact：列出有效 artifact 的错误
- 缺失 schema：带 schema 解析详细信息的错误

## 风险/权衡

| 风险 | 缓解措施 |
|------|----------|
| 顶级命令污染命名空间 | 命令是独特的；隔离放置以便于移除 |
| `status` 与 git 混淆 | 上下文（`--change`）使其清晰 |
| 功能不成功 | 删除单个文件即可移除所有内容 |

## 实现说明

- 所有命令在 `src/commands/artifact-workflow.ts` 中
- 从 `src/core/artifact-graph/` 导入所有操作
- 使用 `item-discovery.ts` 中的 `getActiveChangeIds()` 列出变更
- 遵循现有的 CLI schema（ora 旋转器、commander.js 选项）
- 帮助文本将命令标记为"实验性"
