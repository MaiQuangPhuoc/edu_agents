# Kế hoạch tích hợp 3 chức năng (Hỏi đáp, Tạo đề, Lộ trình) lên UI, chạy ổn định khi có lỗi

Cơ sở: bản mã nguồn mới nhất trên GitHub (`MaiQuangPhuoc/edu_agents`). Chú thích: **[Đã xác minh]** = đã đọc trong code; **[Đề xuất]** = thiết kế cần làm; **[Chưa xác minh]** = chưa kiểm tra.
Tài liệu chi tiết riêng cho phần Lộ trình trên UI: `src/edu_planning/UI_edu_planning.md` (nội dung chính được gộp ở mục 6 dưới đây).

## 1. Mục tiêu
1. Cả 3 chức năng chạy cùng nhau trên UI (không còn mỗi chức năng một chương trình riêng).
2. Một lỗi ở bất kỳ chỗ nào (LLM, mạng, dữ liệu, một node trong graph) **không làm dừng chương trình**; người dùng nhận thông báo rõ ràng và dùng tiếp được.
3. Lộ trình có đủ phần UI: hội thoại hồ sơ, bài test đầu vào, duyệt sườn, xem lộ trình chi tiết, nút "Tạo bài ôn tập" theo buổi.

## 2. Hiện trạng [Đã xác minh]

### 2.1 Các điểm vào hiện có

| Điểm vào | Việc | Vấn đề đã thấy |
|---|---|---|
| `main.py` (CLI menu 1/2/3) | Hỏi đáp, tạo đề, lộ trình | Chức năng 3 chỉ in "đang phát triển". Import `build_qa_graph` từ `src.edu_qa.graph` nhưng file này chỉ có `build_graph(retriever, llm_client)` (thứ tự tham số khác với cách gọi `build_qa_graph(llm_client, retriever)`). Import `src.edu_exam.run_exam` (bản cũ, không phải `run_exam_v2`). Vòng lặp không bắt lỗi nên một lỗi là thoát chương trình |
| `src/edu_qa/run_qa.py` | Chạy hỏi đáp trên console | Cùng lỗi import `build_qa_graph` như trên. Dùng collection `documents`, trong khi tạo đề và API dùng `doc_final` |
| `src/edu_exam/run_exam_v2.py` | Tạo đề trên console (vòng `input()`) | Không bắt lỗi. Có `build_initial_state()` đang được API dùng lại |
| `src/edu_planning/run_planning.py` | Lộ trình trên console (`MODE`: collect / plan / full) | Không bắt lỗi. Cuối `run_full` có gọi tạo bài ôn tập cho buổi `exam_enabled` |

### 2.2 Phía web

| Thành phần | Việc | Ghi chú |
|---|---|---|
| `src/api/` (FastAPI, cổng 8000) | `lifespan` tạo `llm_client`, `retriever` (`doc_final`), `exam_graph`, `qa_graph`. Router `chat` và `exam`, trang `pages` | **Không có router cho lộ trình.** Phiên lưu trong dict bộ nhớ (`SESSIONS_QA`, `SESSIONS_EXAM`), mất khi khởi động lại. Router không `try/except` quanh `graph.invoke`, nên lỗi graph thành HTTP 500 |
| `src/api_phuocmq/` | Biến thể của `src/api` | Cùng cách khởi tạo; `main.py` của `src/api` đang giữ phần này ở dạng comment |
| `src/edu_ui/` (FastAPI, cổng 8001) | Trang chat, đề thi, tài liệu, hồ sơ, lộ trình | Chat chuyển tiếp sang `src.api` (`EDU_QA_API_URL`); thư viện đề đọc file trong `src/test_exam`; hồ sơ dùng `StudentModel`; lộ trình chỉ **đọc file JSON** qua `EDU_UI_ROADMAPS_JSON` theo định dạng khác `LearningPath` |
| Khởi tạo graph lộ trình | `make_roadmap_graph` tự tạo `plan_client` và `guard_client` bên trong | Không có endpoint nào gọi; dùng `MemorySaver` (trong bộ nhớ) |

