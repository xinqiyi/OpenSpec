# 添加更新命令

## 原因

用户需要一种方式来更新本地 OpenSpec 指令（README.md 和 CLAUDE.md），当 OpenSpec 包发布具有改进的 AI Agent 指令或结构约定的新版本时。

## 变更内容

- 添加新的 `openspec update` CLI 命令，用于更新 OpenSpec 指令
- 用最新模板替换 `openspec/README.md`
  - 安全，因为此文件完全由 OpenSpec 管理
- 使用标记仅更新 `CLAUDE.md` 中的 OpenSpec 管理块
  - 保留标记外的所有用户内容
  - 如果 `CLAUDE.md` 缺失，使用管理块创建它
- 更新后显示成功消息（ASCII 安全）："已更新 OpenSpec 指令"
  - 当终端支持时，可以显示前导勾选标记
  - 操作是幂等的（重新运行产生相同的结果）

## 影响范围

- 受影响的规范：`cli-update`（新能力）
- 受影响的代码：
  - `src/core/update.ts`（新命令类，镜像 `InitCommand` 的位置）
  - `src/cli/index.ts`（注册新命令）
  - 通过 `TemplateManager` 和 `readmeTemplate` 使用现有模板

## 排除范围

- 此变更不引入 `.openspec/config.json`。使用默认目录名称 `openspec`。
