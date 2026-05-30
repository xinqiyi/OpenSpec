<p align="center">
  <a href="https://github.com/Fission-AI/OpenSpec">
    <picture>
      <source srcset="assets/openspec_bg.png">
      <img src="assets/openspec_bg.png" alt="OpenSpec logo">
    </picture>
  </a>
</p>

<p align="center">
  <a href="https://github.com/Fission-AI/OpenSpec/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/Fission-AI/OpenSpec/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://www.npmjs.com/package/@fission-ai/openspec"><img alt="npm version" src="https://img.shields.io/npm/v/@fission-ai/openspec?style=flat-square" /></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" /></a>
  <a href="https://discord.gg/YctCnvvshC"><img alt="Discord" src="https://img.shields.io/discord/1411657095639601154?style=flat-square&logo=discord&logoColor=white&label=Discord&suffix=%20online" /></a>
</p>

<details>
<summary><strong>最受欢迎的 spec 框架。</strong></summary>

[![Stars](https://img.shields.io/github/stars/Fission-AI/OpenSpec?style=flat-square&label=Stars)](https://github.com/Fission-AI/OpenSpec/stargazers)
[![Downloads](https://img.shields.io/npm/dm/@fission-ai/openspec?style=flat-square&label=Downloads/mo)](https://www.npmjs.com/package/@fission-ai/openspec)
[![Contributors](https://img.shields.io/github/contributors/Fission-AI/OpenSpec?style=flat-square&label=Contributors)](https://github.com/Fission-AI/OpenSpec/graphs/contributors)

</details>
<p></p>
我们的理念：

```text
→ fluid not rigid
→ iterative not waterfall
→ easy not complex
→ built for brownfield not just greenfield
→ scalable from personal projects to enterprises
```

> [!TIP]
> **New workflow now available!** We've rebuilt OpenSpec with a new artifact-guided workflow.
>
> Run `/opsx:propose "your idea"` to get started. → [Learn more here](docs/opsx.md)

<p align="center">
  在 <a href="https://x.com/0xTab">X 平台关注 @0xTab</a> 获取更新 · 加入 <a href="https://discord.gg/YctCnvvshC">OpenSpec Discord</a> 获取帮助与答疑。
</p>

<!-- TODO: Add GIF demo of /opsx:propose → /opsx:archive workflow -->

## 效果演示

```text
You: /opsx:propose add-dark-mode
AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — why we're doing this, what's changing
     ✓ specs/       — requirements and scenarios
     ✓ design.md    — technical approach
     ✓ tasks.md     — implementation checklist
     Ready for implementation!

You: /opsx:apply
AI:  Implementing tasks...
     ✓ 1.1 Add theme context provider
     ✓ 1.2 Create toggle component
     ✓ 2.1 Add CSS variables
     ✓ 2.2 Wire up localStorage
     All tasks complete!

You: /opsx:archive
AI:  Archived to openspec/changes/archive/2025-01-23-add-dark-mode/
     Specs updated. Ready for the next feature.
```

<details>
<summary><strong>OpenSpec 仪表盘</strong></summary>

<p align="center">
  <img src="assets/openspec_dashboard.png" alt="OpenSpec dashboard preview" width="90%">
</p>

</details>

## 快速开始

**需要 Node.js 20.19.0 或更高版本。**

全局安装 OpenSpec：

```bash
npm install -g @fission-ai/openspec@latest
```

然后进入你的项目目录并初始化：

```bash
cd your-project
openspec init
```

现在告诉你的 AI：`/opsx:propose <你想构建的功能>`

如果你想要扩展工作流（`/opsx:new`、`/opsx:continue`、`/opsx:ff`、`/opsx:verify`、`/opsx:bulk-archive`、`/opsx:onboard`），使用 `openspec config profile` 选择并运行 `openspec update` 应用。

> [!NOTE]
> Not sure if your tool is supported? [View the full list](docs/supported-tools.md) – we support 25+ tools and growing.
>
> Also works with pnpm, yarn, bun, and nix. [See installation options](docs/installation.md).

## 文档

→ **[Getting Started](docs/getting-started.md)**: first steps<br>
→ **[Workflows](docs/workflows.md)**: combos and patterns<br>
→ **[Commands](docs/commands.md)**: slash commands & skills<br>
→ **[CLI](docs/cli.md)**: terminal reference<br>
→ **[Supported Tools](docs/supported-tools.md)**: tool integrations & install paths<br>
→ **[Concepts](docs/concepts.md)**: how it all fits<br>
→ **[Multi-Language](docs/multi-language.md)**: multi-language support<br>
→ **[自定义](docs/customization.md)**: 打造你的专属配置


## 社区模式

通过独立仓库分发的第三方模式包 — 它们提供与 OpenSpec 和其他工具集成的自选工作流，类似于 [github/spec-kit 的社区扩展目录](https://github.com/github/spec-kit/tree/main/extensions) 处理工具集成的方式。

→ **[浏览目录](docs/customization.md#community-schemas)**，详见自定义文档。


## 为什么选择 OpenSpec？

AI 编程助手很强大，但当需求仅存在于聊天历史中时，其结果难以预测。OpenSpec 添加了一个轻量级的 spec 层，让你在编写任何代码之前就达成构建共识。

- **先共识后构建** — 在编写代码之前，人与 AI 就规范达成一致
- **保持条理** — 每次变更都有独立的文件夹，包含提案、规范、设计和任务
- **灵活工作** — 随时更新任何 artifact，没有僵化的阶段关卡
- **使用你的工具** — 通过斜杠命令与 20+ 种 AI 助手配合使用

### 对比

**vs. [Spec Kit](https://github.com/github/spec-kit)** (GitHub) — 功能全面但重量级。僵化的阶段关卡，大量 Markdown，Python 配置。OpenSpec 更轻量，让你自由迭代。

**vs. [Kiro](https://kiro.dev)** (AWS) — 功能强大，但被锁定在其 IDE 中且仅限于 Claude 模型。OpenSpec 与你已有的工具配合使用。

**vs. 不使用任何工具** — 没有规范的 AI 编码意味着模糊的提示和不可预测的结果。OpenSpec 带来了可预测性，且无需繁文缛节。

## 更新 OpenSpec

**升级包**

```bash
npm install -g @fission-ai/openspec@latest
```

**刷新 agent 指令**

在每个项目中运行此命令以重新生成 AI 指导，确保最新的斜杠命令生效：

```bash
openspec update
```

## 使用说明

**模型选择**：OpenSpec 在高推理能力模型上表现最佳。我们推荐使用 Codex 5.5 和 Opus 4.7 进行规划和实现。

**上下文清洁**：OpenSpec 受益于干净的上下文窗口。在开始实现之前清理你的上下文，并在整个会话中保持良好的上下文卫生。

## 贡献指南

**小修复** — Bug 修复、错别字更正和小改进可以直接提交 PR。

**较大变更** — 对于新功能、重大重构或架构变更，请先提交 OpenSpec 变更提案，以便我们在开始实现之前就意图和目标达成一致。

在编写提案时，请牢记 OpenSpec 的理念：我们服务于使用不同编程 agent、模型和用例的广泛用户。变更应对所有人都友好。

**欢迎 AI 生成的代码** — 前提是已经过测试和验证。包含 AI 生成代码的 PR 应注明所使用的编程 agent 和模型（例如："Generated with Claude Code using claude-opus-4-5-20251101"）。

### 开发

- 安装依赖：`pnpm install`
- 构建：`pnpm run build`
- 测试：`pnpm test`
- 本地开发 CLI：`pnpm run dev` 或 `pnpm run dev:cli`
- 约定式提交（一行）：`type(scope): subject`

## 其他

<details>
<summary><strong>遥测</strong></summary>

OpenSpec 收集匿名使用统计信息。

我们仅收集命令名称和版本来了解使用模式。不收集参数、路径、内容或个人身份信息。在 CI 环境中自动禁用。

**退出方式：** `export OPENSPEC_TELEMETRY=0` 或 `export DO_NOT_TRACK=1`

</details>

<details>
<summary><strong>维护者与顾问</strong></summary>

查看 [MAINTAINERS.md](MAINTAINERS.md) 获取核心维护者和指导项目发展的顾问名单。

</details>



## 许可证

MIT 许可证