### 2.3 Điểm chưa nhất quán cần xử lý
- Hai tên graph hỏi đáp (`build_graph` và `build_qa_graph` trong `graph copy.py`) và hai thứ tự tham số.
- Collection: `documents` (CLI hỏi đáp) và `doc_final` (API, tạo đề, lộ trình). [Chưa xác minh] collection nào đúng cho hỏi đáp trên dữ liệu hiện tại.
- Hai bộ API/UI song song (`src/api` + `src/api_phuocmq`, và `src/edu_ui`), cùng một vài đường dẫn tĩnh.

## 3. Kiến trúc đề xuất [Đề xuất]

```
Trình duyệt ──► edu_ui (8001) ──► Backend duy nhất src/api (8000)
                                   ├─ /api/qa/...        (Hỏi đáp)
                                   ├─ /api/exam/...      (Tạo đề, bài ôn tập theo buổi)
                                   ├─ /api/planning/...  (Lộ trình)   ← MỚI
                                   └─ /api/health        (tình trạng từng chức năng)
Dùng chung: llm_client (120b), plan_client (Luna), retriever, các graph, kho phiên
```

- Giữ hai tiến trình như hiện tại (UI 8001, backend 8000) để ít thay đổi nhất; `edu_ui` thêm các route chuyển tiếp cho exam và planning giống cách chat đang làm.
- Tạo một nơi khởi tạo chung (`src/app_context.py`): hàm tạo `llm_client`, `plan_client`, `retriever`, các graph. CLI (`main.py`) và API cùng dùng, thay cho việc mỗi `run_*.py` tự tạo riêng.
- Mỗi chức năng khởi tạo **độc lập**: lỗi ở một chức năng (ví dụ thiếu khóa của Luna) chỉ làm chức năng đó "tạm ngưng", hai chức năng kia vẫn chạy. `/api/health` báo từng chức năng.

## 4. Không để lỗi làm dừng chương trình [Đề xuất]

| Tầng | Cách làm |
|---|---|
| Khởi động | Khởi tạo từng thành phần trong `try/except`; thất bại thì ghi log, đánh dấu chức năng không sẵn sàng; server vẫn lên |
| Mỗi yêu cầu API | Một hàm bọc chung quanh mọi lần gọi graph: `try/except`, giới hạn thời gian (`asyncio.wait_for`), ghi log kèm traceback, trả JSON thống nhất `{ok, message, retryable}` (không để lọt HTTP 500 trần). Xử lý lỗi toàn cục (exception handler) làm lưới cuối |
| Trạng thái phiên | Chụp bản sao trạng thái trước khi gọi graph; lỗi thì khôi phục và không ghi đè phiên. [Chưa xác minh] graph có `MemorySaver` (lộ trình): cần kiểm tra tin nhắn đã ghi vào checkpoint trước khi lỗi có bị nhân đôi khi thử lại |
| Trong graph | Bọc mỗi node bằng một hàm "an toàn": lỗi thì ghi vào `state["error"]`, thêm một tin nhắn xin lỗi và chuyển về điểm kết thúc, thay vì ném ngoại lệ. Vòng sinh lại/phê bình giữ giới hạn số lần có sẵn (ví dụ tạo đề thử lại tối đa 2 lần, critic tối đa 3 lần) |
| Gọi LLM | `invoke_structured` đã có thử lại, chuyển `json_schema` sang `function_calling` khi 400 và trả `None` khi hết lượt. Các node cần luôn kiểm tra `None` (lỗi "ellipsis" vừa rồi là một dòng chưa hoàn thiện, minh họa vì sao cần lớp bọc ở trên) |
| Việc chạy lâu (lộ trình, tạo đề) | Chạy trong `run_in_threadpool` hoặc tiến trình nền, không chặn các yêu cầu khác. UI hỏi trạng thái định kỳ (mục 5) |
| Đồng thời | Khóa theo phiên (mỗi phiên một yêu cầu tại một thời điểm); yêu cầu thứ hai trong lúc đang chạy nhận "đang xử lý" |
| CLI | Bọc từng vòng lặp trong `try/except`; in lỗi và quay lại dấu nhắc, không thoát. Sửa import `build_qa_graph`. Chức năng 3 gọi luồng lộ trình |
| Nhật ký | Ghi log ra file (có sẵn thư mục `logs/`), mỗi lỗi có mã tham chiếu hiển thị cho người dùng |
| Phía UI | Thông báo lỗi thân thiện, nút "Thử lại", giữ nguyên hội thoại và dữ liệu đã nhập; không mất phiên khi lỗi |

