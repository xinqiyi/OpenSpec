## 为什么

状态：已被 context-store-and-initiatives 方向推迟。生成的 workspace 指导仍然重要，但持久交接应围绕与 repository 本地 OpenSpec 变更关联的倡议进行设计，而非围绕 workspace 拥有的跨 repository planning 归属。

其余部分保留了原始的 workspace agent 指导方向，供日后参考。这项工作在倡议和与倡议关联的 repository 本地变更出现后仍具有重要意义；但目前不是最优先的关注点。

OpenSpec workspace 允许用户创建 planning 归属并链接 repository 或文件夹以进行跨区域探索。设置完成后，用户的下一期望很简单：

> 我用 agent 打开了 workspace。agent 应该知道它在哪里，可以安全地检查什么，以及如何帮助我把产品目标转化为 workspace proposal。

如今这种交接过于薄弱。workspace 本地 skill 已安装，CLI 可以创建 workspace 范围的变更，但 agent 的行为仍然大多像是在普通的 repository 本地 OpenSpec 项目中。在创建变更之前，它们没有清晰的 workspace 原生起始模型。

这造成了可以避免的困惑：

- 链接的 repository 或文件夹可能看起来像是实施目标，而非只读的 planning 上下文
- agent 可能不知道哪些已注册的链接名称是有效的受影响区域
- 用户可能感到在 planning 开始之前就需要知道每个受影响区域
- 产品目标可能在 workspace 探索和变更创建之间丢失
- workspace planning 可能感觉像是一种独立的 schema，而非跨链接区域的普通 OpenSpec

此项变更应强化的原则是：

> workspace 可见性不等于变更承诺。

链接的 repository 和文件夹可供探索。创建 workspace 变更捕捉了 planning 承诺。实施编辑仍需明确的 workflow 和允许的编辑根路径。

## 目标

使 workspace 本地 planning skill 为 agent 提供一个小型、可靠的操作模型，用于启动 workspace proposal。

在 workspace 中打开的 agent 应能够：

1. 识别其正在从 workspace planning 归属运行
2. 检查已注册的 workspace 链接作为 planning 上下文
3. 在 planning 期间保持链接的 repository 和文件夹为只读
4. 从用户请求中推导出简洁的 workspace 变更名称和产品目标
5. 仅在已知的受影响区域匹配已注册的 workspace 链接名称时传递它们
6. 即使受影响区域尚未解决也能继续，使这些问题在正常 planning artifact 中保持可见

这对用户来说应该感觉像是普通的 OpenSpec proposal 流程，只是多了 workspace 感知的上下文和安全性。

## 初始范围

从最小的有用表面开始：

- workspace 本地生成的 skill 指导
- 从 workspace planning 归属使用的变更启动 workflow
- 用户产品目标、已注册链接名称和 workspace 变更元数据之间的关系
- 将 planning 与实施编辑分开的护栏

首次实施应优先选择清晰的 agent 指导，而非新的 workflow 机制。如果现有 CLI 已暴露足够的 workspace 上下文，skill 应使用它。如果不够，应在添加更重量的行为之前明确识别缺失的上下文。

## 非目标

此项变更无需解决完整的 workspace 生命周期。

此切片范围之外：

- workspace 应用语义
- workspace 验证或 archive 语义
- 分支或工作树编排
- 为每个受影响区域创建 repository 本地变更
- 共享/团队协作 repository 行为
- spec 的共享合约所有权流程
- 强制用户在创建 proposal 之前确定所有受影响区域

## 需要解决的问题

- agent 在创建变更之前应读取哪些确切的 workspace 上下文？
- 现有的 workspace/status/doctor 输出是否足够，还是我们需要一个更清晰的变更前上下文命令？
- 生成的 skill 应如何决定受影响区域足够确定可以传递为 `--areas`？
- `--goal` 应该是仅 workspace 的元数据，还是也应记录 repository 本地行为？
- 未解决的受影响区域问题应出现在哪里，以便用户和 agent 从同一真实来源继续？
