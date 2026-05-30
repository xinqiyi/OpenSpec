## 1. 反馈命令

- [x] 1.1 在 `src/commands/feedback.ts` 中创建命令实现
- [x] 1.2 使用平台适当的命令检查 `gh` CLI 可用性（Unix/macOS 上使用 `which`，Windows 上使用 `where`）
- [x] 1.3 使用 `gh auth status` 检查 GitHub 认证状态
- [x] 1.4 使用 `execFileSync` 执行 `gh issue create`，附带格式化标题和正文，以防止 shell 注入
- [x] 1.5 显示 `gh` CLI 返回的问题 URL
- [x] 1.6 在 `src/cli/index.ts` 中注册 `feedback <message>` 命令
- [x] 1.7 确保跨平台兼容性（macOS、Linux、Windows）

## 2. Shell 补全

- [x] 2.1 将 `feedback` 命令添加到命令注册表
- [x] 2.2 为所有 shell 重新生成补全脚本

## 3. 反馈技能

- [x] 3.1 在 `skill-templates.ts` 中创建反馈技能模板
- [x] 3.2 记录上下文收集工作流
- [x] 3.3 记录匿名化规则
- [x] 3.4 记录用户确认流程

## 4. 测试

- [x] 4.1 为反馈命令添加单元测试（模拟 `gh` 子进程调用）
- [x] 4.2 使用模拟的 `gh` CLI 为完整反馈流程添加集成测试
- [x] 4.3 测试缺少 `gh` CLI 时的错误处理
- [x] 4.4 测试未认证 `gh` 会话时的错误处理
- [x] 4.5 测试跨平台 `gh` CLI 检测（验证 Unix 上的 `which`，Windows 上的 `where`）
- [x] 4.6 测试平台元数据包含 Windows 的正确值（win32）
