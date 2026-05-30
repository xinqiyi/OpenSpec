# 将工作区稳定为本地视图的证据

## 方向证据

`direction.md` 指出，持久化的共享对象是同步的上下文存储，
initiative 是第一个主要的集合。它将工作区定义为上下文存储和仓库之上的本地工作视图，将仓库变更定义为仓库/团队拥有的
实现计划。

已锁定的产品边界取代了旧模型——即工作区级别的
`changes/` 树拥有规范的共享跨仓库计划。现有
工作区规划行为可以作为 Beta 或遗留基础设施保留，但
不应引导新的生命周期设计。

## 子代理研究

实现研究发现，工作区的 setup、link、relink、list、open、
update 和 doctor 已经基本表现得像本地视图基础设施：

- 共享链接名称存储在工作区状态中
- 机器本地路径和开启器/技能状态存储在本地状态中
- `workspace open` 将链接的文件夹作为本地工作集启动
- 链接的仓库被视为工作区规划命令的上下文
- `workspace update` 刷新工作区本地技能，保持链接的仓库
  不变

指导研究发现，生成的 `AGENTS.md` 块是最重要
的不匹配，因为它仍然将工作区框定为跨
链接仓库的规划工具，并说要使用 `changes/` 进行工作区级别的规划。

测试研究发现，当前 setup/list/doctor、link/relink、
open、update、工件放置和工作区规划防护的覆盖率很高。针对性的
工作区/工件测试切片通过，技能模板一致性测试也通过。

## 主要风险

如果生成的工作区指导继续推荐使用工作区级别的
`changes/`，代理可能将工作区视为持久化的共享规划
对象，尽管 initiative 方向已将持久化协调分配给
initiative，将实现规划分配给仓库本地的变更。

## 实现证据

第一个实现切片更新了生成的工作区 `AGENTS.md`
指导，并使 `workspace update` 刷新工作区本地的开放表面。
它还更新了工作区规划操作上下文，使 Beta 工作区工件被
报告为"工作区本地"兼容性上下文，而非
真相来源。

Doctor/状态审查发现，本地路径映射、未解析的链接、修复
步骤、格式错误的本地状态、缺失的本地状态、仓库规范路径和技能
漂移警告已被覆盖。正常的已安装技能摘要暂时
推迟；当前切片仅更新过时的 `workspace update`
措辞，使其与指导刷新行为匹配。

验证：

- `pnpm run build`
- `pnpm exec vitest run test/commands/workspace.test.ts test/commands/artifact-workflow.test.ts test/core/workspace/foundation.test.ts`
- `pnpm run lint`
- `git diff --check`

## 结项证据

实时文档不再将工作区描述为持久化的规划归宿或
跨仓库规划的规范位置。历史和推迟的工作区
工件保留作为参考材料，活跃的推迟提案标记为
不让它们引导下一个实现切片。