## 5. Giao diện lập trình (API) [Đề xuất]

Mọi phản hồi dùng một dạng chung: thành công `{ok: true, ...}`; lỗi `{ok: false, message, retryable, ref}`.

| Chức năng | Endpoint | Việc |
|---|---|---|
| Hỏi đáp | `POST /api/qa/session`, `POST /api/qa/session/{id}/message` | Đã có (đang là `/api/chat/...`); giữ tương thích, thêm bọc lỗi |
| Tạo đề | `POST /api/exam/session`, `POST /api/exam/session/{id}/message`, `GET /api/exam/{exam_id}`, `POST /api/exam/{exam_id}/submit` | Đã có; thêm bọc lỗi |
| Lộ trình | `POST /api/planning/session` (tạo phiên theo `student_id`) | Mới |
| Lộ trình | `POST /api/planning/{student_id}/message` | Mới: một lượt hội thoại (gửi `HumanMessage`); trả tin nhắn mới và `roadmap_status` |
| Lộ trình | `GET /api/planning/{student_id}/status` | Mới: trạng thái và tiến độ node đang chạy (`outline`, `plan`, `execute`, `assemble`, `critic`, `present`) |
| Lộ trình | `GET /api/planning/{student_id}/path` | Mới: trả `LearningPath` đã chuyển sang định dạng UI đọc được |
| Bài ôn tập | `POST /api/planning/{student_id}/session/{week_no}/{session_no}/exam` | Mới: kiểm tra `exam_enabled`, gọi `handle_request` (`exam_for_session`) |
| Tình trạng | `GET /api/health` | Mới: trạng thái từng chức năng (sẵn sàng / tạm ngưng) |

## 6. Phần UI của Lộ trình (edu_planning) [Đề xuất, dựa trên code đã xác minh]

### 6.1 Điểm vào graph
`make_roadmap_graph(retriever, llm_client, checkpointer=...)`; mỗi tin nhắn học sinh là một lần `graph.invoke({"messages": [HumanMessage(...)]}, {"configurable": {"thread_id": <student_id>}})`. Lần đầu truyền `student_id`; nếu đã có hồ sơ thì truyền thêm `student_model`, `model_done=True`, `entry_done=True` để bỏ qua bước hỏi hồ sơ và bài test.

### 6.2 `roadmap_status` và việc UI làm [Đã xác minh]

