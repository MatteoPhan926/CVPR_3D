# Bàn giao secretary — TRELLIS.2 car follow-up, 09/10/2026

**Trạng thái:** cloud chạy lệnh, đọc/ghi và push GitHub được. Chưa có asset TRELLIS.2; thí nghiệm end-to-end vẫn bị chặn ở dịch vụ cấp GPU. Không có kết luận mới về chất lượng mô hình hay đóng góp CVPR/ICCV.

Đã thực hiện:

- Giữ đúng ảnh xe trên cỏ và yêu cầu mở cửa trước; đọc intent, log cũ, API và mã Space, không đổi mô hình hay task.
- Tách nhánh `trellis2-car-followup-20261009`; giữ nguyên nghiên cứu và probe cũ. Rehash ảnh, raw GLB, latent và authored GLB cũ đều khớp.
- Sửa lỗi client thiếu Pillow trước khi có bất kỳ API call nào; giữ log lỗi. Agent độc lập kiểm tra API, session và bản sửa.
- Chạy thành công session và tiền xử lý chính thức; xem ảnh trả về, xác nhận trùng byte với PNG lịch sử.
- Gửi **một** yêu cầu sinh TRELLIS.2. Dịch vụ trả lỗi ZeroGPU sau khoảng **0,892 giây**, `120s requested vs. 176s left`. **0 preview, 0 export, 0 GLB**. Không tự retry quota.
- Review phản biện xác nhận: lỗi truy cập thực thi; không được quy thành thất bại về chất lượng của TRELLIS.2. Số quota hiển thị mâu thuẫn, nguyên nhân policy/accounting cụ thể chưa rõ.
- Checkpoint GitHub và tải lại kiểm checksum sau từng mốc thực thi (01–04). Bản tải handoff cuối và receipt xác minh được lập chỉ mục tại [DOWNLOADS.md](DOWNLOADS.md); receipt được tạo sau archive và nằm cạnh archive trên GitHub.

**Cần để tiếp tục:** quyền sử dụng GPU thực sự trên Space, đủ cho cả generation lẫn export. Đã lưu draft yêu cầu secret `HF_TOKEN` cho Hugging Face/Space và hướng dẫn phục hồi an toàn; chưa có token, chưa kiểm chứng xác thực hay quota. Người dùng nhập secret trong environment settings, review/save và publish theo yêu cầu nền tảng. Không gửi token trong chat. Có token không bảo đảm được cấp GPU.

Khi điều kiện truy cập thay đổi, tạo attempt mới, không ghi đè attempt001; checkpoint trước bước tốn kém. Nếu có asset, kiểm tra export và bảo toàn UV/PBR trước khi chuẩn bị cửa, rồi kiểm chứng pose 0/30/60°, chuyển động thuận/ngược và diện mạo theo intent cũ. Không dùng nguyên trạng script vertex-color của TripoSR. Không chuyển sang nghiên cứu revision ngoài xe: việc đó chưa bắt đầu và không thuộc lượt này.

**Phân biệt hồ sơ:** TripoSR car cũ có output và thất bại target CGI; TRELLIS.2 chưa có output; metadata của lượt xe khác được nhắc riêng vẫn chưa xác định. Không gộp ba việc thành một kết quả.

Nghiên cứu trước đã được phục hồi và bàn giao riêng, không bị thay bằng kết quả chặn truy cập này:

- [Báo cáo quyết định nghiên cứu trước](https://github.com/MatteoPhan926/CVPR_3D/blob/57dcd5a510cd1ac10a292a8cee2ca9913f7ef375/research_decision_delivery_20261009/RESEARCH_DECISION.md).
- [ZIP tổng hợp nghiên cứu trước](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/c344c863aab527bececa307b29547e96597a0725/research_decision_delivery_20261009/RESEARCH_DECISION_OUTPUT_20261009.zip), SHA-256 `764eec7ccd424fbe7c6f731e5236f65e5362cd85ebac142145cd9d6f3ab44933`.
- [Receipt phục hồi đầy đủ 813 tệp cũ](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/8df00f1481b2e75741eb01e6c076315f9d60f6bb/recovery_checkpoint_20261008/EXTERNAL_VERIFICATION.json), gồm các mesh, arrays và ba latent đã lưu.

Chi tiết mới: [FINAL_REPORT.md](FINAL_REPORT.md), [RUN_LEDGER.json](RUN_LEDGER.json), [review phản biện](research/ADVERSARIAL_REVIEW.md). Đây là bàn giao qua tệp GitHub theo yêu cầu, không phải xác nhận đã nhắn cho một tài khoản secretary bên ngoài.
