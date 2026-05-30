## 1. 类型定义
- [x] 1.1 创建 `src/core/artifact-graph/types.ts`，包含 Zod schema（`ArtifactSchema`、`SchemaYamlSchema`）和通过 `z.infer<>` 推导的类型
- [x] 1.2 为运行时状态定义 `CompletedSet`（Set<string>）、`BlockedArtifacts` 和 `ArtifactGraphResult` 类型

## 2. schema 解析器
- [x] 2.1 创建 `src/core/artifact-graph/schema.ts`，包含 YAML 加载和通过 `.safeParse()` 的 Zod 验证
- [x] 2.2 实现依赖引用验证（确保 `requires` 引用有效的制品 ID）
- [x] 2.3 实现重复制品 ID 检测
- [x] 2.4 在 schema 加载期间添加循环检测（错误格式："检测到循环依赖：A → B → C → A"）

## 3. 制品图核心
- [x] 3.1 创建包含 ArtifactGraph 类的 `src/core/artifact-graph/graph.ts`
- [x] 3.2 实现 `fromYaml(path)` - 从 schema 文件加载图
- [x] 3.3 实现 `getBuildOrder()` - 通过 Kahn 算法进行拓扑排序
- [x] 3.4 实现 `getArtifact(id)` - 检索单个制品定义
- [x] 3.5 实现 `getAllArtifacts()` - 列出所有制品

## 4. 状态检测
- [x] 4.1 创建包含状态检测逻辑的 `src/core/artifact-graph/state.ts`
- [x] 4.2 实现简单路径的文件存在性检查
- [x] 4.3 实现多文件制品的 glob schema 匹配
- [x] 4.4 实现 `detectCompleted(graph, changeDir)` - 扫描文件系统并返回 CompletedSet
- [x] 4.5 优雅处理缺失的 changeDir（返回空的 CompletedSet）

## 5. 就绪计算
- [x] 5.1 实现 `getNextArtifacts(graph, completed)` - 查找所有依赖已完成的制品
- [x] 5.2 实现 `isComplete(graph, completed)` - 检查是否所有制品已完成
- [x] 5.3 实现 `getBlocked(graph, completed)` - 返回 BlockedArtifacts 映射（制品 → 未满足的依赖）

## 6. schema 解析
- [x] 6.1 创建包含 schema 解析逻辑的 `src/core/artifact-graph/resolver.ts`
- [x] 6.2 添加 `getGlobalDataDir()` 到 `src/core/global-config.ts`（XDG_DATA_HOME 带平台回退）
- [x] 6.3 实现 `resolveSchema(name)` - 全局（`${XDG_DATA_HOME}/openspec/schemas/`）→ 内置回退

## 7. 内置 schema
- [x] 7.1 创建 `src/core/artifact-graph/schemas/spec-driven.yaml`（默认：proposal → specs → design → tasks）
- [x] 7.2 创建 `src/core/artifact-graph/schemas/tdd.yaml`（替代方案：tests → implementation → docs）

## 8. 集成
- [x] 8.1 创建包含公共导出的 `src/core/artifact-graph/index.ts`

## 9. 测试
- [x] 9.1 测试：解析有效 schema YAML 返回正确的制品图
- [x] 9.2 测试：解析无效 schema（缺少字段）抛出描述性错误
- [x] 9.3 测试：重复制品 ID 抛出错误
- [x] 9.4 测试：无效的 `requires` 引用抛出错误，标识无效的 ID
- [x] 9.5 测试：schema 中的循环抛出错误，列出循环路径（例如 "A → B → C → A"）
- [x] 9.6 测试：计算构建顺序返回正确的拓扑顺序（线性链）
- [x] 9.7 测试：计算构建顺序正确处理菱形依赖
- [x] 9.8 测试：独立制品以稳定顺序返回
- [x] 9.9 测试：空/缺失的 changeDir 返回空的 CompletedSet
- [x] 9.10 测试：文件存在性将制品标记为已完成
- [x] 9.11 测试：Glob schema specs/*.md 在文件存在时检测为完成
- [x] 9.12 测试：Glob schema 空目录不标记为完成
- [x] 9.13 测试：getNextArtifacts 在无已完成内容时仅返回根制品
- [x] 9.14 测试：getNextArtifacts 包含所有依赖已完成的制品
- [x] 9.15 测试：getBlocked 返回制品及所有未满足的依赖列表
- [x] 9.16 测试：isComplete() 在所有制品完成时返回 true
- [x] 9.17 测试：isComplete() 在某些制品未完成时返回 false
- [x] 9.18 测试：schema 解析在全局覆盖之前优先于内置
- [x] 9.19 测试：schema 解析在无全局时回退到内置
