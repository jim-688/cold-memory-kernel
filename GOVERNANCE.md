# Hermes Architecture Governance

> 生效日期: 2026-07-03
> 状态: frozen（Observation Week 期间禁止修改）
> 退出条件: 见下方 §5

---

## §1 治理对象

Architecture 治理涉及三类对象，每条记录独立文件存储：

| 类型 | 存储位置 | 是否需要验证 | 是否指导实现 |
|------|---------|------------|------------|
| **Constraint** | `architecture/constraints/` | ❌ 否，强制执行 | ✅ 是 |
| **Hypothesis** | `architecture/hypotheses/` | ✅ 需要 Observation 验证 | ⏳ 验证通过后 |
| **Backlog** | `architecture/backlog/` | ❌ 暂时不需要 | ❌ 否 |

---

## §2 状态流转

```
Idea
  │
  ▼
Backlog
  │ 满足升级条件 ↓
  ▼
Hypothesis Review
  │
  ├── 通过 → Hypothesis (provisional)
  │            │
  │            ▼ Observation Week
  │       ┌────┴────┐
  │   validated  invalidated
  │
  └── 不通过 → 退回 Backlog（须记录理由 + 重审触发条件）
```

### 允许的状态

- **Backlog**: `pending` — 暂存，未进入验证
- **Hypothesis**: `provisional` → `observational` → `validated` / `invalidated`
- **Constraint**: `active` — 不可变更，不可绕过

---

## §3 升级条件（Backlog → Hypothesis Review）

Backlog 条目满足以下全部条件时，自动进入 Hypothesis Review：

1. **可验证的假设陈述**（Hypothesis Statement）
2. **最小验证方案**（Minimum Validation Plan）— 在现有资源约束内可执行
3. **验证标准**（Verification Criteria）— 明确定义成功/失败

提交方满足上述条件后，评审方**不得无理由搁置**。

---

## §4 评审规则

1. 评审必须给出明确结论（通过/退回）
2. 退回必须记录 **书面理由**
3. 退回必须给出 **重审触发条件**（什么情况下重新评审）
4. 评审不预设通过率，不设通过名额上限

---

## §5 Feature Freeze

### 冻结范围（禁止）

- 新增架构层
- 新增 Runtime 行为
- 新增 Router 决策逻辑
- 新增 Memory Schema 字段
- 新增 Tool 生命周期

### 允许

- Bug 修复
- 文档完善
- 日志补充
- Metrics 采集
- Observation Checklist 调整（不改变运行逻辑）

### 退出条件

Feature Freeze 在以下任一条件满足时结束：

1. Observation Week 达到预定观察周期
2. Observation Checklist 核心指标收集完成
3. 出现阻断性问题，经评审允许提前结束

---

## §6 设计原则（非强制约束）

- 能直接回答，就不要调用工具
- 能调用一个工具，就不要调用三个
- 能保持简单，就不要增加新层
- 真实数据优先于猜测
- 新规则必须解决真实出现的问题
