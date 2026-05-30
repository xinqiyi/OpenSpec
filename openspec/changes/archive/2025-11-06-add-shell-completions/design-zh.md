# Shell 补全设计

## 概述

本设计建立了一个基于插件的 shell 补全架构，优先考虑清晰的 TypeScript 模式、可扩展性和可维护性。该系统分离了 shell 特定的生成逻辑、动态补全数据提供者和安装自动化之间的关注点。

**范围：** 本提案实现了 **仅 Zsh 补全**（Oh My Zsh 优先）。该架构设计用于在未来的提案中支持 bash、fish 和 PowerShell。

## 原生 Shell 补全行为

**设计理念：** 我们与每个 shell 的原生补全系统集成，而不是尝试自定义或统一其行为。这确保了用户熟悉的体验并降低了维护复杂度。

**注意：** 虽然以下记录了所有四种 shell 的行为作为架构参考，**本提案仅实现了 Zsh**。Bash、Fish 和 PowerShell 的文档旨在指导未来的实现。

### Bash 补全行为

**交互模式：**
- **单次 TAB：** 如果只有一项匹配则补全，否则不做任何操作
- **双次 TAB（TAB TAB）：** 以列表形式显示所有可能的补全
- **输入更多字符 + TAB：** 缩小匹配范围并补全或显示优化后的列表

**OpenSpec 集成：**
```bash
# 安装后：openspec completion install bash
openspec val<TAB>           # 补全为 "openspec validate"
openspec validate <TAB><TAB>  # 显示：--all --changes --specs --strict --json [change-ids] [spec-ids]
openspec show add-<TAB><TAB>  # 显示所有以 "add-" 开头的变更
```

**实现：** 使用 bash-completion 框架，包含 `_init_completion`、`compgen` 和 `COMPREPLY` 数组。

### Zsh 补全行为（使用 Oh My Zsh）

**交互模式：**
- **单次 TAB：** 立即显示包含所有匹配项的交互式菜单
- **TAB / 箭头键：** 在补全选项间导航
- **Enter：** 选择高亮选项
- **Ctrl+C / Esc：** 取消补全菜单

**OpenSpec 集成：**
```zsh
# 安装后：openspec completion install zsh
openspec val<TAB>    # 显示菜单，高亮 "validate" 和 "view"
openspec show <TAB>  # 显示菜单，包含所有变更 ID 和 spec ID，已分类
```

**实现：** 使用 Zsh 补全系统，包含 `_arguments`、`_describe` 和 `compadd` 内置命令。Oh My Zsh 自动提供增强的菜单样式。

### Fish 补全行为

**交互模式：**
- **输入时：** 灰色建议自动实时显示
- **右箭头 / Ctrl+F：** 接受建议
- **TAB：** 如果有多个匹配项则显示菜单
- **再次 TAB：** 循环浏览选项或导航菜单
- **Enter：** 接受当前选择

**OpenSpec 集成：**
```fish
# 安装后：openspec completion install fish
openspec val       # 灰色建议立即显示 "validate"
openspec show a    # 以 "a" 开头的变更实时建议
openspec <TAB>     # 在分页菜单中显示所有命令及其描述
```

**实现：** 使用 Fish 声明式的 `complete -c` 语法。补全从 `~/.config/fish/completions/` 自动加载。

### PowerShell 补全行为

**交互模式：**
- **TAB：** 逐个向前循环浏览补全项（内联替换）
- **Shift+TAB：** 向后循环浏览补全项
- **Ctrl+Space：** 显示 IntelliSense 风格菜单（PSReadLine v2.2+）
- **箭头键：** 如果菜单已显示，则导航菜单

**OpenSpec 集成：**
```powershell
# 安装后：openspec completion install powershell
openspec val<TAB>       # 循环：validate → view → validate
openspec show <TAB>     # 逐个循环浏览变更 ID
openspec <Ctrl+Space>   # 显示包含所有命令的 IntelliSense 菜单
```

