"""activation policy: 什么情况下系统应该主动调 cold_memory_search"""

def should_activate(query, context):
    # 信号1：用户提到过去
    if any(kw in query for kw in ["之前", "上次", "以前", "昨天", "刚才",
                                   "你不是说", "我记得", "之前那个",
                                   "怎么回事", "什么来着"]):
        return True, "user referenced past state"

    # 信号2：涉及配置/状态
    if any(kw in query for kw in ["key", "token", "配置", "设置", "password",
                                   "账号", "密码", "凭证", "token",
                                   "remote", "repo", "仓库"]):
        return True, "config or state reference"

    # 信号3：用户怀疑/纠正
    if any(kw in query for kw in ["确定吗", "你确定", "不对", "不是",
                                   "错了", "你再想想", "查一下"]):
        return True, "user expressed doubt"

    # 信号4：用户问"为什么"
    if "为什么" in query or "why" in query.lower():
        return True, "causal question - may need history"

    # 默认：不触发
    return False, "no activation signal"
