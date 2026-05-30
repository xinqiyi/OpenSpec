# 拒绝倡议解析证据

## 决策摘要

日期：2026-05-25。

经审查，现在或以后都不应实现独立的 `openspec initiative resolve <id>` 命令。

有用的区分已由现有概念覆盖：

- `initiative show` 解析规范的共享倡议上下文。
- 工作区是仓库和文件夹的本地视图。
- 仓库本地变更通过检入的元数据将自己链接到倡议。
- 仓库本地状态报告实施进度。

独立的解析命令大多会重复工作区本地视图状态，或在没有工作区时提供微弱的输出。

## 压力测试

场景：

```bash
git clone git@github.com:acme/context.git
openspec context-store register ./context --id platform
openspec initiative show billing-launch --json
```

这可以定位：

```text
platform/billing-launch
./context/initiatives/billing-launch
./context/initiatives/billing-launch/initiative.yaml
```

它无法知道：

```text
哪些实施仓库应在本地存在
这些仓库在该机器上的位置
用户打算在哪些仓库中工作
哪些仓库应被克隆
用户想要哪个工作区视图
```

这些知识属于用户和工作区，而非倡议。

## 为什么工作区改变了答案

当用户拥有工作区时，本地视图已由工作区解析：

```text
工作区 -> 链接名称 -> 机器本地路径
```

代理可以从工作区上下文进行操作。一个单独的 `initiative resolve` 命令会增加另一层，大多重复工作区已经拥有的内容。

如果未来的 UX 需要能感知倡议的打开，它应该是工作区行为的一部分，例如围绕选定的倡议打开或准备工作区。它不应是一个假装推断本地仓库可用性的独立倡议命令。

## 保留的研究笔记

早期的调查仍然作为背景有用：

- `initiative show` 已经有正确的上下文存储查找行为、歧义处理、不完整查找处理和 JSON 定位器输出。
- 事项 8 将倡议链接作为 `{ store, id }` 存储在仓库本地的 `.openspec.yaml` 中。
- 工作区状态拥有本地路径映射和生成的打开界面。
- 现有的仓库本地状态和指令公开了倡议链接，但不解析或总结倡议。

这些发现支持最终决定：不添加独立命令；将每个职责保留在现有的拥有者中。

## 被拒绝的范围

事项 9 拒绝：

- `openspec initiative resolve <id>`
- 路径解析仪表板
- 进度仪表板
- 全工作区扫描
- 全仓库扫描
- 作为倡议命令的显式路径扫描
- Git 远程匹配
- 仓库所有权推断
- 克隆或分支/工作树编排
- 倡议反向链接

## 验证

此通过仅更新决策构件。

```bash
git diff --check
```

结果：此次修订后通过。
