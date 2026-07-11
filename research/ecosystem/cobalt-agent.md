# cobalt-agent

**⭐ 3 | Plugin | 链接:** https://github.com/thestark77/cobalt-agent

---

## 它解决了什么问题？

Hermes 默认对子 Agent 使用相同模型，成本高速度慢。且没有工具守卫、技能注入、问题分类。cobalt-agent 用插件形式补齐这四项。

## 它是怎么解决的？

- 5 个独立机制：模型路由、工具守卫、技能注入、SDD 分类、超时控制
- **Hook-based Plugin** — 不修改 Hermes 核心，只通过 Hook 注入
- 单命令安装，一键部署
- 设计原则：非侵入、可回溯、模块化

## Hermes 能直接借鉴什么？

- **Plugin 可以做到的事远比想象多** — 路由、守卫、注入全通过 Hook 实现
- **"不修改核心"的设计哲学** — 作者没有觉得"我要重新设计 Hermes"
- **SDD 分类（先判断问题类型再行动）** — 跟你的 Router 设计方向一致

## 哪些不适合？

- 依赖 Enram Cloud 后端（闭源服务）
- ⭐3 说明还没被广泛验证
