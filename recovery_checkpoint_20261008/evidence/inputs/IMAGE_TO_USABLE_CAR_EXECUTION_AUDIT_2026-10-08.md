# Audit execution và ý nghĩa nghiên cứu của image-to-usable-car probe

Ngày review: 08/10/2026. Run được review: `IMAGE_TO_USABLE_CAR_PROBE_20261007_evidence.zip`.

**Kết luận:** giữ mục tiêu ảnh 2D → asset tạo sinh → asset dùng được. Run này cung cấp bằng chứng có ích về một workflow khả thi một phần, nhưng chưa đủ để quy các lỗi nhìn thấy cho generator hoặc chọn một method CVPR. Đường đã sinh mesh là **TripoSR CPU**, không phải TRELLIS.2. Có hạn chế cụ thể ở preprocessing, authoring và kiểm soát hiển thị. Chưa phát hiện lỗi gọi model nghiêm trọng trong hồ sơ đã lưu; cũng chưa thể chứng nhận inference hoàn toàn đúng về số học từ ZIP này.

**Danh tính thí nghiệm:** đây là run riêng mà người dùng vừa gửi, không phải phép thử xe đang tiến hành độc lập trong kế hoạch nghiên cứu trước. Review dùng contract của chính run này; không áp yêu cầu ảnh render Bentley hay đối chứng của một run khác.

## 1. Phạm vi đã kiểm tra

Đã đọc prompt, amendment về input, authoring intent, kế hoạch và attempt logs, source generation/cut/authoring/export/viewer, báo cáo, validation records và các ảnh trước/sau. Hai nhánh audit độc lập kiểm tra generation và authoring; root đối chiếu kết quả, source và ảnh.

Đã thực hiện kiểm tra hash/size, tái tính preprocessing từ cutout đã lưu và đọc trực tiếp dữ liệu nhị phân của raw, authored-v1 và final GLB. Không chạy lại model, U2Net, Blender hay phiên browser trong lượt audit. Ảnh đánh giá là ảnh lưu trong gói; kiểm tra quaternion/hình học/màu là phép tính mới trên GLB.

- ZIP CRC và đường dẫn giải nén hợp lệ; 169/169 mục trong manifest khớp SHA-256 và kích thước.
- 14 source snapshots khớp hash đã ghi. Điều này xác nhận tính nhất quán nội bộ, không chứng thực độc lập lịch sử thực thi hoặc mọi byte của môi trường đã chạy.
- ZIP SHA-256: `ecd681e17c180177fadfa930a341ff050239bfccd213e1628c328672ccfd89bb`.
- Raw GLB SHA-256: `5bd4ab3776084c5586201abd0d3be36416b3331cb28295d8d066ac7ac7beac3d`.
- Final GLB SHA-256: `a94dd03d1c425832c2879c242ac7dd1f571c05c308ea27fceccbfe30285853a6`.

## 2. Run thực sự đã làm gì?

Contract cho phép TRELLIS.2 **hoặc một phương án khả dụng có giải trình**. Amendment ghi trước generation rằng dùng ảnh Citroën trên cỏ 516×387 thay ảnh cũ. `original.jpg` và ảnh giải nén từ RAR trùng byte; hash khớp kế hoạch và log. Không phát hiện dấu hiệu dùng nhầm ảnh. ZIP chứa bản ghi thay input, không chứa toàn bộ hội thoại để kiểm chứng độc lập lời chấp thuận đó.

Một request TRELLIS.2 hosted bị quota chặn khoảng 0,73 giây sau khi gọi generation, trước khi có candidate. Sau đó có một candidate TripoSR CPU được ghi nhận, với source/model revision, seed 42, bốn CPU threads, marching-cubes resolution 256, chunk size 4096 và vertex colors.

Các record cho thấy một forward thành công và một lần extraction; không có dấu hiệu chọn output đẹp trong gói. Không thể chứng minh toàn bộ hoạt động ngoài gói chỉ bằng log này. Retry build dependency không phải retry generation.

Raw có 53.904 vertices và 107.608 triangles. Hash, bounds, chỉ số và số lượng khớp log; tọa độ hữu hạn, indices hợp lệ. Inference 12,64 giây + extraction 29,83 giây là thời gian máy được ghi nhận, chưa gồm setup và authoring; không phải thời gian lao động artist.

