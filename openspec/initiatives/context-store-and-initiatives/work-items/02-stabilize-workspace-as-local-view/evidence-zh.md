# 将 workspace 稳定为本地视图的证据

## 方向证据

`direction.md` 指出，持久化的共享对象是同步的上下文存储，
initiative 是第一个主要的集合。它将 workspace 定义为上下文存储和 repository 之上的本地工作视图，将 repository 变更定义为 repository/团队拥有的
实现计划。

已锁定的产品边界取代了旧模型——即 workspace 级别的
`changes/` 树拥有 spec 的共享跨 repository 计划。现有
workspace planning 行为可以作为 Beta 或遗留基础设施保留，但
不应引导新的生命周期设计。

## 子 agent 研究

实现研究发现，workspace 的 setup、link、relink、list、open、
update 和 doctor 已经基本表现得像本地视图基础设施：

- 共享链接名称存储在 workspace 状态中
- 机器本地路径和开启器/skill 状态存储在本地状态中
- `workspace open` 将链接的文件夹作为本地工作集启动
- 链接的 repository 被视为 workspace planning 命令的上下文
- `workspace update` 刷新 workspace 本地 skill，保持链接的 repository
 不变

指导研究发现，生成的 `AGENTS.md` 块是最重要
的不匹配，因为它仍然将 workspace 框定为跨
链接 repository 的 planning 工具，并说要使用 `changes/` 进行 workspace 级别的 planning。

测试研究发现，当前 setup/list/doctor、link/relink、
open、update、artifact 放置和 workspace planning 防护的覆盖率很高。针对性的
workspace/artifact 测试切片通过，skill template 一致性测试也通过。

## 主要风险

如果生成的 workspace 指导继续推荐使用 workspace 级别的
`changes/`，agent 可能将 workspace 视为持久化的共享 planning
对象，尽管 initiative 方向已将持久化协调分配给
initiative，将实现 planning 分配给 repository 本地的变更。

## 实现证据

第一个实现切片更新了生成的 workspace `AGENTS.md`
指导，并使 `workspace update` 刷新 workspace 本地的开放表面。
它还更新了 workspace planning 操作上下文，使 Beta workspace artifact 被
报告为"workspace 本地"兼容性上下文，而非
真相来源。

Doctor/状态审查发现，本地路径映射、未解析的链接、修复
步骤、格式错误的本地状态、缺失的本地状态、repository spec 路径和 skill
漂移警告已被覆盖。正常的已安装 skill 摘要暂时
推迟；当前切片仅更新过时的 `workspace update`
措辞，使其与指导刷新行为匹配。

验证：

- `pnpm run build`
- `pnpm exec vitest run test/commands/workspace.test.ts test/commands/artifact-workflow.test.ts test/core/workspace/foundation.test.ts`
- `pnpm run lint`
- `git diff --check`

## 结项证据

实时文档不再将 workspace 描述为持久化的 planning 归宿或
跨 repository planning 的 spec 位置。历史和推迟的 workspace
artifact 保留作为参考材料，活跃的推迟 proposal 标记为
不让它们引导下一个实现切片。
