# 设计：采用动词-名词 CLI 结构

## 概述
我们将使动词命令（`list`、`show`、`validate`、`diff`、`archive`）成为主要接口，并将名词命令（`spec`、`change`）作为一个发布周期保留为已弃用的别名。

## 决策

1. 保持路由集中在 `src/cli/index.ts` 中。
2. 为 `openspec list` 添加 `--specs`/`--changes`，默认使用 `--changes`。
3. 对 `openspec change list` 以及一般意义上的任何 `openspec change ...` 和 `openspec spec ...` 子命令显示弃用警告。
4. 不更改 `show`/`validate` 在帮助文本之外的行为；它们已经支持使用 `--type` 进行消歧。

## 向后兼容性
所有基于名词的命令继续可用，附带清晰的弃用警告，引导用户使用动词优先的替代命令。

## 不在此范围
跨 schema 的 `openspec list` JSON 输出对等以及 `show --specs/--changes` 发现功能是后续工作。
