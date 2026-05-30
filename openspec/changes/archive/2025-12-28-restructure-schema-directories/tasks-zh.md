## 1. 创建 Schema 目录

- [ ] 1.1 在包根目录创建 `schemas/` 目录
- [ ] 1.2 从 `SPEC_DRIVEN_SCHEMA` 创建 `schemas/spec-driven/schema.yaml`
- [ ] 1.3 创建 `schemas/spec-driven/templates/` 并放置占位 template
- [ ] 1.4 从 `TDD_SCHEMA` 创建 `schemas/tdd/schema.yaml`
- [ ] 1.5 创建 `schemas/tdd/templates/` 并放置占位 template

## 2. 更新 Schema 解析

- [ ] 2.1 使用 `import.meta.url` 添加 `getPackageSchemasDir()` 函数
- [ ] 2.2 添加 `getSchemaDir(name)` 用于解析 schema 目录路径
- [ ] 2.3 更新 `resolveSchema()` 以从目录结构加载
- [ ] 2.4 更新 `listSchemas()` 以扫描目录而非对象键
- [ ] 2.5 添加用户覆盖解析的测试
- [ ] 2.6 添加内置回退的测试

## 3. 清理

- [ ] 3.1 移除 `builtin-schemas.ts`
- [ ] 3.2 更新 `index.ts` 导出（移除 `BUILTIN_SCHEMAS`、`SPEC_DRIVEN_SCHEMA`、`TDD_SCHEMA`）
- [ ] 3.3 更新所有导入已移除导出的代码

## 4. 包分发

- [ ] 4.1 在 `package.json` 的 `files` 数组中添加 `schemas/`
- [ ] 4.2 验证构建后的包中包含 schema

## 5. 修复 template 路径

- [ ] 5.1 更新 schema.yaml 文件中的 `template` 字段（移除 `templates/` 前缀）
- [ ] 5.2 确保 template 路径相对于 schema 的 templates 目录
