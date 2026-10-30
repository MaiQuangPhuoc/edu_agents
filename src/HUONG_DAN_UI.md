# Bộ tích hợp UI EDUAGENT

Bộ này chứa các file mới và file thay thế, giữ nguyên đường dẫn từ `src/`. Được đối chiếu với commit `1adb36b6ee0050492c12b86744936b55fe1ba18c` của `MaiQuangPhuoc/edu_agents`.

## Cách áp dụng

1. Dừng UI đang chạy.
2. Chép **nội dung thư mục `src` của bộ này** vào `EDUAGENT/src`, ghi đè những file trùng tên. Giữ các file khác của dự án. Đây là bản cập nhật bổ sung, không phải toàn bộ repo để chạy độc lập.
3. Chép đủ các file ngoài `edu_ui` được liệt kê bên dưới. Chỉ thay `main.py` sẽ thiếu dữ liệu câu hỏi đầu vào, nút xác nhận và trường cấu hình trong state.
4. Giữ `.env` ở **EDUAGENT/.env**, cùng cấp `src`. Không cần đổi các API key hay model đã chạy ổn.
5. Trong terminal tại thư mục EDUAGENT, kích hoạt môi trường Python đang dùng, rồi chạy:

```powershell
python -m uvicorn src.edu_ui.main:app --host 127.0.0.1 --port 8001
```

Mở **http://127.0.0.1:8001**, nhấn **Ctrl+F5** để tải lại JavaScript/CSS. Luồng chat mới gọi trực tiếp các graph; không cần chạy thêm `src.api.main` ở cổng 8000. Endpoint proxy cũ `/api/ui/chat` vẫn được giữ để tương thích, nhưng chat UI mới không dùng nó.

Dùng **một worker**. Không bật tự reload khi đang sinh đề/lộ trình: phiên graph và tác vụ nền hiện ở bộ nhớ tiến trình. Khởi động lại server làm hết hạn phiên; UI báo hết hạn, không tự giả tạo lại tiến độ.

## Học sinh và dữ liệu đã lưu

Để thống nhất chat, trang hồ sơ, bài kiểm tra và lộ trình, mã học sinh lấy từ biến tùy chọn trong `.env`:

```dotenv
EDU_UI_STUDENT_ID=hs_006
```

Nếu không đặt, dùng `hs_002`, tương thích mã mặc định UI trước đây. Khởi động lại sau khi thay đổi biến này. Đây là UI chạy cục bộ cho một học sinh được cấu hình; bộ này chưa bổ sung đăng nhập và phân quyền cho nhiều người dùng.

Trang **Lộ trình học** đọc JSON qua `path_store`, mặc định `store/learning_path/<student_id>.json`. File mới lưu thêm `subject` từ cửa sổ lộ trình hiện tại. File cũ thiếu trường môn vẫn xem được nội dung; không tự đoán môn từ phần tử đầu tiên trong hồ sơ để tạo bài ôn tập.

## Các luồng đã nối

| Luồng | Tương tác UI | Nội dung gửi backend |
| :-- | :-- | :-- |
| Chọn chức năng | Dấu `+`, nhãn trong ô nhập, nút `×` | Phiên riêng `qa`, `exam`, `planning` |
| QA | Markdown, công thức KaTeX, nguồn thực tế, nút gợi ý | Nguyên văn câu hỏi được chọn |
| Tạo đề: thu thập | Nút xác nhận khi đủ dữ liệu đang chờ xác nhận | `xác nhận đúng` |
| Tạo đề: quan tâm | Chọn 0–3 theo đúng thứ tự section từ curriculum | Ví dụ `3,1,2,0` |
| Tạo đề: ma trận | Tổng số câu, độ khó, bảng chương, chi tiết chủ đề | Nút xác nhận gửi `ok` |
| Tạo đề: hoàn tất | Nút Xem đề mở đúng đề vừa tạo | Đề được xuất vào `src/test_exam` với tiền tố môn |
| Planning: thu thập | Nút xác nhận hồ sơ | `xác nhận đúng` |
| Planning: đầu vào | Trang trắc nghiệm 2×2, lưu lựa chọn, điều hướng câu | Ví dụ `1-A, 2-B`, gửi đúng phiên đang chờ |
| Planning: sườn | Markdown của sườn, nút xác nhận hoặc góp ý bằng tin nhắn | Nút xác nhận gửi `chốt` |
| Planning: chi tiết | Tuần, buổi, hoạt động, kiến thức và tài nguyên | Đọc dữ liệu LearningPath thực |
| Ôn tập theo buổi | Tạo bài ôn tập nếu `exam_enabled=true` | Backend kiểm tra lại cờ trước khi chạy |
| Kiểm tra tài nguyên | Checkbox trong chế độ Planning | `lp_verify` cho lượt xử lý tiếp theo |
| PDF | Nút Tải PDF lộ trình | Mở hộp thoại in, chọn **Lưu dưới dạng PDF** |

