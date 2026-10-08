# Recovery checkpoint — nghiên cứu ngày 08/10/2026

Cloud đã đọc lại được workspace gốc. Đây là gói bảo toàn artifact thực tế, gồm cả output chưa hoàn tất và log lỗi. Không chạy lại thí nghiệm để tạo lại bằng chứng.

**Trạng thái tại commit dữ liệu ban đầu:** đã đóng gói; cần xem `EXTERNAL_VERIFICATION.json` ở commit xác minh tiếp theo để biết kết quả tải lại.

- [Báo cáo recovery và trạng thái từng công việc](RECOVERY_REPORT.md)
- [Manifest mọi file](MANIFEST_SHA256.json)
- [Phạm vi, file nguồn và phần loại trừ](source_manifest.json)
- [Code, báo cáo, JSON và hình có thể xem ngay trên GitHub](evidence/)
- [Cấu hình onboarding đã lưu](configuration_snapshot.json)

## Tải dữ liệu

Các ZIP dưới đây độc lập, không cần ghép nhị phân. Tải cả năm để có toàn bộ checkpoint; giải nén vào một thư mục recovery mới. Không giải nén đè workspace hiện có.

| ZIP | Nội dung | Dung lượng |
|---|---|---|
| [01 — Generation](archives/01_research_generation.zip?raw=true) | Provenance, density grids, field/mesh variants và ảnh | 76.8 MB |
| [02 — Controls và holdouts](archives/02_research_controls_and_holdouts.zip?raw=true) | Toàn bộ phần nghiên cứu còn lại; teapot/hamburger raw meshes và latents, refinement, authoring controls, review, logs | 55.6 MB |
| [03 — Probe xe](archives/03_car_probe.zip?raw=true) | Raw/authored assets, Blender files, input, **latent xe gốc**, scripts và logs | 78.0 MB |
| [04 — Source và metadata](archives/04_dependency_source_and_metadata.zip?raw=true) | Dependency source, environment mesh arrays, input attachments, cấu hình và provenance recovery | 34.8 MB |
| [05 — Bentley](archives/05_bentley.zip?raw=true) | Asset, source, reports và bằng chứng lịch sử | 58.0 MB |

808 file nguồn được giữ nguyên, cộng 5 file metadata recovery. Cả ba `scene_codes.pt` đều có trong gói. Các ZIP và từng file bên trong có SHA-256.

## Khôi phục có kiểm tra

Dùng Python 3.11 trở lên, không cần cài package. Lấy commit dữ liệu đầy đủ từ receipt xác minh, rồi chạy:

```bash
python3 download_and_verify.py --commit FULL_DATA_COMMIT_SHA --destination ./recovered-checkpoint-new
```

Script tải từ commit cố định, kiểm tra hash từng ZIP, giải nén an toàn vào thư mục mới và kiểm tra toàn bộ file. Nó từ chối thư mục đích đã tồn tại và không thực thi code nghiên cứu.

## Giới hạn

Không backup VM, credentials, processes, installed venv/node_modules hoặc model weights có thể tải lại. Danh sách loại trừ được ghi rõ. **Latent, arrays, mesh, ảnh, logs và kết quả dở không bị coi là cache để loại bỏ.**

Chưa chứng minh pipeline nghiên cứu chạy lại được từ máy mới; checkpoint này bảo toàn và xác minh byte của bằng chứng, không xác nhận chất lượng nghiên cứu.