**Fallback hợp lệ theo contract. Tuy nhiên, kết quả không đo chất lượng TRELLIS.2 và không đại diện cho đường image-to-3D tốt nhất đang khả dụng.** Nếu sau này chọn nghiên cứu chất lượng–chi phí trên CPU, TripoSR có thể là một baseline liên quan; cần đặt rõ ngân sách và so sánh tương ứng.

## 3. Execution: điều gì đứng vững, điều gì cần sửa?

| Hạng mục | Kết quả audit | Giới hạn diễn giải |
|---|---|---|
| Input và resize/composite | Ảnh fitted và composite tái tính trùng pixel với file đã dùng; không thấy stretch, đảo kênh hay dùng nhầm composite của hosted route | Chưa tái chạy U2Net; không chứng nhận mask là tối ưu |
| Alpha ở preprocessing | RGB cutout đã bị nhân alpha; composite nhân alpha lần nữa, làm tối pixel bán trong suốt | Hiệu ứng đo được trên ảnh, chưa đo tác động lên mesh; không đủ giải thích mọi méo hình |
| Gọi TripoSR CPU | Code/config phù hợp snapshots upstream, output và log nhất quán | Thiếu weights/runtime/latent trong ZIP để tái lập đầy đủ hoặc kiểm tra CPU/GPU parity |
| Bảo toàn bề mặt nguồn khi cắt | Tất cả 53.904 vertices gốc còn tồn tại sau đổi hệ tọa độ; màu gốc được giữ trong sai số float | Bảo toàn source không chứng minh cut đúng ngữ nghĩa, không giao cắt hoặc appearance không đổi |
| Animation/export | GLB chứa 0/30/60° và quay về đóng; chỉ hierarchy của pivot được animate | Không chứng minh đó là một cửa xe được dựng đúng hoặc có clearance hợp lý |
| Viewer | Lỗi ánh xạ toàn clip trước đó đã sửa; source/config cuối khớp interval mở cửa | Audit này chưa chạy lại browser; kiểm tra runtime dựa vào record lưu sẵn |
| Cut/completion | Có lựa chọn authoring thô, góp phần tạo kết quả xấu | Không thể lấy thất bại của recipe này làm giới hạn của conventional authoring |
| Shading/material | RGB không bị repaint; normals và sidedness thay đổi giữa raw và authored | Chưa có kiểm tra color-space/material round-trip để quy toàn bộ màu nhạt cho generator |

### Preprocessing có hiệu ứng cụ thể, nhưng chưa có phân rã nhân quả

Từ original RGB và alpha đã lưu, RGB cutout khớp chính xác phép nhân alpha có làm tròn uint8. Caller sau đó composite RGB ấy lên nền xám bằng alpha lần nữa. So với dùng cùng mask nhưng composite một lần, chênh lệch trung bình trên pixel có alpha khác 0 là 1,10/255 mỗi kênh; 3.722 pixel có ít nhất một kênh lệch hơn 5/255, 1.115 pixel hơn 20/255.

Đây là tương tác giữa cách tạo cutout và composite, phù hợp đường upstream được lưu; không phải bằng chứng agent tự sửa sai một thuật toán CPU. Không được suy ra ảnh hưởng 3D nhỏ chỉ từ trung bình ảnh nhỏ; cũng không được dùng nó để giải thích toàn bộ lỗi xe khi chưa có ablation. Mã `naive_cutout` upstream hiện tại corroborate bước premultiply, nhưng không thay thế việc xác minh phiên bản đã cài ở run cũ. [S2]

### Source được giữ, nhưng vùng chuyển động chưa được xác nhận là đúng cửa

Phân tích độc lập GLB cho thấy:

- Sai số vị trí lớn nhất khi đối chiếu vertex gốc: khoảng `2.09e-8` đơn vị tọa độ.
- Sai số RGB lớn nhất trên vertices gốc: khoảng `2.97e-8`.
- Sai số tương đối tổng diện tích body + door source: khoảng `9.05e-10`.
- Màu ở cut vertices mới khớp nội suy trên tam giác nguồn, sai số lớn nhất khoảng `3.25e-6`.

