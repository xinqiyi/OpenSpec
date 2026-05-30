# workspace 重新实现从这里开始

这是面向智能体的、可 grep 的历史入口点，用于处理 workspace 重新实现的相关工作。

## 当前状态

原始的 workspace 生命周期路线图已被上下文存储和倡议方向重新定义。新加入的智能体应将本文档和 POC 材料视为保留的本地视图基础设施参考，而非下一个实现队列。

当前产品权威位于：

1. `openspec/initiatives/context-store-and-initiatives/direction.md`
2. `openspec/initiatives/context-store-and-initiatives/roadmap.md`

锁定边界为：

```text
上下文存储同步真相。
集合塑造真相。
倡议协调工作。
workspace 打开本地视图。
Change 实现 repository 拥有的切片。
```

有用的搜索关键词：

```text
workspace reimplementation
workspace poc
workspace-poc
workspace reference guide
workspace roadmap
fresh agent
start here
```

## 从这里开始

按顺序阅读以下文件：

1. `openspec/initiatives/context-store-and-initiatives/direction.md`
2. `openspec/initiatives/context-store-and-initiatives/roadmap.md`
3. `openspec/changes/workspace-reimplementation-roadmap/HISTORICAL_DIRECTION.md`
4. `openspec/changes/workspace-reimplementation-roadmap/README.md`
5. `openspec/changes/workspace-reimplementation-roadmap/POC_REFERENCE_GUIDE.md`

POC 参考提交为：

```text
workspace-poc @ 79a45ac043f414e63d13e08b9da83b135cb20a39
```

将 POC 用作研究材料。不要将其合并到实现分支中。
除非后续的倡议或 repository 本地变更设计明确决定，否则不要保留其架构。

## 历史实现顺序

原始的扁平 OpenSpec 顺序为：

1. `workspace-foundation`
2. `workspace-create-and-register-repos`
3. `workspace-open-agent-context`
4. `workspace-change-planning`
5. `workspace-agent-guidance`
6. `workspace-apply-repo-slice`
7. `workspace-verify-and-archive`

当前处理方式：

- 保留 setup、link、relink、list、open、update 和 doctor 作为 beta 本地视图基础设施。
- 将 workspace planning 视为遗留或过渡性行为，而非持久的跨 repository 可信源。
- 在倡议关联的 repository 本地 change 存在之前，不要将 `workspace-apply-repo-slice` 或 `workspace-verify-and-archive` 实现为头等 workspace 生命周期命令。
- 将 `workspace-reimplementation-roadmap` 用作连续性和参考，而非活跃的发布序列。

## 编辑前

对于你即将实现的切片，使用 `POC_REFERENCE_GUIDE.md` 检查固定的 POC 提交，然后记录以下内容：

```text
<切片> 的 POC 发现：

需要保留的用户行为：
- ...

值得迁移的测试或示例：
- ...

需要避免的实现捷径：
- ...

开放的设计问题：
- ...
```

将持久的发现记录在相关的倡议、上下文存储或 repository 本地 OpenSpec artifact 中，以便未来会话不依赖于聊天历史。
