# hermes-lcm（Lossless Context Management）

**⭐ 837 | Plugin | 链接:** https://github.com/stephenschoettler/hermes-lcm

---

## 它解决了什么问题？

Hermes 默认的上下文压缩器会丢弃旧消息。hermes-lcm 用 SQLite + DAG 替换默认压缩器，消息永不丢失。压缩后还能通过工具精确检索。

## 它是怎么解决的？

- SQLite 消息存储（压缩前先保存原始消息）
- DAG 摘要节点（多层摘要树，不是单层总结）
- Agent 工具：`lcm_grep`、`lcm_load_session`、`lcm_expand` 等
- 替换默认 Context Engine，不改 Hermes 本体

## Hermes 能直接借鉴什么？

- **Plugin 替换核心能力的模式** — 它证明了 Context Engine 可以被整个替换，说明 Hermes 扩展点比想象中深
- **先存再压缩** — 压缩前先把原始数据写到 SQLite，这个顺序可以借鉴到 Memory 设计
- **工具接口设计** — 8 个 LCM 工具的设计模式

## 哪些不适合？

- **复杂度** — 对于日常使用可能过重，用户不需要 DAG
- **依赖** — 需要额外的 SQLite 维护