**实现：** 使用 `Register-ArgumentCompleter`，配合返回 `[System.Management.Automation.CompletionResult]` 对象的自定义脚本块。

### 对比表

| Shell       | 触发方式         | 显示风格                | 导航                 | 选择方式        |
|-------------|-----------------|------------------------|----------------------|----------------|
| Bash        | TAB TAB         | 列表（一次性打印）       | 继续输入 + TAB       | 自动补全       |
| Zsh         | TAB             | 交互式菜单              | TAB/箭头             | Enter          |
| Fish        | TAB/自动        | 实时 + 菜单             | TAB/箭头             | Enter/右箭头   |
| PowerShell  | TAB             | 内联循环                | TAB/Shift+TAB        | 停止循环       |

**关键洞察：** 每个 shell 的补全用户体验反映了其设计理念。我们尊重这些约定，而不是强制统一。

## 架构原则

### 1. 基于插件的生成器系统

每个 shell 都有独特的补全语法和约定。我们不创建带有分支逻辑的单一生成器，而是使用插件模式，每个 shell 实现一个公共接口：

```typescript
interface CompletionGenerator {
  generate(): string;
  getInstallPath(): string;
  getConfigFile(): string;
}
```

**优点：**
- 添加新 shell 无需修改现有生成器
- Shell 特定逻辑被隔离且可测试
- 类型安全确保所有生成器实现所需方法
- 易于维护和理解（每个生成器单一职责）

**实现类：**
- `ZshCompletionGenerator` - 使用 Zsh 的 `_arguments` 和 `_describe` 函数
- `BashCompletionGenerator` - 使用 `_init_completion` 和 `compgen` 内置命令
- `FishCompletionGenerator` - 使用 `complete -c` 声明式语法
- `PowerShellCompletionGenerator` - 使用 `Register-ArgumentCompleter` cmdlet

### 2. 集中式命令注册表

Shell 补全必须与实际 CLI 命令保持同步。为避免重复和漂移，我们维护一个单一事实源：

```typescript
type CommandDefinition = {
  name: string;
  description: string;
  flags: FlagDefinition[];
  acceptsChangeId: boolean;
  acceptsSpecId: boolean;
  subcommands?: CommandDefinition[];
};

const COMMAND_REGISTRY: CommandDefinition[] = [
  {
    name: 'init',
    description: '在你的项目中初始化 OpenSpec',
    flags: [
      { name: '--tools', description: '以非交互方式配置 AI 工具', hasValue: true }
    ],
    acceptsChangeId: false,
    acceptsSpecId: false
  },
  // ... 所有其他命令
];
```

**优点：**
- 所有生成器消费相同的命令定义
- 添加新命令自动传播到所有 shell
- 标志更改只需在一个地方进行
- 类型安全防止拼写错误和缺少字段
- 更易测试（模拟注册表）

**TypeScript 语法糖：**
- 使用 `const` 断言实现只读注册表
- 利用可辨识联合类型处理命令类型
- 使用 `satisfies` 运算符确保注册表匹配接口

### 3. 动态补全提供者

变更和 spec ID 是项目特定的，在运行时发现。一个专门的提供者封装了此逻辑：

```typescript
class CompletionProvider {
  private changeCache: { ids: string[]; timestamp: number } | null = null;
  private specCache: { ids: string[]; timestamp: number } | null = null;
  private readonly CACHE_TTL_MS = 2000;

  async getChangeIds(): Promise<string[]> {
    if (this.changeCache && Date.now() - this.changeCache.timestamp < this.CACHE_TTL_MS) {
      return this.changeCache.ids;
    }

    const ids = await discoverActiveChangeIds();
    this.changeCache = { ids, timestamp: Date.now() };
    return ids;
  }

  async getSpecIds(): Promise<string[]> {
    // 类似的缓存逻辑
  }

  isOpenSpecProject(): boolean {
    // 检查 openspec/ 目录
  }
}
```

**优点：**
- 缓存在快速 Tab 补全期间减少文件系统开销
- 封装项目检测逻辑
- 使用模拟文件系统易于测试
- 在所有 shell 生成器间共享