Bài kiểm tra **đầu vào Planning yêu cầu trả lời đủ tất cả câu** để giữ nguyên hợp đồng của `entry_grade`. Quy tắc bỏ trống sau ba lần nhắc của trang làm đề thông thường không áp dụng vào bài đầu vào.

Tiến trình dựa trên callback node/tool thực sự được gọi. UI không in prompt, thông tin API key hoặc suy luận nội bộ. Các tác vụ được xếp hàng trong tiến trình này để tránh những bộ sinh đề hiện có ghi đồng thời vào cache/file chung. Bấm xác nhận lặp được chặn bằng phiên bản state; gửi lại cùng `request_id` nhận lại tác vụ cũ.

## Kiểm tra đã thực hiện

- 10 kiểm tra backend: phiên riêng, tác vụ nền, chống gửi trùng, phiên bản cũ, câu trả lời đầu vào, không lộ đáp án, chặn bài ôn tập bị tắt, callback LangGraph thực, xử lý lỗi và khôi phục xác nhận sau khi lộ trình đã hoàn tất.
- Kiểm tra trình duyệt Chromium với API mô phỏng: công thức, Markdown được làm sạch, gợi ý click, đổi nhánh, select chủ đề, ma trận, nút cũ, bài đầu vào, lộ trình JSON và màn hình điện thoại.
- Mô phỏng mất phản hồi POST: tải lại trang gửi lại đúng request_id, nhận cùng tác vụ và khôi phục câu trả lời.
- Kiểm tra cú pháp Python/JavaScript.

**Chưa chạy gọi LLM, Tavily, YouTube hoặc Qdrant thật trong bộ kiểm tra này.** Các bài kiểm tra dùng graph/response mô phỏng; cần chạy thử một phiên QA, một phiên tạo đề và một phiên Planning bằng cấu hình thật trên máy bạn. Không tuyên bố đã đo tốc độ hay chất lượng model.

Có thể chạy kiểm tra backend sau khi chép file test vào `tests/` của dự án:

```powershell
python -m pytest tests/test_workflow_ui.py -q
```

Các thư viện UI mới dùng đúng bộ Marked, DOMPurify và KaTeX đã có ở trang làm bài test, tải qua CDN. Nếu CDN không tải được, nội dung vẫn hiển thị dưới dạng văn bản và có thông báo. Các agent/graph vẫn cần đầy đủ dependency của repo đang chạy.

## Danh sách file tải xuống

Các đường dẫn dưới đây tương ứng vị trí cần đặt trong EDUAGENT. File đã có thì thay thế; file chưa có thì tạo mới.

- [src/edu_exam/collect_info_v2.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_exam/collect_info_v2.py)
- [src/edu_planning/collect_student_model.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_planning/collect_student_model.py)
- [src/edu_planning/entry_test.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_planning/entry_test.py)
- [src/edu_planning/learning_path_graph.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_planning/learning_path_graph.py)
- [src/edu_ui/main.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/main.py)
- [src/edu_ui/static/css/workflow.css](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/static/css/workflow.css)
- [src/edu_ui/static/js/chat.js](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/static/js/chat.js)
- [src/edu_ui/static/js/exams.js](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/static/js/exams.js)
- [src/edu_ui/static/js/profile.js](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/static/js/profile.js)
- [src/edu_ui/static/js/study.js](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/static/js/study.js)
- [src/edu_ui/static/js/workflow.js](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/static/js/workflow.js)
- [src/edu_ui/templates/chat.html](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/templates/chat.html)
- [src/edu_ui/templates/study.html](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/templates/study.html)
- [src/edu_ui/workflow_api.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/workflow_api.py)
- [src/edu_ui/workflow_engine.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/workflow_engine.py)
- [src/edu_ui/workflow_view.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/edu_ui/workflow_view.py)
- [src/state_plan.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/src/state_plan.py)

- [tests/test_workflow_ui.py](sandbox:/workspace/scratch/96e6c1939aed/ui_integration/tests/test_workflow_ui.py) — chỉ dùng kiểm tra, không cần để chạy UI.
