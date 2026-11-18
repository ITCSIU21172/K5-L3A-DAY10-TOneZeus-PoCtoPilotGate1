# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `TOneZeus`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-TOneZeus-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S8`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Hồ Anh Dũng | 2A202603613 | Kỹ sư cổng | x |
|   2 | Ngô Huy Hoàng | 2A202603622 | Sản phẩm và kinh doanh | |
|   3 | Nguyễn Văn Nhi | 2A202603697 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên:
`["HoAnhDung-2A202603613", "NgoHuyHoang-2A202603622", "NguyenVanNhi-2A202603697"]`.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoAnhDung-2A202603613

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng (Trưởng nhóm).
- **Câu của đề & mục phiếu:** Câu 1.3 (Phiếu A mục A2 - Offline metric), Câu 2.1–2.2 (Phiếu B mục B0, B1, B2 - chạy baseline và dò trace `T-002@55`), Câu 2.6–2.8 (Phiếu B mục B7.1–B7.3 - viết cổng phòng ngừa Vòng 1, hai bước tránh rò rỉ dữ liệu, behavioral test), Câu 3.1, 3.5, 3.6 (Phiếu C mục C2, C7, C8 - dò trace sự cố, sửa cổng Vòng 2, thêm chỉ số theo dõi).
- **File phụ trách:** `lab10/guards.py`, `lab10/monitors.py`, quản lý Git/checkpoint và chạy các lệnh đánh giá.

### Đóng góp cụ thể

- Thiết lập repository nhóm, cấu hình `origin`/`upstream`, chạy kiểm tra 13 public tests ban đầu.
- Thiết kế offline metric cho bước ghi lỗi hãng vận chuyển ở Phiếu A mục A2; ký và niêm phong `config/acceptance_criteria.json`.
- Chạy đánh giá baseline, phân tích trace `T-002@55` để tìm nguyên nhân lỗi chìm do `model_override`, xây dựng các cổng phòng ngừa trong `lab10/guards.py` và chốt mốc `prepared` bằng `lab10.checkpoint`.
- Phối hợp phân tích trace sự cố ở Vòng 2, cập nhật `lab10/guards.py` và bổ sung hàm theo dõi mới vào `lab10/monitors.py`.

### Bằng chứng

- Mã commit ký tiêu chí và chốt cổng vòng 1 (`config/acceptance_criteria.lock`, `config/round1.lock`).
- Nhật ký chạy trong `runs/journal.jsonl`, các mục A2, B0, B1, B2, B7.1–B7.3, C2, C7, C8.

### Exit ticket

- **Một điều học được:** Các lỗi nguy hiểm của trợ lý AI có quyền ghi sổ (như ghi đè độ trễ từ lời khai khách hàng, dùng lại phê duyệt cũ, hoặc lỗi khi LLM chạm rate limit) không thể sửa triệt để chỉ bằng prompt mà phải chặn bằng cổng cấp hệ thống (`pre_guard`, `write_gate`) đối chiếu trực tiếp với nguồn sự thật (DB).
- **Một điều còn chưa chắc:** Khi triển khai thật ở quy mô lớn (12 depot), làm sao tối ưu độ trễ truy vấn DB trong `write_gate` khi lượng giao dịch đồng thời tăng đột biến mà không tạo cổ chai mới.

---

## NgoHuyHoang-2A202603622

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh.
- **Câu của đề & mục phiếu:** Chủ trì Phiếu A (Câu 1.1 mục A1, Câu 1.5 mục A3, Câu 1.6 mục A4 - viết câu tiêu chí và ranh giới đầu ra), Câu 2.3 (Phiếu B mục B3 - bản đồ dữ liệu và ví dụ drift), Câu 2.9 (Phiếu B mục B7.4 - cổng kinh doanh), Quyết định Gate 1 v1 (Phiếu B mục B8), Câu 3.2 (Phiếu C mục C5 - specification) và Quyết định Gate 1 v2 (Phiếu C mục C12).
- **File phụ trách:** `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`), `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md` (B3, B7.4, B8), `templates/form-c-incident.md` (C5, C12).

### Đóng góp cụ thể

- Xác định mục tiêu cấp hệ thống, xây dựng hệ thống ngưỡng chấp nhận (`required`, `nice_to_have`, `business_ops`) và 4 quy tắc ra quyết định (`decision_rule`) trong `config/acceptance_criteria.json` trước khi chạy đánh giá.
- Lập bản đồ dữ liệu của trợ lý hoàn tiền và phân tích kịch bản drift khi chính sách chuyển từ `REFUND-v3` sang `REFUND-v4` vào ngày `2026-12-01`.
- Thiết lập các ngưỡng kinh doanh trong `config/operating_gates.json` (`daily_refund_cap_vnd = 1500000`, `cost_budget_per_ticket_vnd = 1200`, `pilot_scope`, `roi_min = 0.25`) dựa trên `ops_limits` và `ops_facts`.
- Phân tích chi phí mỗi ticket, ROI và bảng phân khúc theo kho/hãng để đưa ra quyết định Gate 1 ở cả hai mốc v1 và v2.
- Soát nhất quán Phiếu B với `lab10/ops.py` và `data/world.json`; phát hiện nhánh `KySuCong` có commit đưa Phiếu A về gần bản mẫu (có thể xoá nội dung đã điền nếu bị merge); chỉ ra các chỗ lệch số và cùng nhóm làm rõ.
- Viết phần của Hoàng trong Phiếu C cho thẻ S8 (C5 specification, phân tích tác động kinh doanh, đối chiếu từng tiêu chí đã ký, quyết định v2 đề xuất, mẫu C12) trên nhánh `hoang/vong2-S8`, dùng số trong `report.json` của ba mốc S8.
- Phát hiện nhận định "an toàn bằng 0 ở cả ba mốc" không đúng ở mốc base (`wrongful_refund_vnd = 6.845.000`, `wrongful_carrier_faults = 35`) và gửi nhóm danh sách chỗ lệch giữa Phiếu C và dữ liệu S8.

