# 技术设计

## 架构决策

### 简单至上
- 无版本跟踪 - 始终在命令执行时更新
- 仅对 OpenSpec 管理的文件进行完全替换（例如 `openspec/README.md`）
- 对用户拥有的文件进行基于标记的更新（例如 `CLAUDE.md`）
- template 与包捆绑 - 无需网络
- 最小化错误处理 - 仅检查前提条件

### template 策略
- 使用现有 template 工具
 - 来自 `src/core/templates/readme-template.ts` 的 `readmeTemplate` 用于 `openspec/README.md`
 - `TemplateManager.getClaudeTemplate()` 用于 `CLAUDE.md`
- 目录名称固定为 `openspec`（来自 `OPENSPEC_DIR_NAME`）

### 文件操作
- 使用异步工具以保持一致性
 - `FileSystemUtils.writeFile` 用于 `openspec/README.md`
 - `FileSystemUtils.updateFileWithMarkers` 用于 `CLAUDE.md`
- 不需要原子操作 - 用户有 git
- 在继续之前检查目录是否存在

## 实现

### 更新命令（`src/core/update.ts`）
```typescript
export class UpdateCommand {
 async execute(projectPath: string): Promise<void> {
 const openspecDirName = OPENSPEC_DIR_NAME;
 const openspecPath = path.join(projectPath, openspecDirName);

 // 1. 检查 openspec 目录是否存在
 if (!await FileSystemUtils.directoryExists(openspecPath)) {
 throw new Error(`未找到 OpenSpec 目录。请先运行 'openspec init'。`);
 }

 // 2. 更新 README.md（完全替换）
 const readmePath = path.join(openspecPath, 'README.md');
 await FileSystemUtils.writeFile(readmePath, readmeTemplate);

 // 3. 更新 CLAUDE.md（基于标记）
 const claudePath = path.join(projectPath, 'CLAUDE.md');
 const claudeContent = TemplateManager.getClaudeTemplate();
 await FileSystemUtils.updateFileWithMarkers(
 claudePath,
 claudeContent,
 OPENSPEC_MARKERS.start,
 OPENSPEC_MARKERS.end
 );

 // 4. 成功消息（ASCII 安全，勾选标记可选，取决于终端）
 console.log('已更新 OpenSpec 指令');
 }
}
```

## 为什么采用此方案

### 好处
- **极简**：总共约 40 行代码
- **快速**：无版本检查，最小化解析
- **可预测**：每次结果相同；幂等
- **可维护**：重用现有工具

### 接受的权衡
- 无版本跟踪（不必要的复杂性）
- 仅对 OpenSpec 管理的文件进行完全覆盖
- 对用户拥有的文件进行基于标记的更新

## 错误处理

仅处理关键错误：
- 缺失 `openspec` 目录 → 抛出错误，由 CLI 处理以显示友好消息
- 文件写入失败 → 让错误冒泡到 CLI

## 测试策略

手动冒烟测试初始即足够：
1. 在测试项目中运行 `openspec init`
2. 修改两个文件（包括 `CLAUDE.md` 中标记周围的自定义内容）
3. 运行 `openspec update`
4. 验证 `openspec/README.md` 完全替换；`CLAUDE.md` 的 OpenSpec 块更新而不更改标记外的用户内容
5. 运行命令两次以验证幂等性和无重复标记
6. 测试缺失 `openspec` 目录的情况（预期失败）
