# Changesets

此目录由 [Changesets](https://github.com/changesets/changesets) 管理。

## 快速开始

```bash
pnpm changeset
```

按照提示选择版本升级类型并描述您的更改。

## 工作流

1. **添加 changeset** — 在 PR 之前或之后在本地运行 `pnpm changeset`
2. **版本 PR** — 当 changeset 合并到 main 分支时，CI 打开/更新一个"版本包"PR
3. **发布** — 合并版本 PR 会触发 npm 发布和 GitHub Release

> **注意：** 贡献者只需运行 `pnpm changeset`。版本控制（`changeset version`）和发布会在 CI 中自动完成。

## 模板

使用以下结构编写您的 changeset 内容：

```markdown
---
"@fission-ai/openspec": patch
---

### 新功能

- **功能名称** — 用户现在可以做什么

### 错误修复

- 修复了当 Y 发生时会 X 的问题

### 重大变更

- `oldMethod()` 已被移除，请使用 `newMethod()` 替代

### 弃用

- `legacyOption` 已被弃用，将在 v2.0 中移除

### 其他

- X 的内部重构以获得更好的性能
```

只包含与您的变更相关的部分。

## 版本升级指南

| 类型 | 使用时机 | 示例 |
|------|---------|------|
| `patch` | 错误修复、小改进 | 修复了配置缺失时的崩溃 |
| `minor` | 新功能、非破坏性新增 | 添加了 `--verbose` 标志 |
| `major` | 重大变更、功能移除 | 将 `init` 重命名为 `setup` |

## 何时创建 changeset

**需要创建：**
- 新功能或命令
- 影响用户的错误修复
- 重大变更或弃用
- 用户能注意到的性能改进

**不需要创建：**
- 仅文档更改
- 测试添加/修复
- 对用户无影响的内部重构
- CI/工具链更改

## 编写良好描述

**应该：** 为用户而非开发者编写
```markdown
- **Shell 补全** — 现在 Bash、Fish 和 PowerShell 支持 Tab 补全
```

**不应该：** 编写实现细节
```markdown
- 添加了带有 Bash/Fish/PowerShell 子类的 ShellCompletionGenerator 类
```

**应该：** 解释影响
```markdown
- 修复了配置加载以在 Linux 上尊重 `XDG_CONFIG_HOME`
```

**不应该：** 仅引用修复
```markdown
- 修复了 #123
```