| Trạng thái cuối lượt | Ý nghĩa | UI hiển thị | Lượt kế tiếp |
|---|---|---|---|
| chưa có (`model_done` sai) | Đang thu thập hồ sơ | Tin nhắn bot | Học sinh trả lời tự do |
| `awaiting_test_answers` | Bài test đầu vào đã tạo | Đề (nằm trong text của tin nhắn) | Gửi đáp án dạng `1-a, 2-c, ...` |
| `entry_test_failed` | Tạo đề lỗi | Thông báo lỗi | Tin nhắn bất kỳ để thử lại |
| `awaiting_feedback` | Đã hiện sườn | Sườn dạng văn bản | "chốt", yêu cầu chỉnh, hỏi thêm, hoặc yêu cầu sửa hồ sơ |
| `updating_profile` | Planning cần cập nhật hồ sơ | Câu hỏi thu thập hồ sơ | Học sinh trả lời |
| `approved` | Đã chốt sườn | — | Graph tự chạy tiếp lộ trình chi tiết trong cùng lượt; cuối lượt là `path_ready` hoặc `path_failed` |
| `path_ready` | Lộ trình chi tiết xong | Nút "Xem lộ trình" (từ `additional_kwargs["action"]` loại `open_learning_path`) | Không cần gửi thêm |
| `path_failed` | Soạn lộ trình lỗi | Thông báo lỗi và nút thử lại | Tin nhắn bất kỳ chạy lại phần lộ trình |

Các thao tác "chốt/chỉnh" hiện là tin nhắn văn bản (LLM phân loại thành `approve_roadmap`, `revise_roadmap`, `request_profile_update`). Nút "Chốt sườn" của UI chỉ cần gửi tin nhắn "chốt".

### 6.3 Dữ liệu `LearningPath` UI cần hiển thị [Đã xác minh]
```
LearningPath
├─ current_phase, schedule {start_date, end_date, total_weeks, sessions_per_week, minutes_per_session}
├─ outline: [{phase, weeks:[{week_no, goal, lessons[], activity_types, difficulty_trend, total_hours, has_assessment}]}]
├─ weeks: [{week_no, start_date, end_date, goal, sessions:[Session]}]
└─ assumptions: [str]
Session = {date, start_time, minutes, type: lesson|review|assessment, chapter_id, lesson,
           key_points[], must_know[], must_understand[], related[], difficulty,
           activities[{type, content, minutes, difficulty, problem_type}],
           resources[{type, title, url, note}], assessment|null, exam_enabled: bool}
```
`roadmap_api.py` hiện mong đợi định dạng khác (giai đoạn → buổi với `title`, `duration_minutes`, `status`). Cần một bộ chuyển đổi (đặt ở API) hoặc sửa UI đọc thẳng `LearningPath`. Mình đề xuất đặt ở API.

### 6.4 Nút "Tạo bài ôn tập" (theo `exam_enabled`)
- Mỗi buổi có cờ `exam_enabled` (đúng/sai). Mặc định chỉ buổi đầu tiên của tuần đầu tiên là `true`. UI chỉ đọc cờ: `true` hiện nút, `false` ẩn hoặc làm mờ. Thiếu trường được coi là `false`.
- Gọi: `student_id`, `week_no`, `session_no`. API tra buổi, từ chối nếu `exam_enabled` sai; lấy `student_model` và tên môn (lộ trình không lưu môn) rồi gọi `handle_request`.
- Kết quả: `questions` (không có đáp án), `exam_id`, `key_file` (không gửi cho học sinh), `tests` (danh sách `tên đề : nguồn : link`), `tests_text`. `tests` có thể rỗng.
- Thông báo: đang tạo ("Mình đang tạo bài ôn tập cho buổi này, bạn đợi một chút nhé."); lỗi ("Mình chưa tạo được bài ôn tập, bạn thử lại nhé." và cho bấm lại); buổi chưa mở (không hiện nút).

### 6.5 Các sự kiện UI → hệ thống

