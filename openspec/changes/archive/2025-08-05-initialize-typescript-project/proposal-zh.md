# 初始化 TypeScript 项目

## 为什么
OpenSpec 项目需要适当的 TypeScript 基础来构建最小化的 CLI，帮助开发者设置 OpenSpec 文件结构并保持 AI 指令更新。

## 变更内容
- 使用 ESM 模块创建 TypeScript 项目配置（package.json、tsconfig.json）
- 建立 CLI 实现的基础目录结构
- 配置构建脚本和开发工具
- 添加 CLI 开发所需的必要依赖
- 为 Node.js/TypeScript 项目创建 .gitignore
- 设置最低 Node.js 版本为 20.19.0 以获得原生 ESM 支持

## 影响
- 受影响的规范：无（初始项目设置）
- 受影响的代码：无（全新项目）
- 新目录：src/、dist/、node_modules/
- 新文件：package.json、tsconfig.json、.gitignore、build.js