**设计决策：**
- 2 秒缓存 TTL 在新鲜度和性能之间取得平衡
- 每个进程的缓存（非持久化），避免跨会话的过期数据
- 在 OpenSpec 项目外优雅降级

### 4. 独立的安装逻辑

安装涉及 shell 配置文件的操控，与生成不同。我们分离此关注点：

```typescript
interface CompletionInstaller {
  install(): Promise<InstallResult>;
  uninstall(): Promise<UninstallResult>;
  isInstalled(): Promise<boolean>;
}
```

**特定 Shell 的安装器：**
- `ZshInstaller` - 处理 Oh My Zsh（自定义补全）和标准 Zsh（fpath）
- `BashInstaller` - 检测补全目录并从 `.bashrc` 中 source
- `FishInstaller` - 写入 `~/.config/fish/completions/`（自动加载）
- `PowerShellInstaller` - 追加到 PowerShell 配置文件

**优点：**
- 安装逻辑不污染生成器代码
- 可以在不生成补全脚本的情况下测试安装
- 更容易处理边界情况（缺少目录、权限、已安装）

### 5. 类型安全的 Shell 检测

我们使用 TypeScript 的字面量类型和类型守卫进行 shell 检测：

```typescript
type SupportedShell = 'bash' | 'zsh' | 'fish' | 'powershell';

function detectShell(): SupportedShell {
  const shellPath = process.env.SHELL || '';
  const shellName = path.basename(shellPath).toLowerCase();

  // PowerShell 标准化
  if (shellName === 'pwsh' || shellName === 'powershell') {
    return 'powershell';
  }

  const supported: SupportedShell[] = ['bash', 'zsh', 'fish', 'powershell'];
  if (supported.includes(shellName as SupportedShell)) {
    return shellName as SupportedShell;
  }

  throw new Error(`Shell '${shellName}' 不受支持。支持的 shell：${supported.join(', ')}`);
}
```

**优点：**
- 编译时类型检查防止无效的 shell 名称
- 易于添加新 shell（添加到联合类型）
- 类型收窄在 switch 语句中有效
- 对不受支持的 shell 给出清晰的错误信息

### 6. 用于实例化的工厂模式

一个工厂函数根据 shell 类型选择合适的生成器/安装器：

```typescript
function createGenerator(shell: SupportedShell, provider: CompletionProvider): CompletionGenerator {
  switch (shell) {
    case 'bash': return new BashCompletionGenerator(COMMAND_REGISTRY, provider);
    case 'zsh': return new ZshCompletionGenerator(COMMAND_REGISTRY, provider);
    case 'fish': return new FishCompletionGenerator(COMMAND_REGISTRY, provider);
    case 'powershell': return new PowerShellCompletionGenerator(COMMAND_REGISTRY, provider);
  }
}
```

**优点：**
- 单一的实例化点
- 类型安全确保穷尽 switch（如果缺少 shell 类型，TypeScript 报错）
- 易于注入依赖（注册表、提供者）

## 命令结构

**本提案（仅 Zsh）：**
```
openspec completion
├── zsh               # 生成 Zsh 补全脚本
├── install [shell]   # 安装 Zsh 补全（自动检测或显式指定 zsh）
└── uninstall [shell] # 移除 Zsh 补全（自动检测或显式指定 zsh）
```

**未来（后续提案后）：**
```
openspec completion
├── bash              # 生成 Bash 补全脚本（未来）
├── zsh               # 生成 Zsh 补全脚本（本提案）
├── fish              # 生成 Fish 补全脚本（未来）
├── powershell        # 生成 PowerShell 补全脚本（未来）
├── install [shell]   # 安装补全（自动检测或显式指定 shell）
└── uninstall [shell] # 移除补全（自动检测或显式指定 shell）
```

## 文件组织

