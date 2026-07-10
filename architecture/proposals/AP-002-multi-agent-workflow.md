# AP-002: Multi-Agent Workflow

> **状态:** Proposal · **日期:** 2026-07-09
> **作者:** 吉冠佳
> **关联:** AP-001 (Capability-Driven Architecture), Router (agents.yaml)

---

## 1. 为什么需要 Workflow

当一个任务天然包含多个相互独立或需要交叉验证的步骤时，应允许主 Agent 将任务拆分为多个角色协作完成，而不是依赖单次推理。

典型场景：

- **复杂分析** — 同一问题需要 Support/Opposition 双视角交叉验证
- **学习出题** — 出题 → 审核 → 格式化，三个步骤各自由不同角色完成
- **架构评审** — 提案分析 → 风险评估 → 总结，每个环节独立验证

当前 Hermes 的 `delegate_task` 已经提供了子 Agent 能力，但缺少统一的角色定义和协作流程。AP-002 填补这一层。

---

## 2. Workflow 抽象模型

定义四个角色，每个角色只描述**职责**，不绑定具体模型：

| 角色 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **Planner** | 任务拆解、步骤规划 | 用户意图 | 执行计划 |
| **Executor** | 按计划执行具体动作 | 子任务 + 工具集 | 原始结果 |
| **Reviewer** | 质量校验、一致性检查 | 原始结果 | 通过/拒绝 + 反馈 |
| **Aggregator** | 汇总、冲突消解、最终输出 | 所有通过的结果 | 最终响应 |

执行流程：

```
Task
  │
  ▼
Planner ──→ 任务拆解
  │
  ├── Executor A → 结果 A
  ├── Executor B → 结果 B
  └── Executor C → 结果 C
  │
  ▼
Reviewer ──→ 逐项审查
  │
  ▼
Aggregator ──→ 汇总输出
```

**不包含：**
- ❌ 具体模型推荐（Planner 用谁、Executor 用谁）
- ❌ Provider 绑定
- ❌ Prompt 或实现细节

---

## 3. 与现有架构的关系

```
Workflow (AP-002)
    │   定义"角色如何协作"
    ▼
Capability (AP-001)
    │   定义"每个角色能做什么"
    ▼
Router (agents.yaml)
    │   定义"谁来做"
    ▼
Provider
```

**边界原则：**

> **Workflow 负责协作顺序，Capability 负责能力抽象，Router 负责 Provider 选择。**

- Workflow 不知道 Executor 用的是 DeepSeek 还是小Q
- Capability 不知道 Executor 是 Planner 还是 Reviewer
- Router 不知道 Workflow 的存在

---

## 4. 与现有能力的对照

| 角色 | 当前可用的实现者 | 说明 |
|------|----------------|------|
| Planner | DeepSeek | 需要强推理能力 |
| Executor | 小Q (DeepSeek R1 本地) | 简单任务，免费 |
| Reviewer | Kimi / DeepSeek | 需要批判性视角 |
| Aggregator | DeepSeek | 需要整合多源信息 |

> 注：上表为当前环境的推荐配置，不属于 AP-002 正文。具体 Provider 分配应放在 `deployment/` 或 Profile 配置中。

---

## 5. 后续步骤

| 阶段 | 动作 |
|------|------|
| Obs Week | 记录"是否经常需要拆分子任务" |
| Architecture Review | 评估数据 → 决定是否升级为 Hypothesis |
| 如果通过 | 定义 Workflow DSL（描述如何编排角色） |
| 如果未通过 | 继续以 Proposal 状态保留 |
