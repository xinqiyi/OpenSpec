# 添加集合基础证据

## 研究总结

子 agent 和本地审查得出了相同的方向：

- 项目 4 应定义存储身份与产品特定内容含义之间的界限。
- 集合层应拥有挂载的命名空间和逻辑路径围栏。
- 上下文存储层应保持内容无关。
- 倡议 CRUD 和倡议文件结构属于项目 5。
- 目前运行时注入的注册表已足够；持久化清单和动态插件为时过早。
- 一个薄注册外观应隐藏元数据和本地注册表写入，但项目 4 不应依赖该外观。

## 清洁代码说明

- 使用模块边界和挂载对象来携带上下文。
- 在集合模块内优先使用 `validateMount`、`parseCollectionPath`、`createCollectionRegistry` 和 `mountCollections`。
- 避免将每个概念堆叠在一起的公共辅助函数名称，例如 `validateContextStoreCollectionRelativePath`。
- 在未来的写能力层有意处理符号链接、spec 父路径和后端行为之前，保持路径解析纯粹和词法化。
- 将持久化 YAML 形状保持在公共设置表面之下。运行时/公共处理应使用 camelCase 字段如 `storeRoot`；持久化后端状态可以继续使用 `local_path`。

## 选择的 schema

使用两步 schema：

```ts
const store = await registerContextStore({
 id: "acme-context",
 backend: gitLocalBackend({
 localPath: "/Users/me/repos/acme-context",
 remote: "git@github.com:acme/context.git",
 branch: "main",
 }),
});

const collections = createCollectionRegistry([
 { id: "initiatives", mount: "initiatives" },
]);

const mounted = mountCollections({
 storeRoot: store.storeRoot,
 collections,
});
```

对于项目 4 本身，`mountCollections({ storeRoot, collections })` 是 spec API。一键设置外观、存储生命周期对象、构建器 DSL 和倡议特定设置预设都推迟了。

## 实施证据

- `src/core/collections/runtime.ts` 定义了运行时集合定义、注册表、挂载集合上下文、逻辑路径解析和挂载/路径解析。
- `src/core/collections/index.ts` 导出集合模块，`src/core/index.ts` 为消费者重新导出它。
- `test/core/collections/runtime.test.ts` 涵盖了挂载和 ID 验证、逻辑路径解析、重复 ID/挂载拒绝、Windows 风格根路径、`createHandle(context)`、无文件系统创建以及通用 `initiatives/` 挂载。

## 验证

- `pnpm exec vitest run test/core/collections/runtime.test.ts`
- `pnpm run build`
- `pnpm exec vitest run test/core/collections/runtime.test.ts test/core/context-store/foundation.test.ts test/core/planning-home.test.ts`
- `pnpm exec vitest run test/utils/file-system.test.ts`
- `pnpm run lint`
- `git diff --check`
