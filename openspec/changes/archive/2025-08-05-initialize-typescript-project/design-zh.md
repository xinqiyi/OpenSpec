# 技术设计

## 技术选择

### TypeScript 配置
- **严格 schema**：启用所有严格类型检查以获得更好的 AI 理解
- **目标**：ES2022 以获得现代 JavaScript 特性
- **模块**：ES2022 以获得现代 ESM 支持
- **模块解析**：Node 以获得正确的包解析
- **输出**：dist/ 目录用于编译后的 JavaScript
- **源映射**：启用以便直接调试 TypeScript
- **声明文件**：生成 .d.ts 文件用于类型定义
- **ES 模块互操作**：true 以获得更好的 CommonJS 兼容性
- **跳过库检查**：false 以确保所有类型都经过验证

### 包结构
```
openspec
├── bin/ # CLI 入口点
├── dist/ # 编译后的 JavaScript
├── src/ # TypeScript 源代码
│ ├── cli/ # 命令实现
│ ├── core/ # 核心 OpenSpec 逻辑
│ └── utils/ # 共享工具
├── package.json
├── tsconfig.json
└── build.js # 构建脚本
```

### 依赖策略
- **最小依赖**：仅必要的包
- **commander**：行业标准 CLI 框架
- **@inquirer/prompts**：现代提示库
- **无重型框架**：直接、可读的实现

### 构建方法
- 通过 tsc 的原生 TypeScript 编译
- 用于打包的简单 build.js 脚本
- 无需复杂的构建工具链
- ESM 输出，导入中包含正确的 .js 扩展名

### 开发 workflow
1. `pnpm install` - 安装依赖
2. `pnpm run build` - 编译 TypeScript
3. `pnpm run dev` - 开发 schema
4. `pnpm link` - 本地测试 CLI

### Node.js 要求
- **最低版本**：Node.js 20.19.0
- **推荐**：Node.js 22 LTS
- **理由**：无需标志即可完全支持 ESM，现代 JavaScript 特性

### ESM 配置
- **包类型**：package.json 中设置 `"type": "module"`
- **文件扩展名**：在 TypeScript 导入中使用 .js 扩展名（正确编译）
- **顶级 await**：可用于更清晰的异步初始化
- **面向未来**：与 JavaScript 标准对齐

### TypeScript 最佳实践
- **所有代码使用 TypeScript**：src/ 中无 .js 文件，只有 .ts
- **显式类型**：在能增加清晰度的地方优先使用显式类型而非推断
- **接口优于类型**：对象形状使用接口，联合/别名使用类型
- **无 any**：严格 schema 防止隐式 any，需要时使用 unknown
- **Async/await**：全程使用现代异步 schema
