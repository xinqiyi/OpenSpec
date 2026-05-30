# 设计：Zod 验证框架

## 架构决策

### 验证级别
三级验证系统：
1. **ERROR**：阻止解析的结构性问题（必须修复）
2. **WARNING**：应解决的质量问题（建议修复）
3. **INFO**：改进建议（可选）

**理由：**
- 渐进式执行允许团队逐步采用验证
- CI/CD 可以在错误上失败，但最初允许警告
- 信息级别在不阻塞的情况下提供指导

### 验证规则层级

#### spec 验证规则
```
ERROR 级别：
- 缺少 ## Overview 或 ## Requirements 部分
- 无效的标题层级
- 格式错误的需求/场景结构

WARNING 级别：
- 没有场景的需求
- 缺少 SHALL 关键词的需求
- 空的概述部分

INFO 级别：
- 非常长的需求文本（超过 500 字符）
- 没有 Given/When/Then 结构的场景
```

#### 变更验证规则
```
ERROR 级别：
- 缺少 ## Why 或 ## What Changes 部分
- 无效的差异操作类型
- 格式错误的差异结构

WARNING 级别：
- Why 部分太短（少于 50 字符）
- 没有清晰描述的差异
- 在 ADDED/MODIFIED 中缺少需求

INFO 级别：
- 非常长的 why 部分（超过 1000 字符）
- 单个变更中差异过多（超过 10 个）
```

### 严格 schema
- **默认**：显示所有级别，仅在 ERROR 上失败
- **--strict 标志**：在 ERROR 和 WARNING 上都失败
- **用例**：CI/CD 管道中的逐步质量改进

### Archive 命令安全性
**问题：** 无效的 spec 可能被 archive，污染 archive 库。

**解决方案：**
1. archive 前验证（默认行为）
2. --no-validate 标志带安全措施：
 - 交互式确认提示
 - 显著警告消息
 - 带时间戳的控制台日志记录
 - 不推荐用于 CI/CD 使用

**理由：**
- 默认保护 archive 完整性
- 允许带问责的紧急覆盖
- 清晰的验证绕过审计跟踪

### 验证报告格式
```json
{
 "valid": boolean,
 "issues": [
 {
 "level": "ERROR" | "WARNING" | "INFO",
 "path": "requirements[0].scenarios",
 "message": "Requirement must have at least one scenario",
 "line": 15,
 "column": 0
 }
 ],
 "summary": {
 "errors": 2,
 "warnings": 5,
 "info": 3
 }
}
```

**好处：**
- 机器可读，便于工具集成
- 人类友好的消息
- 行/列信息用于 IDE 集成
- 摘要用于快速评估

### 实现策略
1. **带细化的 Zod schemas**：类型定义中的内置验证
2. **自定义验证器**：额外的业务逻辑验证
3. **可组合规则**：为不同上下文混合搭配
4. **可扩展框架**：无需重构即可轻松添加新规则
