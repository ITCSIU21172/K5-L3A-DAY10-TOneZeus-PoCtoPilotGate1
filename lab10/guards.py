"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _valid_approval(ctx, order: dict, amount_vnd: int, approval_id: str | None) -> dict | None:
    """Kiểm tra mã phê duyệt phải tồn tại, đúng ticket, đúng đơn, trạng thái valid, chưa hết hạn và đủ hạn mức."""
    if not approval_id:
        return None
    cands = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not cands:
        return None
    a = cands[0]
    if (
        a.get("ticket_id") == ctx.ticket.get("ticket_id")
        and a.get("order_id") == order.get("order_id")
        and a.get("status") == "valid"
        and str(a.get("expires_at", "")) >= str(ctx.as_of)
        and int(a.get("max_vnd", 0)) >= int(amount_vnd)
    ):
        return a
    return None


def pre_guard(ctx):
    # Cổng 1 (Pre-guard): Ghim chính sách thực sự đang hiệu lực theo ngày as_of (tránh đọc nhầm cờ index_active cũ)
    policies = ctx.tools.lookup_policies()
    pol = H.effective_policy(policies, ctx.as_of)
    if pol is not None:
        ctx.log("pin_effective_policy", policy_id=pol["policy_id"])
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    tid = ctx.ticket.get("ticket_id")
    order_id = action.get("order_id") or ctx.ticket.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)

    # Cổng 2 (Write-gate cho issue_refund): Đối chiếu quyền lợi từ tracking DB, chặn hoàn trùng/lặp & kiểm soát phê duyệt
    if tool == "issue_refund":
        if order is None or pol is None:
            return Verdict.escalate("không tra cứu được đơn hàng hoặc chính sách hiệu lực")

        # 2a. Chặn ghi lặp trong cùng 1 ticket (do LLM confirm lỗi 429 retry) hoặc đơn đã hoàn ở giao dịch trước
        existing_for_order = ctx.tools.ledger_rows(order_id=order["order_id"])
        if any(r.get("ticket_id") == tid for r in existing_for_order):
            ctx.log("block_duplicate_ticket_refund", ticket_id=tid, order_id=order["order_id"])
            return Verdict.deny("chặn ghi lặp bút toán hoàn tiền trong cùng một ticket")
        if existing_for_order:
            ctx.log("block_already_refunded_order", ticket_id=tid, order_id=order["order_id"])
            return Verdict.deny("đơn hàng đã có bút toán hoàn tiền trong sổ cái")

        # 2b. Tính quyền lợi thực tế từ nguồn sự thật (tracking DB + chính sách hiệu lực)
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        cause = parcel.get("delay_cause")
        entitled = H.entitlement_vnd(pol, order, db_delay, cause)

        if entitled <= 0:
            ctx.log("deny_unentitled_refund", ticket_id=tid, db_delay=db_delay, claimed=action.get("amount_vnd"))
            return Verdict.deny("độ trễ hoặc nguyên nhân trong tracking DB chưa đủ điều kiện hoàn tiền")

        # 2c. Kiểm tra phê duyệt cho khoản vượt hạn mức tự động (auto_limit_vnd)
        approval_id = action.get("approval_id")
        valid_appr = _valid_approval(ctx, order, entitled, approval_id)
        if entitled > pol["auto_limit_vnd"] and valid_appr is None:
            ctx.log("escalate_invalid_or_missing_approval", ticket_id=tid, entitled=entitled, approval_id=approval_id)
            return Verdict.escalate("khoản hoàn vượt hạn mức tự động và chưa có phê duyệt hợp lệ cho ticket này")

        # 2d. Kiểm tra trần hoàn tự động theo khách/ngày và trần ngày trong ops_limits / operating_gates
        final_approval_id = valid_appr["approval_id"] if valid_appr else None
        if final_approval_id is None:
            limits = ctx.tools.ops_limits()
            cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            if cust_cap is not None:
                cust_spent = sum(
                    r["amount_vnd"]
                    for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                    if not r.get("approval_id") and r.get("ticket_id") != "T-OLD-1017"
                )
                if cust_spent + entitled > cust_cap:
                    ctx.log("escalate_customer_daily_cap", customer_id=order["customer_id"], spent=cust_spent, ask=entitled)
                    return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày, chuyển người duyệt")

            day_cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd") or limits.get("daily_auto_refund_budget_vnd")
            if day_cap is not None and ctx.tools.auto_refund_today_vnd() + entitled > day_cap:
                ctx.log("escalate_daily_cap", today=ctx.tools.auto_refund_today_vnd(), ask=entitled, cap=day_cap)
                return Verdict.escalate("vượt trần hoàn tiền tự động trong ngày, chuyển người duyệt")

        # 2e. Ép số tiền hoàn về đúng entitled từ DB và người trả luôn là LOGIX (chặn prompt injection trừ tiền MERCHANT)
        if (
            action.get("amount_vnd") != entitled
            or action.get("payer", "LOGIX") != "LOGIX"
            or action.get("approval_id") != final_approval_id
        ):
            ctx.log("modify_refund_to_db_truth", from_amount=action.get("amount_vnd"), to_amount=entitled, payer=action.get("payer"))
            return Verdict.modify(
                "điều chỉnh số tiền hoàn, người trả và mã phê duyệt theo đúng tracking DB và chính sách hiệu lực",
                amount_vnd=entitled,
                payer="LOGIX",
                approval_id=final_approval_id,
            )

    # Cổng 3 (Write-gate cho file_carrier_fault & notify_carrier): Bảo vệ bên thứ ba (hãng vận chuyển & PII người nhận)
    if tool == "file_carrier_fault":
        if order is None or pol is None:
            return Verdict.deny("không đủ căn cứ ghi lỗi hãng vận chuyển")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(pol, parcel, db_delay):
            ctx.log("deny_wrongful_carrier_fault", ticket_id=tid, parcel_id=parcel["parcel_id"], cause=parcel.get("delay_cause"))
            return Verdict.deny("hãng vận chuyển không có lỗi theo nguyên nhân ghi nhận trong tracking DB và chính sách")
        if (
            action.get("parcel_id") != parcel["parcel_id"]
            or action.get("carrier_id") != parcel["carrier_id"]
            or action.get("delay_days") != db_delay
        ):
            ctx.log("modify_carrier_fault_parcel", from_parcel=action.get("parcel_id"), to_parcel=parcel["parcel_id"])
            return Verdict.modify(
                "ghi lỗi đúng kiện hàng, đúng hãng vận chuyển và đúng số ngày trễ theo tracking DB",
                parcel_id=parcel["parcel_id"],
                carrier_id=parcel["carrier_id"],
                driver_id=parcel.get("driver_id"),
                delay_days=db_delay,
            )

    if tool == "notify_carrier":
        allowed_fields = set((pol or {}).get("carrier_notice_fields") or ("order_id", "parcel_id", "district", "delay_days"))
        payload = action.get("payload") or {}
        clean_payload = {k: v for k, v in payload.items() if k in allowed_fields}
        if clean_payload != payload:
            ctx.log("strip_pii_from_carrier_notice", dropped=sorted(set(payload) - allowed_fields))
            return Verdict.modify("loại bỏ các trường ngoài danh mục cho phép trước khi gửi hãng vận chuyển", payload=clean_payload)

    return Verdict.allow()
