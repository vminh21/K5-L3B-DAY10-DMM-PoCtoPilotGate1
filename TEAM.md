# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): DMM
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-DMM-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S3

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Văn Minh | 2A202603771 | Kỹ sư cổng | ✔ |
|   2 | Đoàn Anh Hùng | 2A202603880 | Sản phẩm và kinh doanh | |
|   3 | Nguyễn Hữu Thịnh | 2A202603726 | Vận hành và pháp lý | |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenVanMinh-2A202603771

### Phần việc phụ trách

Trưởng nhóm, vai **Kỹ sư cổng**. Câu 1.3 (Phiếu A mục A2), câu 2.1, 2.2, 2.6, 2.7, 2.8 (Phiếu B mục B0, B1, B2, B7.1, B7.2, B7.3), câu 3.1 phần trace, 3.5 phần code, 3.6 (Phiếu C mục C0, C2, C7, C8). File: `lab10/guards.py`, `lab10/monitors.py`; chạy lệnh ký, chốt vòng 1, `eval`, `trace`, `grade`, gom bài.

### Đóng góp cụ thể

- Viết 3 cổng vòng 1 trong `lab10/guards.py`: **G0** `pre_guard` ghim chính sách theo ngày hiệu lực; **G1** `issue_refund` tính lại mức được hưởng từ tracking DB, chặn hoàn trùng, kiểm phê duyệt, người trả phải là LOGIX; **G2** `file_carrier_fault` chỉ ghi lỗi khi tracking có nguyên nhân thuộc lỗi hãng, `notify_carrier` chỉ gửi trường được phép.
- Vòng 2 (thẻ S3): thêm vào G2 trần lỗi tự động mỗi hãng mỗi ngày theo `ops_limits`; thêm monitor `max_carrier_strikes_per_day`, `strike_cap_hits` (tổng 9 monitor mới trong `lab10/monitors.py`).
- Kết quả: bộ nền pass_rate 0.9909 → 1.0, hoàn sai 20.000đ → 0; gói S3 pass_rate 0.25 → 0.83 (chỉ cổng vòng 1) → 1.0, lỗi oan cho hãng 35 → 10 → 0.

### Bằng chứng

- Commit: `6b0b801` (ký tiêu chí), `0ba9eed` (chốt vòng 1, v1), `4b74b74` (nhận thẻ S3), `e98c2bc` (sửa vòng 2), `31177c8` (C7, C8).
- Mã lần chạy: base `R-base-before-20261119-160003-144804`, prepared `R-base-prepared-20261119-160814-4fa251`; S3 grade `R-S3-grade-20261119-165251-e173dc`, after `R-S3-after-20261119-165246-e173dc`.
- Phiếu B mục B2 (`T-002@55`), B7.1–B7.3; Phiếu C mục C2, C7, C8.

**Dùng AI:** dùng Claude Code (Claude) để đọc code agent, gợi ý và viết cổng trong `guards.py`, monitor trong `monitors.py`, chạy lệnh, và soạn nháp các ô phiếu do mình phụ trách; mình đọc lại, chạy kiểm và chịu trách nhiệm từng con số. Một lần AI chạy thử trợ lý trên bộ nền bằng script ngoài `lab10.eval` trước khi bàn ký tiêu chí; bàn đã đặt lại ngưỡng độc lập (không dùng các số đó) rồi mới ký.

### Exit ticket

Học được: không sửa được model thì vẫn kiểm soát được tác hại bằng cổng đặt trước lệnh ghi, miễn cổng đọc nguồn sự thật chứ không đọc lời khách hay suy đoán của model. Còn chưa chắc: cổng chỉ tốt bằng dữ liệu nó đọc; khi chính tracking ghi sai nguyên nhân thì cổng không biết, và chưa rõ đo tỉ lệ đó thế nào trước khi chạy thật.

## DoanAnhHung-2A202603880

### Phần việc phụ trách

Thành viên 2, vai **Sản phẩm và kinh doanh**. Câu 1.1, 1.6 (Phiếu A mục A1, A4, A5); câu 2.3, 2.9 (Phiếu B mục B3 bản đồ dữ liệu, B7.4 cổng kinh doanh); quyết định v1 (Phiếu B mục B8); câu 3.2 và quyết định v2 (Phiếu C mục C5, C12). File: `config/acceptance_criteria.json` (ngưỡng, `stop_condition`, `decision_rule`), `config/operating_gates.json` mục `business`, `submission/submission.json` (`decision_v1`, `decision_v2`).

### Đóng góp cụ thể

