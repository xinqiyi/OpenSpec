# ai-tool-paths 增量规范

## 修改的需求

### 需求：支持工具的路径配置

`AI_TOOLS` 数组应包含支持 Agent Skills 规范的工具的 `skillsDir`。

#### 场景：定义 Kimi CLI 路径

- **当** 查找 `kimi` 工具时
- **则** `skillsDir` 应为 `.kimi`