### Bằng chứng

- File `config/acceptance_criteria.json`, mục `business` trong `config/operating_gates.json`.
- Các mục A1, A3, A4 trong `templates/form-a-criteria.md`; B3, B7.4, B8 trong `templates/form-b-evaluation-gates.md`; C5, C12 trong `templates/form-c-incident.md`.
- Nhánh `hoang/vong2-S8`: khối "(Hoàng bổ sung)" trong `templates/form-c-incident.md`, đối chiếu với `submission/runs/R-S8-*/report.json`.

### Dùng AI

- Đã dùng Claude (Claude Code và claude.ai) để hỗ trợ soát Phiếu B và soạn phần Phiếu C. Mọi con số đối chiếu lại với `report.json` và `lab10/ops.py`.

### Exit ticket

- **Một điều học được:** Một hệ thống AI có `pass_rate` cao vẫn có thể gây lỗ nặng (ROI âm) nếu chỉ có 1–2 ca hoàn tiền sai giá trị lớn hoặc nếu chi phí nhân sự duyệt/kiểm mẫu vượt quá tiền tiết kiệm làm tay (10.000đ/ticket).
- **Một điều còn chưa chắc:** Cách định lượng chi phí uy tín dài hạn khi hãng vận chuyển bị phạt oan và ngừng hợp tác để đưa trực tiếp vào công thức tính ROI của pilot.

---

## NguyenVanNhi-2A202603697

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý.
- **Câu của đề & mục phiếu:** Câu 1.2 (Phiếu A mục A1 - mục tiêu từ góc nhìn kế toán đối soát và trưởng ca CSKH), Câu 1.4 (Phiếu A mục A2 - telemetry production), Câu 2.4 (Phiếu B mục B4 - HAZOP vòng 1 và mở rộng ngoài kỹ thuật; mục B5 - checklist 9 nhóm việc có PIC), Câu 2.5 (Phiếu B mục B6 - pre-mortem lăng kính vận hành & pháp lý), Câu 2.10 (Phiếu B mục B7.5–B7.6 - cổng vận hành/pháp lý, Runbook phần 1–3 và phương án Giờ cao điểm); Chủ trì Phiếu C (Câu 3.1–3.7 mục C3, C4, C5 câu 3.3, C6, C9, C10, C11 - phần riêng thẻ, HAZOP sự cố, giả định môi trường, fault tree trước/sau sửa, risk register, cập nhật checklist và Runbook phần 4–5) và gom bài nộp.
- **File phụ trách:** `config/operating_gates.json` (mục `operations` và `legal`), `templates/form-a-criteria.md` (A1.2, A2.4), `templates/form-b-evaluation-gates.md` (B4, B5, B6, B7.5, B7.6), `templates/form-c-incident.md`, `submission/submission.json`.

### Đóng góp cụ thể

- Xác định mục tiêu vận hành sát thực tế cho chị Phạm Kiều Oanh (`NV-OANH`) và chị Trần Thị Hạnh (`NV-HANH`); thiết kế telemetry giám sát rò rỉ PII và lỗi phạt hãng trên môi trường production không nhãn.
- Thực hiện phân tích HAZOP vòng 1 trên tool ghi kèm mở rộng ngoài kỹ thuật (công suất người duyệt 6 ca/giờ và lộ PII đơn quà tặng), lập checklist 9 nhóm việc go-live gắn PIC tên cụ thể.
- Cấu hình cổng `operations` (`pic: "NV-TUNG"`, `approver_id: "NV-HANH"`, `reviewers_on_shift`, `max_queue_wait_minutes: 60`, `stop_conditions`, `alert_channel`) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause: true`) trong `config/operating_gates.json`.
- Soạn thảo Runbook vận hành phần 1–5 và kịch bản ứng phó Giờ cao điểm; hoàn thiện hồ sơ sự cố Phiếu C, `submission/submission.json` và kiểm tra đủ thành phần bài nộp *(có sử dụng trợ lý AI hỗ trợ rà soát cấu trúc văn bản và kiểm tra đối chiếu dữ liệu `data/world.json`)*.

### Bằng chứng

- File `config/operating_gates.json` (mục `operations`, `legal`), `submission/submission.json`.
- Các mục A1 (1.2), A2 (1.4) trong Phiếu A; B4, B5, B6, B7.5, B7.6 trong Phiếu B; C3–C6, C9–C11 trong Phiếu C.

### Exit ticket

- **Một điều học được:** Cổng bảo vệ không chỉ nằm ở code (`guards.py`) mà còn nằm ở thiết kế vận hành và pháp lý: chỉ cần chặn đúng trường dữ liệu nhạy cảm (`recipient_contact`, `customer_note`) và bắt buộc đối chiếu `delay_cause` trước khi phạt hãng, kèm quy trình dừng khẩn cấp có người chịu trách nhiệm rõ ràng (`NV-TUNG`, `NV-HANH`), hệ thống sẽ tránh được rủi ro pháp lý với bên thứ ba.
- **Một điều còn chưa chắc:** Trong thực tế vận hành ca đêm khi lượng ticket tăng đột biến gấp 3 lần do bão lũ, việc huy động thêm người duyệt dự phòng trong 15 phút có khả thi hay phải ưu tiên tự động thu hẹp `pilot_scope` trước.
