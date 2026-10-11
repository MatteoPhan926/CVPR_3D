# Bàn giao: TRELLIS.2 → thao tác cửa xe, 10/10/2026

**Trạng thái:** hoàn tất phép điều tra có giới hạn. Có GLB/Blender/viewer mở cửa 0–60° và đóng lại, giữ texture gốc. **Chưa đạt mục tiêu CGI thuyết phục khi mở cửa; chưa có đóng góp CVPR/ICCV được chứng minh.** Đây là đánh giá kỹ thuật/hình ảnh của agent; chưa có artist nghiệm thu hoặc số liệu thời gian lao động.

## Đã làm và đã kiểm chứng

- Bảo toàn nguyên byte hai GLB người dùng cung cấp; kiểm tra format, UV/PBR, hình học và round-trip Blender cho cả hai. Không chạy lại generation, không gọi dịch vụ trả phí.
- Chọn A (`183055.354`) theo thứ tự tên file cho một lượt chỉnh cửa thông thường; B chỉ được kiểm tra raw/import/export/presentation.
- Giữ UV, texture và normals khi tách bề mặt; thêm lining, cạnh, jamb và nội thất đơn giản có tên rõ ràng. Giữ cả bản chỉ tách cửa, arrays/source-face IDs và các trạng thái trung gian.
- Xuất GLB, mở lại và kiểm tra 121 mẫu chuyển động, ảnh hero/side 0/30/60° cùng cận cảnh. Chu trình 2 giây mở + 2 giây đóng; thân xe giữ nguyên. Texture nhúng trong GLB cuối khớp byte với A gốc.
- Viewer đã qua kiểm tra slider 30/60°, đảo chiều/lặp lại, pause/reset, vật liệu và body cố định. Sửa lỗi lệch một frame ở viewer; không sửa GLB. Giữ bản lỗi và log.
- Có review độc lập và phản biện dựa trên ảnh thực tế, dữ liệu và mã.

## Kết luận và giới hạn

Phần tích cực là đường đi asset → DCC → tách vùng → điều khiển → export hoạt động, với ảnh đóng gần như giữ nguyên. Phần chưa đạt là cạnh/frame nhiều lớp, lởm chởm và khoang nội thất còn thô, thấy cả ở ảnh toàn xe và sau mở lại.

Giải thích thay thế mạnh nhất: cách chọn vùng bằng polygon/depth và cách hoàn thiện đơn giản tương tác với bề mặt đã tạo. Chưa chứng minh đây là giới hạn nội tại của TRELLIS.2 hay là trần chất lượng của chỉnh sửa thủ công có chuyên môn. Không lấy tỷ lệ diện tích gốc cao hoặc mesh liền khối làm bằng chứng cho một bottleneck nghiên cứu.

Người dùng báo đã thử 512/1536 trên Hugging Face, nhưng mapping từng file, seed, decimation và hash ảnh conditioning (gốc hay đã tách nền) vẫn **unknown**. Hai file không phải so sánh resolution có đối chứng. Không gán thiết lập từ screenshot của lượt lỗi. Thử nghiệm xe độc lập khác vẫn chưa xác định được run/branch; nghiên cứu revision ngoài xe vẫn chưa bắt đầu.

## Quyết định tiếp theo

Dừng lượt sửa này và giữ kết quả partial. Bước nghiên cứu có giá trị tiếp theo là baseline chuẩn bị cục bộ bằng DCC có chuyên môn, cùng contract/camera, ghi thời gian thao tác thực và artist chấp nhận/từ chối. Chỉ phát triển phương pháp nếu một bất lợi chất lượng–chi phí/độ tin cậy/điều khiển còn lặp lại qua các asset/tác vụ được chọn trước, và prototype cải thiện so với baseline thích hợp. Nếu công cụ thông thường đã đủ tốt, đóng nhánh giả thuyết đó. Chưa chọn topology, articulation hay learned editing làm đóng góp.

## File và khôi phục

- [Báo cáo đầy đủ](FINAL_REPORT.md); [download và checkpoint](DOWNLOADS.md); [run ledger](RUN_LEDGER.json).
- `artifacts/authoring_A_v1/car_door_authored.glb` và `.blend`: kết quả chỉnh cửa.
- `artifacts/viewer/car_door_standalone.html`: viewer tự chứa asset/thư viện. Trình duyệt cloud cấm `file://`; đã kiểm chứng qua localhost, không dùng request ngoài. Cách chạy nằm trong README. Chưa xác minh mở file trực tiếp hoặc FPS tương tác.
- `artifacts/reopened_A_v1/`: ảnh/trạng thái sau mở lại; `research/final_validation/`, `research/selection_diagnostic/`, `research/final_adversarial_review/`, `research/viewer/`: bằng chứng.
- `inputs/`: hai GLB gốc, provenance và ảnh tham chiếu dự kiến.

Nhánh: `trellis2-downstream-assets-20261009`, remote `MatteoPhan926/CVPR_3D`. Dùng commit/URL chính xác trong DOWNLOADS; tải lại và kiểm checksum trước khi xử lý tiếp. Local commit/ZIP không được coi là backup. Giữ nguyên thay đổi đang có; khôi phục vào thư mục mới nếu xung đột. Không tự chạy lại setup nặng, generation hay authoring để thay artifact bị thiếu. Metadata và latent chưa được cung cấp phải tiếp tục ghi là thiếu.

Handoff này được lưu trên GitHub để người dùng chuyển tiếp; không gửi tin nhắn cho một người/địa chỉ secretary bên ngoài.
