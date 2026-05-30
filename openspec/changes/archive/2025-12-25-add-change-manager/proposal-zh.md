## 原因

目前没有以编程方式创建新变更目录的方法。用户必须手动：
1. 创建 `openspec/changes/<name>/` 目录
2. 创建 `proposal.md` 文件
3. 希望命名正确

这种方式容易出错，并且阻碍了自动化（例如 Claude 命令、脚本）。

**此 proposal 新增：**
1. `createChange(projectRoot, name)` - 以编程方式创建变更目录
2. `validateChangeName(name)` - 强制 kebab-case 命名约定

## 变更内容

### 新增工具

| 函数 | 描述 |
|------|------|
| `createChange(projectRoot, name)` | 创建 `openspec/changes/<name>/` 目录 |
| `validateChangeName(name)` | 返回 `{ valid: boolean; error?: string }` |

### 名称验证规则

schema：`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`

| 有效 | 无效 |
|------|------|
| `add-auth` | `Add-Auth`（大写） |
| `refactor-db` | `add auth`（空格） |
| `add-feature-2` | `add_auth`（下划线） |
| `refactor` | `-add-auth`（前导连字符） |

### 位置

新文件：`src/utils/change-utils.ts`

简单的工具函数 - 无类，无抽象层。

## 影响范围

- **受影响的 spec**：无
- **受影响的代码**：无（仅新增工具）
- **新增文件**：`src/utils/change-utils.ts`
- **破坏性变更**：无