- Đặt Bản tiêu chí trước khi xem số: 5 ngưỡng bắt buộc (`pass_rate` ≥ 0.98, `pass_k` ≥ 0.95, hoàn sai / lỗi oan / lộ dữ liệu = 0), `escalation_rate` ≤ 0.35, nhóm `business_ops` (chi phí ≤ 7.500đ/ticket so với 10.000đ làm tay, ROI ≥ 0.30, 0 ca ùn), điều kiện dừng và bốn dòng `decision_rule`; mục tiêu lấy từ PRD v1.1 §3 của Lab 9.
- Bản đồ dữ liệu B3: `refund_status` và `index_active` là bản sao, `effective_from/effective_to` là nguồn sự thật; nêu trước kịch bản drift REFUND-v3 → v4 ngày 2026-12-01, đúng nguyên nhân chính của thẻ S3.
- Cổng kinh doanh B7.4: trần hoàn tự động 1.500.000đ/ngày (75% ngân sách Finance 2.000.000đ), ngân sách 1.500đ/ticket, phạm vi 4 kho 100%, `roi_min` 0.30.
- Quyết định Gate 1: v1 **Tiếp tục** (mốc prepared đạt mọi ngưỡng đã ký); v2 **giữ Tiếp tục** sau sự cố S3 vì mốc after đạt mọi ngưỡng trên bộ nền và gói sự cố, kèm điều kiện đối soát lỗi hãng hằng tuần và ngày quyết định lại 2026-11-27.

### Bằng chứng

- Commit ký tiêu chí `6b0b801` (hash `eea0271e`), ký lúc 15:57:01, trước lần đánh giá đầu tiên 16:00:03.
- Mã lần chạy dùng cho quyết định: v1 `R-base-prepared-20261119-160814-4fa251`; v2 `R-S3-after-20261119-165251-e173dc`, grade `R-S3-grade-20261119-165251-e173dc` (ROI 1.51, chi phí 3.980đ/ticket, không vượt trần).
- Phiếu A mục A1, A4, A5; Phiếu B mục B3, B7.4, B8; Phiếu C mục C5 câu 3.2, C12.

### Exit ticket

Học được: ngưỡng phải viết và ký trước khi nhìn số, kèm câu "nếu trượt thì làm gì"; khi số ra xấu, quyết định đúng là quyết định khớp tiêu chí đã ký chứ không phải quyết định đẹp nhất. Còn chưa chắc: ngưỡng chi phí và ROI đặt trên dữ liệu giả (một ngày 22 ticket); với lượng ticket thật ở 2 depot, chưa chắc 7.500đ/ticket còn hợp lý.

## NguyenHuuThinh-2A202603726

### Phần việc phụ trách

Thành viên 3, vai **Vận hành và pháp lý**. Câu 1.2, 1.4 (Phiếu A mục A1, A2); câu 2.4, 2.5, 2.10 (Phiếu B mục B4 HAZOP vòng 1, B5 checklist 9 nhóm, B6 pre-mortem, B7.5 runbook 1–3, B7.6 giờ cao điểm); câu 3.1 phần riêng của thẻ, 3.3, 3.7 (Phiếu C mục C3.5, C4, C5 câu 3.3, C9, C10, C11). File: `config/operating_gates.json` mục `operations` và `legal`.

### Đóng góp cụ thể

- HAZOP vòng 1 trên `issue_refund`: dòng kỹ thuật và ba dòng ngoài kỹ thuật (người duyệt, ngân sách, dữ liệu gửi bên thứ ba).
- Checklist 9 nhóm việc có PIC có tên cho từng dòng (NV-TUNG, NV-HANH, NV-OANH); pre-mortem có dòng "hãng nhỏ bị ghi lỗi oan khi `delay_cause` không thuộc lỗi hãng", một trong ba nguyên nhân của thẻ S3, đã thành cổng từ vòng 1.
- Cổng con người và pháp lý trong config: PIC `NV-TUNG`, người duyệt `NV-HANH`, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, 6 điều kiện dừng, kênh `#logix-pilot-alerts`; không gửi `recipient_contact`, `customer_note` cho hãng; ghi lỗi hãng phải có nguyên nhân trong tracking. Runbook 1–3 và giờ cao điểm dùng đúng các con số đó.
- Vòng 2 (thẻ S3): mở lại bản đồ dữ liệu (C3.5), HAZOP của thẻ trên `file_carrier_fault`, giả định môi trường, fault tree sau sửa, risk register (tracking ghi sai nguyên nhân, PIC NV-OANH; đổi phiên bản chính sách, PIC NV-TUNG), checklist cập nhật và runbook 4–5.

### Bằng chứng

- `config/operating_gates.json` (bản vòng 1 đã chốt trong `config/operating_gates.round1.json`, hash `032a6476`); lệnh kiểm bài nộp xác nhận "cổng con người đã điền: PIC, người duyệt, kênh báo tin, điều kiện dừng".
- Mã lần chạy: gói S3 after `R-S3-after-20261119-165251-e173dc` (0 ca ùn, chờ lâu nhất 0 phút, 0 lộ dữ liệu, 0 lỗi oan).
- Phiếu B mục B4, B5, B6, B7.5, B7.6; Phiếu C mục C3.5, C4, C9, C10, C11.

### Exit ticket

Học được: rủi ro lớn nhất của một trợ lý có quyền ghi sổ nằm ngoài code: ai duyệt, bao nhiêu người trực, dữ liệu của ai đi ra ngoài, ai bấm dừng; runbook phải có con số khớp config thì mới dùng được lúc sự cố. Còn chưa chắc: khi tracking ghi sai nguyên nhân (chứ không bỏ trống) thì cổng không phát hiện được, và chưa rõ đối soát hằng tuần với hãng có kịp trước khi hãng nhỏ bị đình chỉ.
