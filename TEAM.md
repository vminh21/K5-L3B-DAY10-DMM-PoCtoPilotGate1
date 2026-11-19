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

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
