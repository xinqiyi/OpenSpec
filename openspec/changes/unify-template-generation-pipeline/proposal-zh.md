## 原因

最近将 `skill-templates.ts` 拆分为 workflow 模块提高了可读性，但生成流水线仍然分散在多个层中：

- workflow 定义与投影逻辑分离（`getSkillTemplates`、`getCommandTemplates`、`getCommandContents`）
- 工具能力和兼容性分布在 `AI_TOOLS`、`CommandAdapterRegistry` 和硬编码列表（如 `SKILL_NAMES`）之间
- agent/工具特定的转换（例如 OpenCode 命令引用重写）在不同的地方应用（`init`、`update` 和适配器代码）
- artifact 写入逻辑在 `init`、`update` 和遗留升级流程之间重复

这种分散造成了漂移风险（缺少导出、缺少元数据一致性、数量/支持不匹配），并使未来的 workflow/工具添加变得更慢且更不可预测。

## 变更内容

- 引入一个 spec 的 `WorkflowManifest` 作为所有 artifact 事实的单一来源
- 引入一个 `ToolProfileRegistry` 来集中管理工具能力（skill 路径、命令适配器、转换）
- 引入一个具有显式阶段（`preAdapter`、`postAdapter`）和作用域（`skill`、`command`、`both`）的一级转换流水线
- 引入一个由 `init`、`update` 和遗留升级路径使用的共享 `ArtifactSyncEngine`
- 添加严格的验证和测试护栏，以在迁移和未来变更期间保持保真度

## 能力

### 新能力

- `template-artifact-pipeline`：统一的 workflow 清单、工具配置文件注册表、转换流水线和 skill/命令生成的同步引擎

### 修改的能力

- `command-generation`：扩展为支持适配器渲染周围的有序转换阶段
- `cli-init`：使用共享的 artifact 同步编排，而非特制的循环
- `cli-update`：使用共享的 artifact 同步编排，而非特制的循环

## 影响

- **主要重构区域**：
 - `src/core/templates/*`
 - `src/core/shared/skill-generation.ts`
 - `src/core/command-generation/*`
 - `src/core/init.ts`
 - `src/core/update.ts`
 - `src/core/shared/tool-detection.ts`
- **测试新增**：
 - 清单完整性测试（workflow、必需元数据、投影一致性）
 - 转换排序和适用性测试
 - 跨工具的端到端校验测试，用于生成的 skill/命令输出
- **面向用户的行为**：
 - 不需要新的 CLI 表面积
 - 除非在未来的 delta 中明确更改，否则现有生成的 artifact 在行为上保持等效
