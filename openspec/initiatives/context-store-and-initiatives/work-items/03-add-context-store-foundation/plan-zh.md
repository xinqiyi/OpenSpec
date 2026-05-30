# 添加上下文存储基础

## 状态

注册/解析外观层已实现。

## 事实来源

从 `../direction.md` 开始。

相关模型是：

```text
上下文存储同步事实。
集合塑造事实。
倡议协调工作。
工作区打开本地视图。
变更实现仓库拥有的切片。
```

## 目标

为上下文存储添加最小的核心基础，而不让存储层知道倡议、集合、工作区或仓库本地变更。

## 锁定方向

- 第一个切片支持一个后端：Git/本地检出后端。
- 将实际上下文存储根视为用户选择的本地 Git 检出或同步文件夹。
- 默认不将真实团队上下文存储隐藏在 XDG 数据下。
- 将机器本地注册表存储在全局数据下：`$XDG_DATA_HOME/openspec/context-stores/registry.yaml`。
- 将可移植上下文存储身份存储在存储根内：`<store-root>/.openspec-store/store.yaml`。
- 从后端身份/配置、严格验证、路径助手和注册表/元数据读/写助手开始。
- 在倡议 CLI 接线之前添加一个薄的注册/解析外观层，以便调用方不直接操作原始注册表和元数据 YAML。
- 不重新实现 TypeScript 或 Node 文件系统 API 作为公共存储接口。
- 在此切片中不添加倡议、集合、工作区打开、同步、拉取、推送或 CLI 行为。

## 初始形态

机器本地注册表：

```yaml
version: 1
stores:
  acme-context:
    backend:
      type: git
      local_path: /Users/me/repos/acme-context
      remote: git@github.com:acme/context.git
      branch: main
```

存储根中的可移植元数据：

```yaml
version: 1
id: acme-context
```

## 可能的仓库切片

- 添加 `src/core/context-store/foundation.ts`。
- 添加 `src/core/context-store/registry.ts`。
- 添加 `src/core/context-store/index.ts`。
- 从 `src/core/index.ts` 导出核心上下文存储基础。
- 在 `test/core/context-store/` 下添加针对性测试。
- 在有意暴露行为/API 契约之前保持规范不变。

## 已实现的外观层切片

- 添加了 `registerContextStore(...)`。
- 添加了 `listRegisteredContextStores(...)`。
- 添加了 `resolveRegisteredContextStore(...)`。
- 注册在缺失时写入可移植存储元数据，在存在时验证现有元数据，并合并/更新机器本地注册表。
- 解析验证注册表 ID 与存储根元数据 ID 匹配。
- 未添加 Git 克隆、拉取、推送、同步、工作区状态、集合清单或 CLI 行为。
