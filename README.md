# Image → car probe — kết quả mới

[Xem ảnh và hướng dẫn tải](image_to_usable_car_probe_20261007/README.md) · [Tải ZIP đầy đủ (18,6 MB)](https://github.com/MatteoPhan926/CVPR_3D/raw/refs/heads/image-to-usable-car-20261007/image_to_usable_car_probe_20261007/IMAGE_TO_USABLE_CAR_PROBE_20261007_evidence.zip) · [Báo cáo](image_to_usable_car_probe_20261007/IMAGE_TO_USABLE_CAR_REPORT.md)

Bản thử nghiệm từ ảnh Citroën có chuyển động cửa 0–60°. Kiểm tra điều khiển đã đạt; **chất lượng hình ảnh vẫn là kết quả một phần, chưa đạt CGI thuyết phục**.

![Cửa mở](image_to_usable_car_probe_20261007/source/viewer/verification/final/authored_open.png)

---

# Bentley authoring session — download package

Download `Bentley_authoring_session.zip`, then extract it. The session contains the original and animated GLB, offline preview, source/configuration, validation, provenance and report. Run `launch.sh` from the extracted session folder with Python 3 installed.

The authored cabin door opens continuously from 0 to 65 degrees. Blender and Chromium reopening checks passed. Physical clearance is incomplete: lining/sill and local hinge/trim intersections remain; see `AUTHORING_SESSION_REPORT.md`. User acceptance remains unassessed.

The ZIP has 73 manifest entries verified against their SHA-256 hashes. Its checksum is in `SHA256SUMS.txt`.

![Open door preview](preview_open.png)