**本提案（仅 Zsh）：**
```
src/
├── commands/
│   └── completion.ts              # CLI 命令注册（zsh, install, uninstall）
├── core/
│   └── completions/
│       ├── types.ts               # 接口：CompletionGenerator, CommandDefinition 等
│       ├── command-registry.ts    # OpenSpec 命令的单一事实源
│       ├── completion-provider.ts # 带缓存的动态变更/spec ID 发现
│       ├── factory.ts             # 用于实例化 Zsh 生成器/安装器的工厂
│       ├── generators/
│       │   └── zsh-generator.ts   # Zsh 补全脚本生成器
│       └── installers/
│           └── zsh-installer.ts   # 处理 Oh My Zsh + 标准 Zsh 安装
└── utils/
    └── shell-detection.ts         # Shell 检测（返回 'zsh' 或抛出异常）
```

**未来添加（bash、fish、powershell）：**
- `generators/bash-generator.ts`、`fish-generator.ts`、`powershell-generator.ts`
- `installers/bash-installer.ts`、`fish-installer.ts`、`powershell-installer.ts`
- 更新 `shell-detection.ts` 以支持更多 shell 类型

## Oh My Zsh 优先

Zsh 实现优先考虑 Oh My Zsh，原因是：
1. **流行度** - Oh My Zsh 是最流行的 Zsh 配置框架
2. **约定** - 有标准的补全目录（`~/.oh-my-zsh/custom/completions/`）
3. **检测** - 通过 `$ZSH` 环境变量易于检测
4. **回退** - 标准 Zsh 支持提供了未安装 Oh My Zsh 时的兼容性

**安装策略：**
```typescript
if (isOhMyZshInstalled()) {
  // 安装到 ~/.oh-my-zsh/custom/completions/_openspec
  // 由 Oh My Zsh 自动加载
} else {
  // 安装到 ~/.zsh/completions/_openspec
  // 必要时更新 ~/.zshrc 中的 fpath 和 compinit
}
```

## 缓存策略

动态补全将结果缓存 2 秒，以在新鲜度和性能之间取得平衡：

**为什么是 2 秒？**
- 典型的 Tab 补全会话持续时间 < 2 秒
- 防止在快速连续按 Tab 时重复扫描文件系统
- 足够短，在添加变更/spec 时感觉"实时"
- 每个进程自动过期（不会跨会话留下过期数据）

**实现：**
```typescript
private changeCache: { ids: string[]; timestamp: number } | null = null;
private readonly CACHE_TTL_MS = 2000;

if (this.changeCache && Date.now() - this.changeCache.timestamp < this.CACHE_TTL_MS) {
  return this.changeCache.ids; // 使用缓存
}
// 刷新缓存
```

## 错误处理理念

补全应优雅降级，而不是破坏工作流程：

1. **不支持的 shell** - 清晰错误，列出支持的 shell
2. **不在 OpenSpec 项目中** - 跳过动态补全，仅提供静态命令
3. **权限错误** - 建议替代安装方法
4. **缺少配置目录** - 自动创建并通知用户
5. **已安装** - 提供重新安装/更新选项
6. **未安装（卸载时）** - 优雅退出，给出信息性消息

## 测试策略

每个组件都可独立测试：

1. **单元测试**
   - 使用模拟的 `$SHELL` 环境变量进行 shell 检测
   - 生成器输出验证（正则表达式模式匹配）
   - 补全提供者缓存行为
   - 命令注册表结构验证

2. **集成测试**
   - 安装到临时测试目录
   - 配置文件修改
   - 端到端命令流程（生成 → 安装 → 验证）

3. **手动测试**
   - 真实的 shell 环境（Oh My Zsh、Bash、Fish、PowerShell）
   - OpenSpec 项目中的 Tab 补全行为
   - 动态变更/spec ID 建议
   - 安装/卸载工作流程

## TypeScript 语法糖模式

### 1. 不可变数据的 Const 断言
```typescript
const COMMAND_REGISTRY = [
  { name: 'init', ... },
  { name: 'list', ... }
] as const;
```

