# 拟议倡议下一步 / Agent 交接用户体验

## 状态

讨论草稿。尚未锁定到编号路线图中。

## 存在的理由

GSD workspace 比较突显了一个用户体验差距：OpenSpec 拥有越来越好的发现原语，但 Agent 仍然需要从多个命令中推断出下一步有用操作。

候选方案是一个微型的"现在做什么？"交接命令，在从当前 repository 或 workspace 发现倡议之后使用。它不应成为仪表板、工作进度状态视图或 workspace 本地视图行为的替代品。

手动 Beta 测试揭示了第二个相关的交接差距：在 `initiative next` 这样的命令存在之前，一个新的编码 Agent 仍然需要基础的 OpenSpec 素养。它需要理解上下文存储、倡议、workspace、repository 本地变更以及产物应该放在哪里。一个小型的 `use-openspec` skill 可能是最简单的初始切片。

## 候选目标

帮助 Agent 回答：

```text
从当前 repository 或 workspace 来看，这个倡议的下一步我应该做什么？
```

## 可能的命令形态

```bash
openspec initiative next <id> --json
```

可能的响应：

```json
{
 "initiative": "billing-launch",
 "next_action": "create_repo_change",
 "reason": "已找到倡议，但此 repository 没有关联的本地变更",
 "suggested_command": "openspec new change add-billing-api --initiative billing-launch"
}
```

## 可能的 skill 形态

```text
use-openspec/
 SKILL.md
 references/
 shared-context-beta.md
 artifact-placement.md
```

这将是一个基础指南 skill，而不是 workflow 操作。它不应产生 `/opsx:use-openspec`，不应作为实施 workflow 出现，也不应暗示 workflow 命令交付不可用。

开放设计问题：它是默认配置的一部分，还是一个独立的始终在线内置 skill，或者是一个每当所选 Agent 支持 skill 时默认安装的托管指南 skill。

## 待审查的讨论点

- 在 workspace 倡议打开之前，这是否应成为编号路线图项？
- `initiative next` 是正确的命令名称，还是该指南应放在 workspace 倡议打开或 repository 本地状态中？
- 该命令应建议恰好一个下一步操作，还是返回一组排名的可能操作？
- 它应检查实际工作进度，还是仅限于交接就绪状态？
- 当没有注册存储、倡议不明确、本地 repository 不相关或已存在关联变更时，它应如何表现？
- 基础 OpenSpec 指南应建模为默认 skill、配置成员还是单独的托管指南？
- 指南 skill 如何与面向命令的交付交互？
- 它应如何教授产物放置：上下文存储倡议 vs repository 本地变更 vs workspace 视图？

## 边界

- 在第一个版本中不要添加进度/状态语义。
- 不要创建变更、克隆 repository 或改变 workspace 状态。
- 不要将 workspace 打开设为先决条件。
- 在初始切片中，优先选择 Agent 可读的 JSON 而非广泛的交互式用户体验。
- 除非出现单独的 workflow 需求，否则不要将基础指南转变为新的斜杠命令。
