# 任务

## 1. 项目配置
- [x] 1.1 创建包含项目元数据、脚本和 ESM 配置的 package.json
- [x] 1.2 使用 tsconfig.json 配置 TypeScript 以输出 ESM
- [x] 1.3 为 Node.js/TypeScript 项目添加 .gitignore
- [x] 1.4 设置 Node.js 引擎要求为 >=20.19.0

## 2. 目录结构
- [x] 2.1 创建 src/ 目录用于源代码
- [x] 2.2 创建 src/cli/ 目录用于 CLI 命令
- [x] 2.3 创建 src/core/ 目录用于核心 OpenSpec 逻辑
- [x] 2.4 创建 src/utils/ 目录用于共享工具

## 3. 构建配置
- [x] 3.1 创建用于原生 TypeScript 编译的 build.js
- [x] 3.2 配置开发脚本（build、dev）
- [x] 3.3 使用 ESM 导出设置包入口点
- [x] 3.4 配置 ESM 的正确文件扩展名处理

## 4. 初始依赖
- [x] 4.1 将 TypeScript 添加为开发依赖
- [x] 4.2 添加 commander 用于 CLI 框架
- [x] 4.3 添加 @inquirer/prompts 用于用户交互
- [x] 4.4 添加必要的类型定义
