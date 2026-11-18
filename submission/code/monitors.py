"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def guard_intervention_rate(trials):
    """Tỉ lệ lần chạy mà cổng bảo vệ (write_gate / business_gate / legal_gate) phải can thiệp chặn, sửa hoặc chuyển người."""
    if not trials:
        return 0.0
    hits = sum(
        any(e.get("type") in ("gate", "business_gate", "legal_gate") for e in t.get("events", []))
        for t in trials
    )
    return hits / len(trials)


def anomalous_agent_event_rate(trials):
    """Tỉ lệ lần chạy xuất hiện hành vi bất thường của model/LLM (model_override, directive_obeyed, llm_error, llm_fallback, write_retry)."""
    if not trials:
        return 0.0
    bad_types = {"model_override", "directive_obeyed", "llm_error", "llm_fallback", "write_retry"}
    hits = sum(
        any(e.get("type") in bad_types for e in t.get("events", []))
        for t in trials
    )
    return hits / len(trials)


def max_queue_wait_minutes(trials):
    """Thời gian chờ người duyệt lâu nhất (phút) trong ca để phát hiện sớm nguy cơ ùn tắc hàng chờ giờ cao điểm."""
    if not trials:
        return 0.0
    return max((float(t.get("queue_wait_min") or 0.0) for t in trials), default=0.0)


MONITORS = {
    "escalation_rate": escalation_rate,                     # có sẵn; KHÔNG tính là metric mới của đội
    "guard_intervention_rate": guard_intervention_rate,     # metric mới 1: tỉ lệ can thiệp của cổng bảo vệ
    "anomalous_agent_event_rate": anomalous_agent_event_rate,  # metric mới 2: tỉ lệ sự kiện bất thường của agent/LLM
    "max_queue_wait_minutes": max_queue_wait_minutes,       # metric mới 3: thời gian chờ duyệt tối đa (phút)
}
STARTER_MONITORS = ("escalation_rate",)