### 2. 命令类型的可辨识联合
```typescript
type Command =
  | { type: 'simple'; name: string }
  | { type: 'with-subcommands'; name: string; subcommands: Command[] };
```

### 3. 字符串的模板字面量类型
```typescript
type ShellConfigFile = `~/.${SupportedShell}rc` | `~/.${SupportedShell}_profile`;
```

### 4. 用于类型验证的 Satisfies 运算符
```typescript
const config = {
  shell: 'zsh',
  path: '~/.zshrc'
} satisfies ShellConfig;
```

### 5. 可选链和空值合并
```typescript
const path = process.env.ZSH ?? `${os.homedir()}/.oh-my-zsh`;
```

### 6. 使用 Promise.all 进行 Async/Await 并行操作
```typescript
const [changes, specs] = await Promise.all([
  provider.getChangeIds(),
  provider.getSpecIds()
]);
```

## 可扩展性考虑

### 添加新 Shell

1. 在 `SupportedShell` 联合类型中定义 shell
2. 创建实现 `CompletionGenerator` 的生成器类
3. 创建实现 `CompletionInstaller` 的安装器类
4. 在工厂函数中添加分支
5. 在 CLI 中添加命令注册
6. 编写测试

**TypeScript 将强制** 所有 switch 语句被更新（穷尽性检查）。

### 添加新命令

1. 将命令添加到 `COMMAND_REGISTRY`，附带适当的元数据
2. 所有生成器自动包含它
3. 更新测试以验证新命令出现

### 更改补全行为

动态补全逻辑集中在 `CompletionProvider` 中，使得在不触碰 shell 特定代码的情况下更改行为变得简单。

## 权衡与决策

### 决策：独立生成器与模板引擎

**选择：** 每个 shell 使用独立的生成器类

**替代方案：** 使用模板引擎配合 shell 特定模板

**理由：**
- Shell 补全语法本质上是不同的（不仅仅是文本替换）
- 类比模板提供更好的类型安全
- 逻辑复杂度（缓存、动态补全）不适合模板范式
- 专门的类更易于调试和测试

### 决策：2 秒缓存 TTL

**选择：** 2 秒缓存

**替代方案：** 无缓存（慢）、更长缓存（过期）、持久缓存（复杂）

**理由：**
- 平衡性能与新鲜度
- 匹配典型的用户交互模式
- 实现简单（无失效复杂度）
- 进程退出时自动清理

### 决策：Oh My Zsh 检测

**选择：** 优先检查 `$ZSH` 环境变量，然后检查 `~/.oh-my-zsh/` 目录

**理由：**
- `$ZSH` 由 Oh My Zsh 初始化设置（可靠）
- 目录检查是非交互式场景的回退
- 标准 Zsh 作为最终回退

### 决策：安装自动化与手动说明

**选择：** 自动化安装，带有 install/uninstall 命令

**替代方案：** 生成脚本并提供手动安装说明

**理由：**
- 更好的用户体验（一个命令 vs 多个手动步骤）
- 减少手动配置造成的错误
- 符合用户对现代 CLI 工具的期望
- 仍支持通过脚本生成到 stdout 的手动工作流程

## 未来增强

1. **上下文相关的标志补全** - 仅为当前命令建议有效的标志
2. **模糊匹配** - 允许变更/spec ID 的部分匹配
3. **丰富描述** - 在补全建议中包含"原因"部分（取决于 shell）
4. **补全统计** - 跟踪补全使用情况以进行分析
5. **自定义补全钩子** - 允许项目扩展补全
6. **MCP 集成** - 通过模型上下文协议提供补全

## 参考资料

- [Bash 可编程补全](https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion.html)
- [Zsh 补全系统](https://zsh.sourceforge.io/Doc/Release/Completion-System.html)
- [Fish 补全](https://fishshell.com/docs/current/completions.html)
- [PowerShell 参数补全器](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/register-argumentcompleter)
- [Oh My Zsh 自定义补全](https://github.com/ohmyzsh/ohmyzsh/wiki/Customization#adding-custom-completions)
