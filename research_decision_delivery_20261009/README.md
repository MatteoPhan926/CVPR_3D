# Kết quả task nghiên cứu — 09/10/2026

**Đã có output nghiên cứu và bản tổng hợp quyết định. Chưa có method CVPR/ICCV được chứng minh.**

Quyết định: **đổi trọng tâm sang đo giá trị của một thao tác downstream cụ thể; chưa đầu tư một method mới.** Giữ các kiểm tra và cải thiện kỹ thuật đã đo được. Không tiếp tục biến việc sửa chiếc xe thành chiến dịch tìm novelty.

- [Báo cáo nghiên cứu đầy đủ](RESEARCH_DECISION.md)
- [Bàn giao cho secretary](SECRETARY_HANDOFF.md)
- [Trạng thái từng công việc](RUN_LEDGER.json)
- [Đối chiếu độc lập và phản biện](REVIEWS.md)
- [Số liệu tổng hợp có thể kiểm tra](DERIVED_SUMMARY.json)
- [Manifest và link toàn bộ artifact lớn](FULL_EVIDENCE.json)

## Những gì đã thực hiện và học được

1. **Xác minh đúng model và execution.** Xe đã audit do TripoSR CPU sinh; TRELLIS.2 bị quota chặn trước output. Replay từ đúng input đã xử lý tái tạo latent chính xác, sai số tối đa 0. Không thể dùng kết quả này để đánh giá TRELLIS.2 hoặc mọi generator.
2. **Tách lỗi hiển thị khỏi lỗi asset.** Chỉ đổi material hiển thị đã gây sai khác RGB lớn; chia mesh với cùng material gần như giữ nguyên ảnh ở hai góc đóng đã đo. Selection làm cửa có một mảnh dưới tách rời. Vì vậy, screenshot xấu chưa đủ chứng minh bottleneck topology.
3. **Sinh hai đối chứng ngoài xe.** Teapot và hamburger đều có raw mesh, latent, config và log; mỗi asset một inference. Đây không phải phép thử revision của artist.
4. **Thử một cải thiện số học có kiểm soát.** Bisection trên cạnh và lấy mẫu màu lại giảm MAE so với native field khoảng **11,0% / 6,8% / 18,4%** cho xe/teapot/hamburger. Phần lớn mức giảm vẫn xuất hiện khi giữ hình học gốc và dùng màu mới. Đây là cải thiện độ khớp với chính model, chưa phải bằng chứng hình học đúng hơn hoặc artist làm việc tốt hơn.
5. **Tìm được lỗi triển khai cụ thể.** Comparator log-density dừng vì assert yêu cầu `trunc_exp`, trong khi checkpoint thực dùng `exp`. Phép thử đó chưa cho kết quả; không được gọi là phương pháp thất bại. Browser export validation cũng chưa pass.
6. **Kiểm tra thành công bị bỏ sót và novelty.** Bentley giữ được texture/hình học không chỉnh sửa; lỗi OOM Particulate trong lịch sử đã được sửa. Edge bisection có prior trực tiếp. Những điều này làm yếu đi cả kết luận bi quan quá rộng lẫn một claim method mới quá sớm.

## Kết luận mạnh nhất và bước tiếp theo

**Cách giải thích cạnh tranh mạnh nhất:** hiệu chỉnh display, nội suy và lấy mẫu màu giải thích phần đáng kể kết quả; quy trình chọn cửa và bù nội thất cũng gây nhiễu. Hiện chưa đo artist acceptance, thời gian lao động tiết kiệm hoặc một thao tác downstream có ích.

Đề xuất tiếp theo là **một pilot có giới hạn**, dùng asset ngoài xe hiện có cho một công việc thật như bố trí cảnh/preview camera. Chốt yêu cầu trước; so với mesh chuẩn bị bằng công cụ thông thường/texture baking, image card và native field nếu phù hợp. Nếu baseline thường đã đáp ứng tốt và không còn khoảng cải thiện chất lượng–chi phí đáng kể, giữ workflow hữu ích và đóng claim method đó. Nếu có residual quan trọng, lặp lại được và một can thiệp dự đoán được lợi ích, mới cấp thêm một prototype.

Pilot này **chưa chạy**. Không cần một thất bại kịch tính để làm nghiên cứu; một cải thiện nhỏ nhưng có ích, đo được và vượt đối chứng thích hợp cũng đáng xét.

## Tải và kiểm tra

`RESEARCH_DECISION_OUTPUT_20261009.zip` là gói báo cáo/handoff và bằng chứng chọn lọc, gồm cả ảnh đối chứng. Toàn bộ meshes, latents và arrays nằm trong năm ZIP recovery đã tải lại xác minh; xem [FULL_EVIDENCE.json](FULL_EVIDENCE.json).

Bản tổng hợp này chỉ đọc hồ sơ và tính lại số học từ JSON. Không inference, render hoặc sửa asset trong lượt bàn giao. Dữ liệu nguồn và checkpoint recovery cũ được giữ nguyên.

