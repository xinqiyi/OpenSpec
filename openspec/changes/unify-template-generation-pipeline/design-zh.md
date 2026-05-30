## 上下文

OpenSpec 目前拥有强大的构建模块（workflow template、命令适配器、生成辅助函数），但编排关注点分散在各处：

- workflow 定义和投影列表分开维护
- 工具支持在多个地方表示，存在部分重叠
- 转换可以在 template 渲染时和各个适配器内部发生
- `init`/`update`/legacy-upgrade 各自运行类似但略有差异的写入流水线

设计目标是在保留当前行为的同时，使扩展点明确和确定。

## 目标 / 非目标

**目标：**
- 为 workflow 内容和元数据定义一个 spec 的单一来源
- 使工具/agent 特定行为明确且可集中发现
- 将命令适配器保持为工具语法差异的格式化边界
- 将 artifact 生成/写入编排整合到一个可重用的引擎中
- 通过可强制执行的验证和校验测试提高正确性

**非目标：**
- 重新设计命令语义或 workflow 指令内容
- 在本 proposal 中更改面向用户的 CLI 命令名称/标志
- 合并超出 artifact 生成重用的无关遗留清理行为

## 决策

### 1. spec 的 `WorkflowManifest`

**决策**：在清单条目中一次性表示每个 workflow，包含 spec 的 skill 和命令定义以及元数据默认值。

建议形状：

```ts
interface WorkflowManifestEntry {
 workflowId: string; // 例如 'explore', 'ff', 'onboard'
 skillDirName: string; // 例如 'openspec-explore'
 skill: SkillTemplate;
 command?: CommandTemplate;
 commandId?: string;
 tags: string[];
 compatibility: string;
}
```

**理由**：
- 消除多个手动维护数组之间的漂移
- 使 workflow 完整性可在一处测试
- 保持 workflow 模块分离的同时集中注册

### 2. 用于能力连接的 `ToolProfileRegistry`

**决策**：添加一个将工具 ID 映射到生成能力和行为的工具配置文件层。

建议形状：

```ts
interface ToolProfile {
 toolId: string;
 skillsDir?: string;
 commandAdapterId?: string;
 transforms: string[];
}
```

**理由**：
- 防止 `AI_TOOLS`、适配器注册表和检测逻辑之间的能力漂移
- 允许有意的"仅 skill"工具，无需隐式特殊处理
- 提供一个地方回答"这个工具支持什么？"

### 3. 一级转换流水线

**决策**：将转换建模为具有 scope + phase + applicability 的有序插件。

建议形状：

```ts
interface ArtifactTransform {
 id: string;
 scope: 'skill' | 'command' | 'both';
 phase: 'preAdapter' | 'postAdapter';
 priority: number;
 applies(ctx: GenerationContext): boolean;
 transform(content: string, ctx: GenerationContext): string;
}
```

执行顺序：
1. 从清单渲染 spec 内容
2. 应用匹配的 `preAdapter` 转换
3. 对于命令，运行适配器格式化
4. 应用匹配的 `postAdapter` 转换
5. 验证并写入

**理由**：
- 保持适配器专注于工具格式化，而非分散的行为重写
- 使 agent 特定的修改变得明确和可测试
- 替换 `init`/`update` 中的临时转换调用

### 4. 共享的 `ArtifactSyncEngine`

**决策**：引入一个由所有生成入口点使用的单一编排引擎。

职责：
- 从 `(workflows × selected tools × artifact kinds)` 构建生成计划
- 运行渲染/转换/适配器流水线
- 验证输出
- 写入文件并返回结果摘要

**理由**：
- 移除 init/update 路径中重复的循环和不同的行为
- 支持 dry-run 和未来的预览功能，无需重新实现逻辑
- 提高更新和遗留迁移的可靠性

### 5. 验证 + 校验护栏

**决策**：在测试中添加严格检查（以及开发构建中的可选运行时断言），包括：

- 所有清单条目都存在必需的 skill 元数据字段（`license`、`compatibility`、`metadata`）
- 投影一致性（从清单派生的 skill、命令、检测名称）
- 工具配置文件一致性（适配器存在性、预期能力）
- 关键 workflow/工具的黄金/校验输出

**理由**：
- 将先前的审查问题转化为强制不变量
- 在允许内部重构的同时保持输出保真度
- 使回归在 CI 中显而易见

## 风险 / 权衡

**风险：迁移复杂性**
广泛的重构可能破坏生成路径。
→ 缓解措施：分阶段引入，在切换前进行校验测试。

**风险：过度抽象**
太多层可能掩盖简单流程。
→ 缓解措施：保持接口最小化，将注册表与生成代码放在一起。

**权衡：更多前置结构**
添加清单/配置文件/转换注册表增加了概念表面积。
→ 已接受：此成本被减少的漂移和更简单的扩展所抵消。

## 实施方法

1. 在当前公共 API 之后构建清单 + 配置文件 + 转换类型和注册表
2. 重新连接 `getSkillTemplates`/`getCommandContents` 以从清单派生
3. 引入 `ArtifactSyncEngine` 并使 `init` 使用它，同时进行校验检查
4. 将 `update` 和遗留升级流程切换到同一引擎
5. 在校验确认无误后移除重复/硬编码的列表
