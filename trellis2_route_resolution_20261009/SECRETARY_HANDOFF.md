# Bàn giao secretary — điều tra route TRELLIS.2, 09/10/2026

**Kết quả chính:** đã chuẩn bị được route fal TRELLIS.2 cụ thể và thu hẹp lỗi của route Hugging Face. **Chưa có output TRELLIS.2 cho xe của người dùng**, chưa thử mở cửa, chưa có kết luận chất lượng hay đóng góp CVPR/ICCV. Không có lượt API trả phí hoặc upload ảnh người dùng mới.

## Đã hoàn thành và có bằng chứng

- Đọc báo cáo/handoff trước; giữ đúng ảnh xe và intent cửa trước 0–60°. Bảo toàn dữ liệu qua các lần cloud reconnect.
- Kiểm tra auth thực tế: HF_TOKEN đã hiện diện, nhưng client chính thức vẫn trả 401. Lần cuối **22:16 ngày 9/10, giờ Bangkok**. Chưa tách được lỗi token khỏi binding/proxy. Máy không có NVIDIA; FAL_KEY/Meshy/Tripo key chưa hiện diện trong lần kiểm tra.
- Kiểm tra đúng source `spaces==0.50.2`: ở cấu hình Blackwell/non-xlarge, duration120 có thể thành180 khi schedule nhưng lỗi vẫn hiển thị120. Đây là giải thích có điều kiện cho `120 vs176`; chưa biết cấu hình server thật, chưa giải thích dứt điểm `120 vs180`.
- Điều tra độc lập tài liệu chính thức: fal TRELLIS.2 có GLB và các tham số cần dùng, giá công bố **$0,30/lượt1024**; Meshy7.1 là comparator hiện đại, standard+2K/PBR **30APIcredits**, cần paid-plan API entitlement. Chưa có kết quả so sánh chất lượng. Tripo chỉ lấy được app shell nên không kết luận.
- Tạo [payload fal chưa gửi](config/fal_request_prepared_NOT_SUBMITTED.json), giữ nguyên byte ảnh gốc/seed42/các tham số kế thừa; kiểm schema và roundtrip ảnh thành công. Provider preprocessing/revision không được xác nhận giống Microsoft Space.
- Tải một **GLB mẫu công khai** từ docs fal để kiểm tra format. Mẫu có UV, base-color và metallic/roughness, dùng WebP. Validator báo18lỗi normal; Blender4.3.2 mở được, giải mã2texture2048 và nối đúng kênh. Import ít hơn20mặt; raw có57tamgiác diện tích0, chưa ánh xạ mặt bị đổi. Không render/re-export/sửa mesh. Mẫu **không phải xe người dùng**, không thay thế generation.
- Review độc lập ban đầu và phản biện đã hoàn thành; mọi giả thuyết/giới hạn được giữ trong báo cáo. ZIP/manifest/receipts nằm trong [DOWNLOADS.md](DOWNLOADS.md).

## Đang bị chặn / chưa chạy

Auth Hugging Face chưa dùng được; có token không bảo đảm quota. Chưa có GPU admission/generation/export mới cho xe. Chưa có door-authoring/artist acceptance. Nghiên cứu revision riêng chưa bắt đầu. Metadata của một lượt xe riêng khác vẫn chưa xác định; không gộp với lượt này.

## Điều kiện để chạy tiếp

**Route gốc:** kiểm tra/sửa đường HF_TOKEN trong environment settings để official whoami trả200; không gửi secret trong chat. Sau đó cần quota/chi phí được phép cho **cả generation lẫn export**, cùng live session. Tài khoản trả phí có thể tự trừ credits khi vượt quota; không coi đó là miễn phí mặc định.

**Route fal đã chuẩn bị:** cần người dùng cho phép đúng **một** lượt1024 với giá công bố$0,30, FAL_KEY hợp lệ qua secure settings và số dư prepaid đủ. Chưa biết mức nạp tối thiểu/tổng chi phí mở tài khoản; không khẳng định chỉ cần nạp$0,30. Việc đổi provider/preprocessing/checkpoint phải được ghi rõ. Chưa thêm binding FAL_KEY hoặc tự thực hiện thanh toán.

Khi có output thật: lưu raw asset/metadata/latents có thể tải, push+download-verify trước authoring; bảo toàn UV/PBR; kiểm appearance qua import/export rồi chuẩn bị cửa bằng công cụ thông thường trong budget cũ. Không dùng nguyên trạng script cắt vertex-color TripoSR. Không đổi sang một cơ chế nghiên cứu chỉ vì lỗi thực thi hay18normals của mẫu.

Onboarding đã lưu/read-back `start_skill` mới với checkpoint và quy tắc không ghi đè. Không đổi install script/secret; cấu hình cần review/save/publish theo UI, việc đó tự nó không sửa401.

## Hồ sơ liên quan

- [Báo cáo lượt này](FINAL_REPORT.md), [run ledger](RUN_LEDGER.json), [review phản biện](research/adversarial_review/FINDINGS.md).
- [Lượt TRELLIS bị từ chối trước](https://github.com/MatteoPhan926/CVPR_3D/blob/abf0cb8fb1375b92affdc26e8cdacc66f508e499/trellis2_car_followup_20261009/FINAL_REPORT.md).
- [Tổng hợp nghiên cứu trước](https://github.com/MatteoPhan926/CVPR_3D/blob/57dcd5a510cd1ac10a292a8cee2ca9913f7ef375/research_decision_delivery_20261009/RESEARCH_DECISION.md), [ZIP](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/c344c863aab527bececa307b29547e96597a0725/research_decision_delivery_20261009/RESEARCH_DECISION_OUTPUT_20261009.zip).
- [Receipt phục hồi813tệp gốc, gồm3latent](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/8df00f1481b2e75741eb01e6c076315f9d60f6bb/recovery_checkpoint_20261008/EXTERNAL_VERIFICATION.json).

Đây là bàn giao bằng tệp GitHub theo yêu cầu; không phải xác nhận đã nhắn một tài khoản secretary bên ngoài.
