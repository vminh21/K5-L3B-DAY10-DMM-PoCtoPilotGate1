"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

─────────────────────────────────────────────────────────────────────────────────────────────────────────────
CỔNG VÒNG 1 CỦA BÀN (mọi kiểm tra dựa trên NGUỒN SỰ THẬT: tracking DB, chính sách theo ngày hiệu lực, sổ cái,
bảng phê duyệt. Không rẽ nhánh theo mã ticket hay câu chữ của khách.)

  G0  pre_guard        Ghim chính sách theo NGÀY HIỆU LỰC (không tin cờ index_active).          [drift v3 → v4]
  G1  issue_refund     Đối chiếu số tiền với mức được hưởng tính từ tracking DB; người trả phải là LOGIX;
                       chặn hoàn trùng (đơn đã có dòng sổ cái); phê duyệt phải còn hiệu lực và đúng đơn.
                       [model tin số ngày khách ghi (T-002@55), lệnh nhúng trong ticket/ghi chú, fail-open, ghi lặp]
  G2  file_carrier_fault / notify_carrier
                       Chỉ ghi lỗi hãng khi tracking có nguyên nhân thuộc fault_causes, và ghi đúng kiện trễ;
                       thông báo cho hãng chỉ giữ các trường chính sách cho phép (carrier_notice_fields).
                       [ghi lỗi oan cho hãng, lộ dữ liệu cá nhân người nhận cho bên thứ ba]
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


# ───────────────────────────── tra cứu dùng chung (chỉ đọc nguồn sự thật) ─────────────────────────────

def _policy(ctx):
    """Chính sách đang hiệu lực theo ngày hôm nay (không theo cờ index_active)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(order, parcel, db_delay, policy) cho ticket hiện tại; None nếu thiếu dữ liệu."""
    order = ctx.tools.lookup_order(order_id)
    pol = _policy(ctx)
    if order is None or pol is None or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), pol


def _approval_ok(ctx, approval_id, order_id, amount):
    """Phê duyệt phải: tồn tại, status valid, chưa hết hạn, đúng đơn, hạn mức đủ cho số tiền."""
    rows = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not rows:
        return False
    a = rows[0]
    return (a.get("status") == "valid"
            and (not a.get("expires_at") or a["expires_at"] >= ctx.as_of)
            and a.get("order_id") == order_id
            and int(a.get("max_vnd") or 0) >= int(amount))


# ───────────────────────────────────────────── G0 ─────────────────────────────────────────────

def pre_guard(ctx):
    pol = _policy(ctx)
    if pol is not None:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


# ───────────────────────────────────────────── G1 ─────────────────────────────────────────────

def _gate_refund(ctx, action):
    order_id = action.get("order_id")
    amount = int(action.get("amount_vnd") or 0)
    f = _facts(ctx, order_id)
    if f is None:
        return Verdict.escalate("G1: không đủ dữ liệu nguồn sự thật để đối chiếu, chuyển người")
    order, parcel, delay, pol = f

    # (a) hoàn trùng: sổ cái đã có khoản hoàn cho đơn này (cờ refund_status chỉ cập nhật theo batch đêm,
    #     hoặc agent ghi lại lần 2 khi không chắc lần 1 đã ghi)
    prior = ctx.tools.ledger_rows(order_id=order_id)
    if prior:
        ctx.log("guard_refund_duplicate", order_id=order_id, prior_vnd=sum(r["amount_vnd"] for r in prior))
        return Verdict.deny("G1: đơn đã có khoản hoàn trong sổ cái, không hoàn lần nữa")

    # (b) mức được hưởng tính từ tracking DB + chính sách theo ngày hiệu lực
    ent = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    if ent <= 0:
        ctx.log("guard_refund_fix", asked=amount, entitled=0, db_delay_days=delay)
        return Verdict.deny("G1: theo tracking DB đơn chưa đủ điều kiện hoàn")

    # (c) phê duyệt (nếu agent gắn) phải hợp lệ
    approval_id = action.get("approval_id")
    if approval_id and not _approval_ok(ctx, approval_id, order_id, min(amount, ent)):
        ctx.log("guard_bad_approval", approval_id=approval_id)
        return Verdict.escalate("G1: phê duyệt không hợp lệ (hết hạn / đã dùng / khác đơn / thiếu hạn mức)")

    # (d) số tiền hoặc người trả lệch so với nguồn sự thật
    if amount != ent or action.get("payer", "LOGIX") != "LOGIX":
        changes = {"amount_vnd": ent, "payer": "LOGIX"}
        if ent > pol["auto_limit_vnd"] and not (approval_id and _approval_ok(ctx, approval_id, order_id, ent)):
            # tìm phê duyệt hợp lệ của ĐÚNG đơn này (không lấy theo khách)
            valid = [a for a in ctx.tools.lookup_approvals(order_id=order_id)
                     if _approval_ok(ctx, a["approval_id"], order_id, ent)]
            if not valid:
                ctx.log("guard_refund_fix", asked=amount, entitled=ent, db_delay_days=delay, escalated=True)
                return Verdict.escalate("G1: mức được hưởng vượt hạn mức tự động, cần phê duyệt")
            changes["approval_id"] = valid[0]["approval_id"]
        ctx.log("guard_refund_fix", asked=amount, entitled=ent, db_delay_days=delay,
                payer=action.get("payer"))
        return Verdict.modify("G1: đưa số tiền về mức tính từ tracking DB, người trả LOGIX", **changes)
    return Verdict.allow()


# ───────────────────────────────────────────── G2 ─────────────────────────────────────────────

def _gate_fault(ctx, action):
    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.deny("G2: không đủ dữ liệu để ghi lỗi hãng")
    order, parcel, delay, pol = f
    if not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("guard_fault_blocked", parcel_id=parcel["parcel_id"], cause=parcel.get("delay_cause"),
                db_delay_days=delay)
        return Verdict.deny("G2: tracking không ghi nguyên nhân thuộc lỗi hãng, không ghi lỗi")
    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    if any(action.get(k) != v for k, v in want.items()):
        ctx.log("guard_fault_fix", asked={k: action.get(k) for k in want}, fixed=want)
        return Verdict.modify("G2: ghi lỗi đúng kiện trễ và số ngày theo tracking DB", **want)
    return Verdict.allow()


def _gate_notify(ctx, action):
    pol = _policy(ctx)
    allowed = set((pol or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "delay_days"])
    payload = action.get("payload") or {}
    extra = sorted(set(payload) - allowed)
    if extra:
        ctx.log("guard_payload_trim", dropped=extra)
        return Verdict.modify("G2: chỉ gửi hãng các trường chính sách cho phép",
                              payload={k: v for k, v in payload.items() if k in allowed})
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()
