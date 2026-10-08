# Recovery checkpoint — nghiên cứu ngày 08/10/2026

Cloud đã đọc lại được workspace gốc. Đây là gói bảo toàn artifact thực tế, gồm cả output chưa hoàn tất và log lỗi. Không chạy lại thí nghiệm để tạo lại bằng chứng.

**Đã xác minh bản sao ngoài cloud:** tải lại đủ năm ZIP và kiểm tra hash của 813 file. Cả ba latent đều được giữ. [Biên bản xác minh](EXTERNAL_VERIFICATION.json).

Commit dữ liệu: `42dc0ea31f75e8783bf1f208b8fb83d523ab076c`. Xác minh này kiểm tra byte đã lưu, không phải chạy lại nghiên cứu.

- [Báo cáo recovery và trạng thái từng công việc](RECOVERY_REPORT.md)
- [Manifest mọi file](MANIFEST_SHA256.json)
- [Phạm vi, file nguồn và phần loại trừ](source_manifest.json)
- [Code, báo cáo, JSON và hình có thể xem ngay trên GitHub](evidence/)
- [Cấu hình onboarding đã lưu](configuration_snapshot.json)

## Tải dữ liệu

Các ZIP dưới đây độc lập, không cần ghép nhị phân. Tải cả năm để có toàn bộ checkpoint; giải nén vào một thư mục recovery mới. Không giải nén đè workspace hiện có.

| ZIP | Nội dung | Dung lượng |
|---|---|---|
| [01 — Generation](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/01_research_generation.zip) | Provenance, density grids, field/mesh variants và ảnh | 76.8 MB |
| [02 — Controls và holdouts](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/02_research_controls_and_holdouts.zip) | Toàn bộ phần nghiên cứu còn lại; teapot/hamburger raw meshes và latents, refinement, authoring controls, review, logs | 55.6 MB |
| [03 — Probe xe](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/03_car_probe.zip) | Raw/authored assets, Blender files, input, **latent xe gốc**, scripts và logs | 78.0 MB |
| [04 — Source và metadata](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/04_dependency_source_and_metadata.zip) | Dependency source, environment mesh arrays, input attachments, cấu hình và provenance recovery | 34.8 MB |
| [05 — Bentley](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/05_bentley.zip) | Asset, source, reports và bằng chứng lịch sử | 58.0 MB |

808 file nguồn được giữ nguyên, cộng 5 file metadata recovery. Cả ba `scene_codes.pt` đều có trong gói. Các ZIP và từng file bên trong có SHA-256.

## Khôi phục có kiểm tra

Dùng Python 3.11 trở lên, không cần cài package. Lấy commit dữ liệu đầy đủ từ receipt xác minh, rồi chạy:

```bash
python3 download_and_verify.py --commit 42dc0ea31f75e8783bf1f208b8fb83d523ab076c --destination ./recovered-checkpoint-new
```

Script tải từ commit cố định, kiểm tra hash từng ZIP, giải nén an toàn vào thư mục mới và kiểm tra toàn bộ file. Nó từ chối thư mục đích đã tồn tại và không thực thi code nghiên cứu.

## Giới hạn

Không backup VM, credentials, processes, installed venv/node_modules hoặc model weights có thể tải lại. Danh sách loại trừ được ghi rõ. **Latent, arrays, mesh, ảnh, logs và kết quả dở không bị coi là cache để loại bỏ.**

Chưa chứng minh pipeline nghiên cứu chạy lại được từ máy mới; checkpoint này bảo toàn và xác minh byte của bằng chứng, không xác nhận chất lượng nghiên cứu.

