## 1. 更新解析器类型和辅助函数

- [x] 1.1 在 `src/core/artifact-graph/resolver.ts` 中将 `SchemaInfo.source` 类型更新为包含 `'project'`
- [x] 1.2 添加 `getProjectSchemasDir(projectRoot: string): string` 函数

## 2. 更新 schema 解析函数

- [x] 2.1 更新 `getSchemaDir(name, projectRoot?)` 在提供 projectRoot 时优先检查项目本地
- [x] 2.2 更新 `resolveSchema(name, projectRoot?)` 将 projectRoot 传递给 getSchemaDir
- [x] 2.3 更新 `listSchemas(projectRoot?)` 以包含项目本地 schema
- [x] 2.4 更新 `listSchemasWithInfo(projectRoot?)` 以包含 `source: 'project'` 的项目 schema

## 3. 更新 CLI 命令

- [x] 3.1 更新 `schemasCommand` 以传递 projectRoot 并在输出中显示来源标签

## 4. 更新调用点

- [x] 4.1 审查并更新需要项目本地 schema 支持的调用点，以传递 projectRoot

## 5. 测试

- [x] 5.1 为 `getProjectSchemasDir()` 添加单元测试
- [x] 5.2 为项目本地 schema 解析优先级添加单元测试
- [x] 5.3 为向后兼容（无 projectRoot = 仅用户 + 包）添加单元测试
- [x] 5.4 为包含项目 schema 的 `listSchemas()` 添加单元测试
- [x] 5.5 为包含 `source: 'project'` 的 `listSchemasWithInfo()` 添加单元测试
- [x] 5.6 使用包含本地 schema 的临时项目添加集成测试