Nhưng selection là một vùng cắt theo không gian, không phải một mask ngữ nghĩa đã kiểm tra. Bề mặt ngoài được cho chuyển động gồm **hai mảnh rời**: mảnh chính 7.264 triangles và mảnh thấp hơn 1.115 triangles. Chưa xác nhận mảnh thấp ấy thuộc cửa hay phải đứng yên. Đây là nghi vấn authoring cụ thể cần kiểm tra, không tự chứng minh mask sai chỉ vì có hai component.

Lining được tạo bằng cách dịch toàn bộ selection theo trục X vào trong, bao gồm vùng kính opaque và mảnh thấp; jamb cũng từ boundary ấy. Cabin gồm bốn hộp đơn giản. Dịch theo một trục toàn cục không tự tạo độ dày đều theo pháp tuyến trên mặt cong. Ảnh cho thấy mép cửa/kính nham nhở, bề mặt xen nhau và cabin thô. Những phần này có nguồn gốc ở cả mesh đầu vào lẫn recipe dựng thêm.

Final so với v1 chỉ thay kích thước/vị trí bốn cabin boxes; cut, pivot và các bề mặt cửa giữ nguyên. Không phát hiện sai dấu quay: rear-edge pivot và chiều quay đã chọn đưa vùng phía trước pivot ra ngoài phía camera. Hinge placement chính xác, semantic fit và clearance vẫn chưa được chứng minh.

### PASS của motion không đồng nghĩa artist acceptance

Quaternions xuất ra cho khoảng 0°, 30,000006° và 60,000004°, rồi trở về đúng quaternion đóng. Chu kỳ thực là hai giây mở + hai giây đóng, có timestamp đầu ở 1/30 giây. Viewer cuối dùng khoảng 1/30–61/30 giây cho slider 0–60°. Lỗi mapping cũ không còn là lý do bác final.

Các kiểm tra này chứng minh điều khiển và cấu trúc animation ở phạm vi đã đo. Chúng không chấm chất lượng đường cửa, kính, mặt khuất hay mức chấp nhận cho một shot CGI.

### Màu nhạt và các vệt trên mái cần đọc cẩn thận

Raw có vertex colors thật; không phải toàn bộ xe trắng do loader quên màu. Raw không có normals hay authored material. Authored thêm smooth normals và `doubleSided=true`, trong khi raw dùng culling một mặt mặc định. Báo cáo đã nói về smoothing nhưng chưa ghi rõ thay đổi sidedness. Đây là thiếu sót trong mô tả thay đổi hiển thị, không phải bằng chứng repaint giấu kín.

glTF quy định flat normals khi thiếu NORMAL và có quy tắc riêng cho sidedness/material defaults. [S1] Vì vậy cùng RGB, ánh sáng và camera vẫn chưa đồng nghĩa hai file có cùng cách shading. Chưa cô lập quy ước RGB của neural output → vertex color → PBR/tone mapping; lỗi sRGB/linear là giải thích cần kiểm tra, chưa phải bug đã xác nhận.

Méo silhouette/bánh/thân và mất chi tiết đã thấy trong raw là quan sát vững hơn việc quy toàn bộ màu nhạt hoặc terracing cho năng lực model. Chưa tách model, mask, field extraction và rendering thành các đóng góp định lượng.

## 4. Đánh giá báo cáo gốc

**Chấp nhận kết luận chính với bổ sung:** informative partial; có điều khiển cửa; chưa đạt convincing CGI target; chưa kiểm nghiệm TRELLIS.2; chưa có kết luận topology hoặc novelty.

Báo cáo gốc đã chủ động tách mechanical PASS khỏi visual failure và công khai fallback. Không có cơ sở nói agent giả báo thành công hoặc toàn bộ lượt chạy sai. Bổ sung cần thiết là double-alpha, mảnh thấp trong selection, đổi sidedness và giới hạn color attribution. Không được biến “không phát hiện lỗi gọi model nghiêm trọng” thành “output hoàn toàn phản ánh giới hạn model”.

## 5. Hướng này có đáng theo không?

