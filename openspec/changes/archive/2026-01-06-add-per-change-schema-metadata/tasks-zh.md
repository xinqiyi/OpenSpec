## 1. Zod 架构和类型

- [x] 1.1 在 `src/core/artifact-graph/types.ts` 中添加 `ChangeMetadataSchema` Zod 架构
- [x] 1.2 导出从架构推断的 `ChangeMetadata` 类型

## 2. 核心元数据函数

- [x] 2.1 创建使用 `writeChangeMetadata()` 函数的 `src/utils/change-metadata.ts`
- [x] 2.2 添加带有 Zod 验证的 `readChangeMetadata()` 函数
- [x] 2.3 更新 `createChange()` 以接受可选的 `schema` 参数并写入元数据

## 3. 指令加载器中的自动检测

- [x] 3.1 修改 `loadChangeContext()` 以从 `.openspec.yaml` 读取架构
- [x] 3.2 使 `schemaName` 参数可选（回退到元数据，然后是默认值）

## 4. CLI 更新

- [x] 4.1 向 `openspec new change` 命令添加 `--schema <name>` 选项
- [x] 4.2 验证现有命令（`status`、`instructions`）能与自动检测正常工作

## 5. 测试

- [x] 5.1 测试 `ChangeMetadataSchema` 正确验证（有效/无效情况）
- [x] 5.2 测试 `writeChangeMetadata()` 创建有效的 YAML
- [x] 5.3 测试 `readChangeMetadata()` 解析和验证架构
- [x] 5.4 测试 `loadChangeContext()` 从元数据自动检测架构
- [x] 5.5 测试无元数据时回退到默认值
- [x] 5.6 测试 `--schema` 标志覆盖元数据
