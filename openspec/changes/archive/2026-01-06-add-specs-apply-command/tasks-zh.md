## 任务

### 核心实现

- [x] 将规范应用逻辑从 `ArchiveCommand` 提取到 `src/core/specs-apply.ts`
  - 将 `buildUpdatedSpec()`、`findSpecUpdates()`、`writeUpdatedSpec()` 移动到共享模块
  - 保持 `ArchiveCommand` 从新模块导入
  - 确保所有验证逻辑得以保留

### 技能模板

- [x] 在 `src/core/templates/skill-templates.ts` 中添加 `getSyncSpecsSkillTemplate()` 函数
  - 技能名称：`openspec-sync-specs`
  - 描述：将 delta 规范同步到主规范
  - **Agent 驱动**：指示 Agent 读取 delta 并直接编辑主规范的指令

- [x] 在 `skill-templates.ts` 中添加 `/opsx:sync` 斜杠命令模板
  - 镜像技能模板以适应斜杠命令格式
  - **Agent 驱动**：无 CLI 命令，Agent 执行合并

### 注册

- [x] 在托管技能中注册技能（通过 `artifact-experimental-setup`）
  - 以适当的元数据添加到技能列表
  - 确保它出现在设置输出中

### 设计决策

**为什么是 Agent 驱动而不是 CLI 驱动？**

程序化合并以需求级别粒度操作：
- MODIFIED 需要复制所有场景，而不仅仅是变更的场景
- 如果 Agent 忘记了一个场景，它会被删除
- Delta 规范因复制的内容而变得臃肿

Agent 驱动的方法：
- Agent 可以应用部分更新（添加场景而不复制其他场景）
- Delta 表示*意图*，而不是整体替换
- 更灵活和自然的编辑工作流
- 归档仍然使用程序化合并（用于最终确定的变更）
