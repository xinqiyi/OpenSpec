## 原因

spec 应用目前与 archive 捆绑在一起 - 用户必须运行 `openspec archive` 才能将 delta spec 应用到主 spec。这耦合了两个不同的关注点（应用 spec vs archive 变更），并迫使用户等到"完成"后才能看到主 spec 更新。用户希望在 workflow 中更灵活地提前同步 spec，特别是在迭代期间。

## 变更内容

- 添加 `/opsx:sync` skill，将 delta spec 同步到主 spec 作为独立操作
- 该操作是幂等的 - 多次运行安全，Agent 合并主 spec 以匹配 delta
- archive 继续像今天一样工作（如果尚未合并则应用 spec，然后移动到 archive）
- 无新的状态跟踪 - Agent 读取 delta 和主 spec，每次运行时合并
- Agent 驱动的方法允许智能合并（部分更新、添加场景）

**workflow 变为：**
```
/opsx:new → /opsx:continue → /opsx:apply → archive
 │
 └── /opsx:sync（可选，随时）
```

## 能力

### 新增能力
- `specs-sync-skill`：`/opsx:sync` 命令的 skill template，将主 spec 与 delta spec 合并

### 修改的能力
- 无（Agent 驱动，无需 CLI 命令）

## 影响范围

- **skill**：`skill-templates.ts` 中的新 `openspec-sync-specs` skill
- **archive**：无需更改 - 已进行合并，将继续工作
- **Agent workflow**：用户获得在 archive 前同步 spec 的灵活性