**Có lý do giữ mục tiêu rộng và tiếp tục thăm dò chất lượng–chi phí.** Thành công đáng ghi nhận là từ một ảnh thật, qua một output generator, có thể tạo một asset điều khiển được bằng các thao tác hữu hạn mà giữ bề mặt/màu nguồn. Nó bổ sung bằng chứng thực hành cho mục tiêu gốc.

Nhưng ca này chưa chứng minh người dùng sẽ chấp nhận asset, còn thiếu đúng loại cấu trúc nào, hay một cải tiến kỹ thuật cụ thể sẽ vượt baseline. Lỗi cửa nhìn thấy chưa sạch khỏi lựa chọn authoring; chất lượng ảnh–mesh chưa đánh giá TRELLIS.2. Không chọn topology, completion hoặc rigging chỉ từ screenshot này.

Một cơ hội nghiên cứu không cần generator hoàn toàn bất lực. Cải thiện vừa phải nhưng lặp lại được về giữ diện mạo, độ ổn định thao tác, chất lượng ở cùng compute hoặc lượng chuẩn bị ở cùng chất lượng đều có thể đáng phát triển. Tiềm năng ở đây là một trục điều tra; chưa phải một claim về novelty hay xác suất được CVPR chấp nhận.

Ví dụ câu hỏi đáng kiểm tra, chưa phải thesis đã chọn: **khi thêm một thao tác downstream, có thể giữ tốt hơn các thuộc tính đã chấp nhận của asset, hoặc giảm công chuẩn bị ở cùng chất lượng hay không?** Để theo completion cần quan sát mới thực sự gắn với mặt lộ ra; để theo efficiency cần đo chi phí tương ứng. Không ép mọi kết quả vào câu hỏi này.

## 6. Bước tiếp theo và quan hệ với kế hoạch đang chạy

**Ngay bây giờ:** ghi nhận run này đúng là TripoSR fallback, gắn các bổ sung audit vào handoff và giữ completed bounded probe. Không tiếp tục sửa chiếc xe này đến khi đẹp để rồi gọi chuỗi sửa ấy là method discovery.

Nếu cần truy nguyên lỗi hình ảnh của chính candidate này trước khi dùng làm witness, chỉ cần một đối chứng nhỏ trên saved asset ở executor gốc:

1. Giữ camera/lighting cố định; render source surfaces sau cut với các phần thêm được tắt, rồi bật lining/jamb/cabin. Ghi rõ những gì đổi. Dùng thiết lập normals/culling phù hợp để tách ảnh hưởng của việc chia mesh và vật liệu; không trừ một scalar error rồi gọi là causal decomposition.
2. Kiểm tra trực tiếp mảnh thấp được chọn có đúng thuộc cửa. Chỉ sửa selection nếu bằng chứng cho thấy sai, lưu trước/sau. Không mở một chiến dịch repair.
3. Chỉ kiểm tra color transfer hoặc chạy đối chứng alpha nếu kết luận sắp dùng phụ thuộc vào màu/biên mask. Không yêu cầu mọi diagnostic này như gate trước khi được thử ý tưởng.

Đây là sửa phép đo và kiểm tra implementation, chưa phải dự án method. Audit hiện tại đã đủ để bác việc dùng final screenshot làm bằng chứng thuần về generator; không cần chờ các đối chứng này để sửa diễn giải đó.

**Với chương trình nghiên cứu:** giữ phép thử revision trên asset ngoài xe theo kế hoạch trước và giữ run xe đang tiến hành độc lập theo contract riêng. Gói vừa review không thay thế hoặc hoàn thành run xe ấy. Khi kết quả kia về, đọc đúng nguồn/task trước khi dùng để thay đổi ưu tiên; không gộp hai run thành một test.

Nếu sau đó vẫn cần trả lời riêng “TRELLIS.2 với ảnh này làm được gì?”, phải có một follow-up chạy thành công đúng TRELLIS.2, giữ nguyên provenance/input và cấu hình được ghi trước. Đây là phép thử mới, không phải lặp ngầm trong budget one-candidate đã hoàn tất. Nếu resource/quota vẫn chặn, ghi blocker; không dùng fallback để trả lời claim riêng về TRELLIS.2. Chưa có lý do mở thêm một job xe ngay trong lượt audit này.

