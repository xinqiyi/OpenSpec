# 为 OpenSpec 变更采用未来状态存储

## 为什么

当前以差异文件（`.spec.md.diff`）存储 spec 变更的方式给人类和 AI 都带来了障碍。带有 `+` 和 `-` 前缀的差异语法使 spec 难以阅读，AI 工具在理解未来状态时也难以处理这种格式，而且 GitHub 无法在不同文件夹中显示当前和提议 spec 之间的良好对比。

## 变更内容

- 从存储差异（`patches/[能力]/spec.md.diff`）改为存储完整的未来状态（`specs/[能力]/spec.md`）
- 更新所有文档以反映新的存储格式
- 将现有的 `add-init-command` 变更新格式
- 添加新的 `openspec-conventions` 能力以记录这些约定

## 影响

- 受影响的 spec：新的 `openspec-conventions` 能力
- 受影响的代码：
 - openspec/README.md（第 85-108 行）
 - docs/PRD.md（第 376-382 行，第 778-783 行）
 - docs/openspec-walkthrough.md（第 58-62 行，第 112-126 行）
 - openspec/changes/add-init-command/（需要迁移）
