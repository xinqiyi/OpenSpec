# 向 OpenSpec CLI 添加 Diff 命令

## 为什么

开发人员需要轻松查看提议的 spec 变更与当前 spec 之间的差异，而无需手动比较文件。

## 变更内容

- 添加 `openspec diff [change-name]` 命令，显示变更 spec 与当前 spec 之间的差异
- 将 `changes/[change-name]/specs/` 中的文件与 `specs/` 中的相应文件进行比较
- 显示统一 diff 输出，显示添加/删除/修改的行
- 支持彩色输出以提高可读性

## 影响

- 受影响的 spec：将新增 `cli-diff` 能力
- 受影响的代码：
 - `src/cli/index.ts` - 添加 diff 命令
 - `src/core/diff.ts` - 包含 diff 逻辑的新文件（约 80 行）
