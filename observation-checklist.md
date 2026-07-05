# Observation Week Checklist
# Start: 2026-07-02
# Goal: 用数据决定下一轮优化的优先级

---

## 1. Tool Parallelism

**观察什么：** 哪些工具可以在同一回合被并行调用

| 问题 | 记录位置 |
|------|---------|
| read_file 并行被调用过几次？ | 手工留意 |
| search_files 是否与 browser_snapshot 同时发生？ | 手工留意 |
| 有多少次本可以并行但串行了？ | session 日志 |
| 哪些工具组合经常同时出现？ | 手工记录 |

**信号：** 如果 read_file / search_files / browser_snapshot 频繁结伴，说明并行执行值得做。

---

## 2. Provider Stability

**观察什么：** 各 API 的真实稳定性数据

| 指标 | DeepSeek | Kimi | Xiaomi | 小Q |
|------|----------|------|--------|-----|
| 调用次数 | count | count | count | count |
| 超时次数 | count | count | count | count |
| 超时率 | % | % | % | % |
| 平均响应时间 | ms | ms | ms | ms |
| 错误率 | % | % | % | % |
| 空内容返回 | count | count | count | N/A |

**信号：** 如果有 Provider 超时率 > 30%，分层重试（换模型兜底）有明确依据。

---

## 3. Memory Schema 效果

**观察什么：** schema.yaml 定的规则在实际使用中表现

| 问题 | 记录 |
|------|------|
| Learned Event 三条（obs/why/apply_when）是否每次都填了？ | 自查 |
| Admission Rule 有效阻止了不必要的记忆吗？ | 回顾每次 memory call |
| Hot memory 容量还剩多少空间？ | memory tool 输出 |
| 有没有"想写但 admission 说不行"的情况？ | 手工记录 |

**信号：** 如果 Admission Rule 导致重要信息丢失，需要调整规则优先级。

---

## 4. Memory 噪声比

**观察什么：** 存进去的东西最终有多少被用到

| 指标 | 测量方式 |
|------|---------|
| 本周 memory add 总数 | memory tool 统计 |
| 本周 memory 被引用/搜索次数 | session 回顾 |
| 其中有用的条数 | 用户主观评判 |
| 噪声条目数（写了再没看过） | 差异计算 |

**信号：** 如果噪声比 > 50%，Admission Rule 需要收紧。

---

## 5. Route 命中率

**观察什么：** agents.yaml 里的路由表是否匹配实际使用模式

| 路由规则 | 命中次数 | 是否准确 |
|---------|---------|---------|
| deepseek (默认) | count | ✅/❌ |
| kimi (深度讨论) | count | ✅/❌ |
| xiaomi (超长文档) | count | ✅/❌ |
| 小Q (简单问答) | count | ✅/❌ |
| 用户点名 | count | ✅/❌ |

**信号：** 如果有规则基本没命中过，可以移除或合并。

---

## 6. Tool Metadata 使用情况

**观察什么：** isReadOnly / supportsParallel 标记是否符合实际

| 问题 | 记录 |
|------|------|
| 有没有工具被标记为 ReadOnly 但实际上改了状态？ | 报错记录 |
| 有没有工具实际可并行但没标记？ | session 观察 |
| supportsParallel 准确率 | 对比评估 |

**信号：** Accuracy < 80% → 修正标记 → 再观察。

---

## 7. Session 主要活动

| 日期 | 主要活动 | 意外/发现 |
|------|---------|----------|
| 07-02 | Memory Schema + Tool Metadata | 小Q离线 |
| ... | (持续记录) | |

---

## 8. 架构冲动（Architecture Impulses）

每天记录：

- **想法：**
- **为什么没有实现：**
- **是否影响今天正常使用：** 是 / 否

> 目标：记录事实，不设计未来；收集证据，不寻找证据。
> 如果影响正常使用 = 否 → 好点子但不是痛点
> 如果影响正常使用 = 是 → 值得在 Architecture Review 中讨论

---

## 9. 反证收集

Observation Week 不只是验证假设，也要主动收**反证**：

- Tool 并没有稳定共现 → H-004 不成立
- Provider 实际很稳定 → H-005 优先级下降
- 基本不用搜索 → H-001 不需要复杂化
- Memory 容量没再满过 → 压缩策略不需要进一步设计

> 一周后能否定一个原本很好的想法，也是一次成功的 Observation。

---

## Week End 决策矩阵

Observation Week 结束后，用以下标准做决策：

| 项目 | 触发条件 | 行动 |
|------|---------|------|
| 分层重试 | 任一提速器超时率 > 30% | 设计 3 层 retry：deepseek→kimi→小Q |
| 并行执行 | readOnly 工具经常结伴出现 | 加并行调度逻辑 |
| Schema 调整 | Admission Rule 导致重要信息丢失 | 放宽规则，加例外机制 |
| 路由优化 | 某路由规则命中率 < 10% | 移除或合并该规则 |
