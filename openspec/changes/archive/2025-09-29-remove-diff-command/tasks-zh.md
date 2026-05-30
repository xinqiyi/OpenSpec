# 移除 Diff 命令 - 任务

## 1. 移除核心实现
- [x] 删除 `/src/core/diff.ts`
- [x] 从 `/src/cli/index.ts` 移除 DiffCommand 导入
- [x] 从 CLI 移除 diff 命令注册

## 2. 移除 spec
- [x] 删除 `/openspec/specs/cli-diff/spec.md`
- [x] 如需历史参考，archive 该 spec

## 3. 更新依赖
- [x] 从 package.json 依赖中移除 jest-diff
- [x] 运行 pnpm install 更新锁文件

## 4. 更新文档
- [x] 更新主 README.md，移除 diff 命令引用
- [x] 更新 openspec/README.md，从命令列表中移除 diff 命令
- [x] 更新 CLAUDE.md template（如果其中提到了 diff 命令）
- [x] 更新任何使用了 diff 命令的示例 workflow

## 5. 更新相关文件
- [x] 搜索并更新所有对 "openspec diff" 的引用，包括：
 - template 文件
 - 测试文件（如果存在 diff 命令的测试）
 - archive 文档
 - 变更 proposal

## 7. 测试
- [x] 确保移除后所有测试通过
- [x] 验证 CLI 帮助文本不再显示 diff 命令
- [x] 测试 show 命令提供足够的替代功能

## 8. 替代 workflow 文档
- [x] 记录如何使用 `openspec show` 查看变更
- [x] 记录如何使用 git diff 进行文件比较
- [x] 在帮助文本或文档中添加迁移指南
