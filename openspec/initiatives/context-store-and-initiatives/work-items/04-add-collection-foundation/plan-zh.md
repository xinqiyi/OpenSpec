# 添加集合基础

## 状态

第一个实施切片已完成。

## 权威来源

从 `../../direction.md` 开始。

相关模型是：

```text
上下文存储同步真理。
集合塑造真理。
倡议协调工作。
工作区打开本地视图。
变更实现仓库拥有的切片。*
```

## 目标

添加最小的集合基础，使产品特定内容系统可以在上下文存储内挂载，而无需上下文存储层知道这些系统的含义。

## 已锁定的方向

- 将项目 4 视为挂载/路径基础，而非集合运行时。
- 保持集合组合仅为运行时和依赖注入。
- 保持上下文存储注册与运行时集合挂载分离。
- 使用未来的薄注册外观进行元数据/注册表设置，而不是在公共示例中显示原始注册表或元数据状态写入。
- 暂不添加持久化集合清单。
- 暂不添加 CLI 行为。
- 暂不添加通用 `read`、`write`、`list` 或 `delete` 辅助函数。
- 暂不添加倡议文件结构、倡议 CRUD 或倡议验证。
- 证明 `initiatives/` 可以通过通用集合定义挂载，而不是通过倡议特定的上下文存储逻辑。

## 命名方向

使用模块/对象边界来携带上下文，而不是增长辅助函数名称。

使用专注的通用模块，如 `src/core/collections/runtime.ts`，使用短名称：

```ts
validateCollectionId(id);
validateMount(mount);
parseCollectionPath(input);

createCollectionRegistry(...);
mountCollections(...);
```

偏好挂载对象进行上下文感知操作：

```ts
const mounted = collections.require("initiatives");

mounted.resolvePath("launch-billing-flow/initiative.yaml");
mounted.toStorePath("launch-billing-flow/initiative.yaml");
```

避免像 `validateContextStoreCollectionRelativePath` 这样的名称。它们表明过多的上下文已泄露到独立的辅助函数名称中。

## 最小 API 形状

第一个切片应保持接近以下内容：

```ts
interface CollectionDefinition<THandle = unknown> {
  id: string;
  mount: string;
  metadata?: CollectionMetadata;
  hooks?: CollectionHooks;
  createHandle?: (context: MountedCollectionContext) => THandle;
}

interface MountedCollectionContext {
  storeRoot: string;
  collectionId: string;
  mount: string;
  mountRoot: string;
  resolvePath(relativePath?: string): string;
  toStorePath(relativePath?: string): string;
}

interface MountedCollection<THandle = unknown> {
  collectionId: string;
  mount: string;
  mountRoot: string;
  context: MountedCollectionContext;
  handle: THandle | undefined;
}
```

在定义上使用 `id`，但在挂载的处理和上下文中使用 `collectionId`，这样领域对象 ID（如倡议 ID）不会与集合类型 ID 冲突。

## 设置和挂载模式

使用两个独立的层：

1. 用于设置的上下文存储注册外观。
2. 用于项目 4 的纯运行时集合挂载 API。

注册应隐藏持久化 YAML 细节：

```ts
const store = await registerContextStore({
  id: "acme-context",
  backend: gitLocalBackend({
    localPath: "/Users/me/repos/acme-context",
    remote: "git@github.com:acme/context.git",
    branch: "main",
  }),
});
```

注册外观可以在内部调用较低级别的辅助函数，如后端配置规范化、元数据写入和本地注册表写入。公共示例不应调用原始的 `writeContextStoreMetadataState(...)`、`writeContextStoreRegistryState(...)` 或暴露持久化的 snake_case 后端状态如 `local_path`。

项目 4 的挂载应保持独立于注册，并且只接受它需要的权限：

```ts
const collections = createCollectionRegistry([
  { id: "initiatives", mount: "initiatives" },
]);

const mounted = mountCollections({
  storeRoot: store.storeRoot,
  collections,
});

mounted.require("initiatives").resolvePath(
  "launch-billing-flow/initiative.yaml"
);
```

优先使用 `mountCollections({ storeRoot, collections })` 作为规范的第一个 API。传递整个存储句柄可以等到真正需要时再进行。

## 路径方向

- 挂载名称是单段 kebab-case 文件夹名称，如 `initiatives`、`decisions` 或 `api-catalog`。
- 集合相对路径是挂载内的逻辑可移植路径。
- 路径解析器仅是词法化的。它证明逻辑路径属于集合挂载下；它不声称是文件系统安全沙箱。
- 未来的写能力辅助函数在接触磁盘之前必须重新审视符号链接和规范父路径处理。

拒绝：

- 空挂载
- `.`
- `..`
- 隐藏/保留挂载，如 `.openspec-store`
- 绝对路径
- Windows 驱动器路径
- UNC 路径
- NUL 字节
- 遍历段
- 兄弟前缀逃逸

## 推迟

- 存储级集合配置文件。
- 动态插件加载。
- 一键 `setupContextStore({ id, backend, collections })` API。
- `createStore(...).setup()` 生命周期 API。
- 构建器风格设置 DSL。
- 通用上下文存储层中的倡议特定设置预设。
- 模板覆盖搜索路径。
- 丰富验证执行。
- 代理指导生成。
- 工作区集成。
- Git 同步、提交、拉取、推送、监视或冲突行为。

## 已实现的切片

- 在 `src/core/collections/runtime.ts` 添加了纯运行时集合模块。
- 通过 `src/core/collections/index.ts` 和 `src/core/index.ts` 导出了该模块。
- 在 `test/core/collections/runtime.test.ts` 下添加了专注的测试。
- 证明了通用 `{ id: "initiatives", mount: "initiatives" }` 定义可以在没有倡议特定存储逻辑的情况下挂载和解析路径。
- 将验证/模板钩子保留为惰性扩展字段；丰富的钩子执行仍然推迟。
