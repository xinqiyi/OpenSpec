## 阶段 1：实现名称验证

- [x] 1.1 创建 `src/utils/change-utils.ts`
- [x] 1.2 实现使用 kebab-case schema 的 `validateChangeName()`
- [x] 1.3 schema：`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`
- [x] 1.4 返回 `{ valid: boolean; error?: string }`
- [x] 1.5 添加测试：有效名称被接受（`add-auth`、`refactor`、`add-feature-2`）
- [x] 1.6 添加测试：大写被拒绝
- [x] 1.7 添加测试：空格被拒绝
- [x] 1.8 添加测试：下划线被拒绝
- [x] 1.9 添加测试：特殊字符被拒绝
- [x] 1.10 添加测试：前导/尾随连字符被拒绝
- [x] 1.11 添加测试：连续连字符被拒绝

## 阶段 2：实现变更创建

- [x] 2.1 实现 `createChange(projectRoot, name)`
- [x] 2.2 创建前验证名称
- [x] 2.3 必要时创建父目录（`openspec/changes/`）
- [x] 2.4 如果变更已存在则抛出错误
- [x] 2.5 添加测试：创建目录
- [x] 2.6 添加测试：重复变更抛出错误
- [x] 2.7 添加测试：无效名称抛出验证错误
- [x] 2.8 添加测试：必要时创建父目录

## 阶段 3：集成

- [x] 3.1 从 `src/utils/index.ts` 导出函数
- [x] 3.2 添加 JSDoc 注释
- [x] 3.3 运行所有测试以验证无回归
