# hermes-skill-factory

**⭐ 405 | Plugin | 链接:** https://github.com/Romanescu11/hermes-skill-factory

---

## 它解决了什么问题？

每次用 Hermes 解决完一个问题，那个工作流就消失了。下次得重新解释一遍。Skill Factory 自动检测重复模式，询问用户是否保存为 Skill。

## 它是怎么解决的？

- **元 Skill** — 一个 Skill 不做事，而是观察用户做事
- 检测重复模式 → 询问用户 → 自动生成 SKILL.md + plugin.py
- 支持 `/skill-factory propose` 等斜杠命令
- 本质是 **Programming by Demonstration（示教编程）**

## Hermes 能直接借鉴什么？

- **从行为生成抽象** — 不是先设计 Workflow，而是从操作中提炼 Workflow
- **Proposal 可以来自行为日志** — 如果 Hermes 记录行为，自动发现重复模式，Proposal 就不是拍脑袋来的
- **Meta-Skill 模式** — Skill 可以操作 Skill，这层抽象值得学

## 哪些不适合？

- 对于简单任务（查单词、写代码）不太需要
- 生成质量取决于检测精度，误报会烦人