Chưa cần Deep Research/Elicit rộng. Thông tin đang thiếu trước hết là phân biệt tác động của stage và hiệu quả của một can thiệp cụ thể. Khi có một dự đoán kỹ thuật cần đầu tư, dùng tìm kiếm hẹp để đối chiếu đúng baseline/cơ chế gần nhất.

| Quan sát tiếp theo | Quyết định phù hợp |
|---|---|
| Tắt/sửa geometry thêm làm biến mất lỗi chính | Xử lý như authoring/implementation; không gọi là giới hạn generator |
| Ordinary preparation đạt chất lượng với công ít | Thu hẹp nhu cầu của ca này; vẫn có thể xem efficiency/robustness nếu có dữ liệu |
| Có công chuẩn bị hoặc đánh đổi chất lượng rõ, một can thiệp nhỏ cải thiện được | Phát triển prototype và thử ngoài ca đã dùng thiết kế, với đối chứng công bằng |
| Lỗi chỉ có ở candidate/fallback hiện tại | Giữ làm baseline knowledge; chưa đẩy thành thesis tổng quát |
| Có cải thiện khiêm tốn nhưng ổn định trên trade-off có ích | Không loại vì “gap nhỏ”; tăng kiểm chứng theo phạm vi claim và mức đầu tư |

Điều kiện nâng thành thread nghiêm túc là có hậu quả downstream rõ, một giải thích hoặc can thiệp có dự đoán, so sánh liên quan và tín hiệu ngoài ca phát triển. Không cần chứng minh mọi cách thông thường đều thất bại trước khi thử prototype; cũng không được dùng sự vụng của một recipe làm bằng chứng thay thế.

## 7. Chỉ mục bằng chứng

Các đường dẫn dưới đây là đường dẫn bên trong ZIP nguồn.

| Claim | File quyết định |
|---|---|
| Contract và thay input | `inputs/CODEX_IMAGE_TO_USABLE_CAR_PROBE_2026-10-06.md`; `config/AUTHORING_INTENT.md`; `inputs/original.jpg`; `inputs/archive-manifest.json` |
| TRELLIS bị quota; TripoSR thực thi | `raw/hosted-attempt001/attempt.json`; `raw/cpu-attempt001/attempt.json`; `source/cpu_attempt.py`; `config/generation-plan.json` |
| Preprocessing | `inputs/cpu_cutout.png`; `inputs/cpu_fitted_rgba.png`; `inputs/cpu_preprocessed.png`; `research/cpu_route_review/run.py`; `research/cpu_route_review/tsr__utils.py` |
| Cut/completion/pivot | `source/cut_door.py`; `source/author_car.py`; `config/door-authoring.json`; `artifacts/car_authored.glb` |
| Hình ảnh trước/sau | `source/viewer/verification/final/raw_hero.png`; `raw_side.png`; `authored_comparison_closed.png`; `authored_open_side.png` trong cùng thư mục; `artifacts/authored-inspection/open_exposed.png` |
| Mechanical checks và viewer | `logs/authored-reopen-validation.json`; `source/viewer/config.json`; `source/viewer/src/main.js`; `source/viewer/verification/final/` |
| Kết luận của executor và giới hạn gói | `IMAGE_TO_USABLE_CAR_REPORT.md`; `RESUME.md`; `source/package_evidence.py` |

Nguồn sơ cấp ngoài gói dùng để kiểm tra hẹp, không phải một survey mới:

- **S1:** [Khronos glTF 2.0 specification](https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/Specification.adoc), phần primitive data, materials và sidedness.
- **S2:** [rembg upstream `bg.py`](https://github.com/danielgatis/rembg/blob/main/rembg/bg.py), `naive_cutout`; source hiện tại chỉ corroborate cơ chế, không chứng thực byte của runtime cũ.

**Giới hạn cuối:** thiếu checkpoint, runtime đầy đủ và cached neural codes trong ZIP; không tái lập inference/Chamfer hay benchmark SOTA. Kết luận chắc nhất là tính nhất quán của artifact, sự hoạt động của motion và sự hiện diện của nhiều nguồn ảnh hưởng trong final. Chưa có đảm bảo tuyệt đối rằng output không chịu ảnh hưởng execution.
