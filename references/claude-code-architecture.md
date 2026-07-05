# Claude Code Architecture — 学习笔记

来源: [how-claude-code-works](https://github.com/Windy3f3f3f3f/how-claude-code-works) (2.9k⭐)
日期: 2026-07-02
说明: Claude Code 源码深度解析 15 篇，以下是与 Hermes 架构相关的提炼

---

## 1. 系统主循环 (02-agent-loop.md)

**关键设计:**
- 双层生成器架构 (outer/inner generator)
- QueryEngine 管理会话生命周期
- **7 个继续点 (Continue Sites)** — 7 种不同的故障恢复策略
- 错误扣留 (Withholding) — 能恢复的错误用户看不到
- Token 上限自动升级: 4K→64K 自动重试

**Hermes 差距:** 当前只有 1 次 retry，没有分层恢复策略

---

## 2. 上下文工程 (03-context-engineering.md)

**5 级渐进式压缩流水线:**
1. Tool Result 预算裁剪 — 截断旧的工具输出
2. History Snip — 去除历史中的大块内容
3. Microcompact — 精细节压缩
4. Context Collapse — 聚类压缩
5. Autocompact — 子 Agent 摘要

**前缀缓存策略:** 系统提示词必须字节级一致才能命中缓存
- 动态内容通过 `<system-reminder>` 注入（不破坏缓存）
- 工具 schema 最后一个工具标记 cache_control 作为断点
- CLAUDE.md 放在 messages[0] 而非 system prompt 中

**Hermes 差距:** 没有压缩流水线，Hot Memory 满了直接归档到 Cold

---

## 3. 工具系统 (04-tool-system.md)

**统一 Tool 接口:**
```typescript
Tool<Input, Output, Progress> {
  name, aliases, maxResultSizeChars
  call(), description(), prompt()
  inputSchema (Zod), inputJSONSchema
  isConcurrencySafe(), isReadOnly(), isDestructive()
  validateInput(), checkPermissions()
  renderToolUseMessage(), renderToolResultMessage()
}
```

**关键设计:**
- isReadOnly=true → 自动并行执行
- isDestructive=true → 自动串行 + 权限检查
- 结果 >100K 字符 → 自动落盘，模型只拿摘要+文件路径
- 66 个工具共用同一套接口

**Hermes 差距:** 工具没有统一接口，只读/写标记缺失

---

## 4. 代码编辑策略 (05-code-editing-strategy.md)

**两种编辑工具:**
| 工具 | 策略 | 适用场景 | 破坏性 |
|------|------|---------|--------|
| FileEditTool | search-and-replace | 修改已有文件 | 低 |
| FileWriteTool | 全文件覆盖 | 新建或重写 | 高 |

**Search-and-Replace 优势:**
- 低破坏性（只改目标部分）
- 可验证（明确的 before/after）
- 抗幻觉（不存在的字符串直接报错）
- Token 效率（只需发送修改点附近上下文）
- 位置无关（不怕行号偏移）

**Hermes 差距:** 你的 patch 工具类似 search-and-replace，方向一致

---

## 5. Hooks 系统 (06-hooks-extensibility.md)

**27 种事件钩子，覆盖完整生命周期:**

| 类别 | 事件 | 触发时机 |
|------|------|---------|
| 工具生命周期 | PreToolUse, PostToolUse, PostToolUseFailure | 工具执行前后 |
| 权限 | PermissionRequest, PermissionDenied | 权限判定时 |
| 会话 | SessionStart, SessionEnd, UserPromptSubmit | 会话生命周期 |
| 模型响应 | Stop, StopFailure | 模型决定停止时 |
| Agent协调 | SubagentStart, SubagentStop, TeammateIdle | 多 Agent 协作 |
| 任务 | TaskCreated, TaskCompleted | 任务生命周期 |
| 压缩 | PreCompact, PostCompact | 上下文压缩前后 |

**4 种可配置 Hook + 2 种编程式 Hook**
**Matcher 三级匹配机制:** 事件类型 → 工具/类型匹配 → if 条件

**Hermes 差距:** 只有 activation gate，没有完整生命周期钩子

---

## 6. 多 Agent 架构 (07-multi-agent.md)

**三种模式:**
| 模式 | 适用场景 | 通信方式 |
|------|---------|---------|
| 子 Agent (AgentTool) | 单个独立子任务 | fork-return |
| 协调器 (Coordinator) | 复杂多步任务 | 派生+综合 |
| Swarm 团队 | 并行协作 | 命名信箱通信 |

**关键设计:**
- 子 Agent prompt 必须自包含（不继承父对话历史）
- Explore Agent 用 Haiku（速度快），内部用户继承父级模型
- 34M+ 次 Explore 调用/周，省略 CLAUDE.md 节省 5-15 Gtok/周

**Hermes:** 你已经在用协调器模式（DeepSeek主脑），方向一致

---

## 7. 记忆系统 (08-memory-system.md)

**四种封闭类型:**
| 类型 | 记什么 | 示例 |
|------|--------|------|
| user | 用户身份、偏好 | "数据科学家，专注可观测性" |
| feedback | 行为纠正 + 肯定 | "不要末尾总结，用户能看 diff" |
| project | 项目进展、决策 | "2026-03-05 合并冻结" |
| reference | 外部系统位置 | "管道 Bug 追踪在 Linear INGEST" |

**原则: 只记不可从当前项目状态推导的信息**
不记: 代码模式、Git 历史、CLAUDE.md 已有内容、临时任务细节

**feedback 必须含 Why + How to apply**
**相对日期必须转绝对日期**
**MEMORY.md 是索引不是容器**

**Hermes:** 你的 cold memory 缺少 feedback 类型 + Why/Apply When 结构

---

## 8. 技能系统 (09-skills-system.md)

**双重调用:** 用户手动 (`/commit`) + 模型自动（意图识别）
**技能格式:** 目录含 SKILL.md（frontmatter + prompt）+ 可选资源文件
**6 个来源:** 内置 → 可选 → 用户 → 项目 → MCP → 依赖

**关键设计:**
- SKILL.md 的 description 是召回核心依据（必须精确）
- 技能可以带参数（`$ARGUMENTS` 占位符）
- Inline vs Fork 两种执行模式

**Hermes:** 你的 68 个 skills 只有手动触发，没有模型自动调用

---

## 9. Plan 模式 (10-plan-mode.md)

**核心理念:** 复杂任务先降权（只读）→ 探索 + 规划 → 审批 → 恢复权限执行

**流程:**
1. 调用 EnterPlanMode → 模式切换为 plan
2. 系统注入 plan_mode 附件（5 阶段工作流）
3. Explore Agent 探索代码 → Plan Agent 设计方案
4. 写入计划文件 → 调用 ExitPlanMode
5. 用户审批（可编辑计划）→ 恢复原模式
6. 开始实施

**Hermes 差距:** 没有对应机制，架构修改直接执行

---

## 10. 权限安全 (11-permission-security.md)

**7 层纵深防御:**
1. 工作区信任确认
2. 权限模式（5 种）
3. 权限规则匹配（allow/deny/ask）
4. Bash AST 解析 + 23 项静态检查
5. 工具级安全（validateInput + checkPermissions）
6. 沙箱与隔离（Sandbox + Git Worktree）
7. 用户确认（ML 分类器竞速 + 200ms 防误触）

**Hermes 差距:** 只有 tools_allowed 白名单，相当于 Layer 5 的一小部分

---

## 11. 用户体验 (12-user-experience.md)

**设计哲学:** 可观察的自主性 (Observable Autonomy)
- 工具调用流式展示（用户能在前 3 秒 Ctrl+C）
- 权限弹窗 200ms 防误触
- 流式输出 + 增量 Markdown 渲染
- 自研 Ink/React 终端渲染器（251KB）

**Hermes:** 终端是桌面端自带功能，暂无对应设计需求

---

## 12. 最小必要组件 (13-minimal-components.md)

**7 个组件即可构建一个可用的 Coding Agent:**
1. Prompt Orchestration（提示词编排）
2. Tool Registry（工具注册表）
3. Agent Loop（代理循环）
4. File Operations（文件操作）
5. Shell Execution（Shell 执行）
6. Edit Strategy（编辑策略）
7. CLI UX（命令行交互）

**配套项目:** [claude-code-from-scratch](https://github.com/Windy3f3f3f3f/claude-code-from-scratch)
~3000 行 TypeScript/Python 实现完整 coding agent

**Hermes:** 你的四层架构 + agents.yaml + project_state 已经覆盖了大部分

---

## 13. 任务系统 (15-task-system.md)

**TodoV2 架构:** 每个任务一个独立文件（支持多 Agent 并发）
**四个核心工具:** TaskCreate, TaskGet, TaskList, TaskUpdate
**状态机:** pending → in_progress → completed
**依赖追踪:** blocks / blockedBy 双向更新

**Hermes:** 你的 project_state 跟这个思路一致，但粒度更粗

---

## Hermes 改进优先级（基于 Claude Code 源码分析）

| 优先级 | 项目 | 参考章节 |
|--------|------|---------|
| P0 | Learning Event 结构 (Observation/Why/Apply When/Avoid When) | 08-memory-system |
| P0 | "只记不可推导的信息"元原则 | 08-memory-system |
| P1 | 渐进式压缩流水线（摘要→语义去重→再摘要） | 03-context-engineering |
| P1 | 工具统一接口 + 只读/写标记 | 04-tool-system |
| P1 | 分层恢复策略（代替当前 1 次 retry） | 02-agent-loop |
| P2 | Hooks 系统扩展 | 06-hooks-extensibility |
| P2 | Plan 模式（架构修改前先规划） | 10-plan-mode |
| P3 | 纵深权限安全 | 11-permission-security |