| Sự kiện | Gửi gì | UI làm tiếp |
|---|---|---|
| Học sinh gõ tin nhắn | Tin nhắn vào phiên của học sinh | Hiện tin nhắn bot mới |
| Gửi đáp án test | `1-a, 2-c, ...` | Hiện kết quả chấm và sườn |
| Chốt sườn / chỉnh sườn | "chốt" hoặc yêu cầu chỉnh | Hiện trạng thái đang soạn rồi nút xem lộ trình |
| Bấm "Xem lộ trình" | `GET .../path` | Hiện lộ trình theo tuần và buổi |
| Bấm "Tạo bài ôn tập" | mục 6.4 | Hiện đề và danh sách bài tập |
| Bật/tắt kiểm tra tài nguyên bằng LLM | khóa `lp_verify` (đúng/sai) trong state lượt chạy; mặc định từ `.env` `LP_VERIFY` | Không đổi giao diện; chỉ ảnh hưởng chất lượng và thời gian soạn |
| Sửa hồ sơ ở trang Hồ sơ | `profile_api` ghi file hồ sơ | [Chưa xác minh] [Cần quyết] cách nạp lại hồ sơ vào phiên lộ trình đang chạy (checkpoint giữ `student_model` cũ) |

### 6.6 Khi chờ kết quả
Phần lộ trình chi tiết chạy lâu (nhiều lần gọi LLM và tìm kiếm). UI hiện "đang soạn", khóa nút gửi, hỏi `GET .../status` định kỳ và hiện tên bước đang chạy; có hết hạn thời gian dài và nút thử lại. [Chưa xác minh] cách lấy tiến độ theo node từ graph con (`graph.stream`, có thể cần `subgraphs=True`).

## 7. Các bước thực hiện (thứ tự đề xuất)

| # | Việc | File chính | Ghi chú |
|---|---|---|---|
| 1 | Sửa các lỗi nhất quán ở mục 2.3: thống nhất `build_graph`, thứ tự tham số, import cũ; chốt collection cho hỏi đáp | `main.py`, `run_qa.py`, `api/main.py` | Cần bạn xác nhận collection đúng (mục 8) |
| 2 | `src/app_context.py`: khởi tạo chung, tách lỗi theo chức năng, `/api/health` | mới; `src/api/main.py` | |
| 3 | Hàm bọc lỗi chung cho API và graph (mục 4) | `src/api/safe.py` (mới) | Dùng cho cả 3 router |
| 4 | Router lộ trình và tiến độ (mục 5) | `src/api/routers/planning.py` (mới) | Dùng `make_roadmap_graph`, khóa theo phiên |
| 5 | Nút tạo bài ôn tập (mục 6.4) | `src/api/routers/planning.py`, `edu_exam/exam_for_session.py` | |
| 6 | UI: chat lộ trình, hiển thị `LearningPath`, nút tạo bài ôn tập, thông báo lỗi và thử lại | `src/edu_ui/*` | Viết bộ chuyển đổi `LearningPath` (mục 6.3) |
| 7 | CLI: bọc lỗi, chức năng 3 chạy lộ trình | `main.py` | |
| 8 | Kiểm thử: tạo lỗi giả (LLM lỗi, mạng, dữ liệu hỏng) và xác nhận hệ thống không dừng; chạy cả 3 chức năng trên UI | script test | |

## 8. Cần bạn quyết trước khi làm
1. Dùng **một backend** (`src/api`) và để `src/api_phuocmq` ngừng dùng, đúng không? Nếu `src/api_phuocmq` còn cần thì mình giữ.
2. Collection cho hỏi đáp: `documents` hay `doc_final`?
3. Phiên chỉ lưu trong bộ nhớ như hiện tại (mất khi khởi động lại), hay cần lưu ra file/CSDL? Bản đầu mình đề xuất giữ trong bộ nhớ cho đơn giản.
4. Một người dùng (một `student_id`) tại một thời điểm, hay nhiều người dùng đồng thời? Điều này quyết định cách khóa phiên.

## 9. Chưa xác minh
- Chưa chạy thử toàn bộ trên UI; kế hoạch dựa trên đọc code.
- Checkpoint `MemorySaver` khi graph lỗi giữa chừng (có nhân đôi tin nhắn khi thử lại hay không).
- Tiến độ theo node của graph con.
- `src/api_phuocmq` và các trang trong `templates/` ở thư mục gốc có còn dùng không.
