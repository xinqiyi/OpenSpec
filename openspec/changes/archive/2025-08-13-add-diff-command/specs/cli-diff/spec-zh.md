# CLI Diff 命令 spec

## 目的

`openspec diff` 命令为开发者提供提议的 spec 变更与当前已部署 spec 之间的可视化比较。

## 命令语法

```bash
openspec diff [change-name]
```

## 行为

### 不带参数

当运行 `openspec diff` 不带参数时
则列出 `changes/` 目录中所有可用的变更（排除 archive）
并提示用户选择一个变更

### 带变更名称

当运行 `openspec diff <change-name>` 时
则将 `changes/<change-name>/specs/` 中的所有 spec 文件与 `specs/` 中对应的文件进行比较

### Diff 输出

对于变更中的每个 spec 文件：
- 如果文件在两个位置都存在，则显示统一 diff
- 如果文件仅存在于变更中，则显示为新文件（所有行带 +）
- 如果文件仅存在于当前 spec 中，则显示为已删除（所有行带 -）

### 显示格式

Diff 应使用标准的统一 diff 格式：
- 以 `-` 为前缀的行表示删除的内容
- 以 `+` 为前缀的行表示添加的内容
- 无前缀的行表示未更改的上下文
- 显示正在比较路径的文件头

### 颜色支持

当终端支持颜色时：
- 删除的行以红色显示
- 添加的行以绿色显示
- 文件头以粗体显示
- 上下文行以默认颜色显示

### 错误处理

当指定的变更不存在时，显示错误"变更 '<name>' 未找到"
当变更中没有 specs 目录时，显示"'<name>' 未找到 spec 变更"
当 changes 目录不存在时，显示"未找到 OpenSpec 变更目录"

## 示例

```bash
# 查看特定变更的 diff
$ openspec diff add-auth-feature

--- specs/user-auth/spec.md
+++ changes/add-auth-feature/specs/user-auth/spec.md
@@ -10,6 +10,8 @@
用户应使用邮箱和密码进行身份验证。

+用户可通过 OAuth 提供商进行身份验证。
+
当凭证有效时，则签发 JWT 令牌。

# 列出所有变更并选择
$ openspec diff
可用变更：
 1. add-auth-feature
 2. update-payment-flow
 3. add-status-command
选择一个变更（1-3）：
```
