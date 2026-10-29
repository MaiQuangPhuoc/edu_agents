# UI ↔ edu_planning: khi nào UI tác động và tác động gì

Phạm vi: Adaptive Learning Roadmap (`src/edu_planning/`). Mục **[Đã có]** là đã đọc trong code; mục **[Đề xuất]** là thiết kế cần làm, chưa tồn tại; mục **[Chưa xác minh]** là chưa kiểm tra.

## 1. Hiện trạng UI (`src/edu_ui/`) [Đã có]

| Thành phần | Việc hiện làm | Liên hệ với edu_planning |
|---|---|---|
| `profile_api.py` (`/api/ui/students/...`) | Đọc/ghi hồ sơ học sinh bằng `StudentModel` vào `store/student/<student_id>.json` (cùng thư mục `student_store.STUDENT_DIR`) | Dùng chung schema và file với planning |
| `roadmap_api.py` (`GET /api/ui/roadmaps`) | Chỉ đọc file JSON do biến `EDU_UI_ROADMAPS_JSON` trỏ tới. Định dạng mong đợi: `roadmaps[].phases[].sessions[]` với `title`, `duration_minutes`, `status` | **Chưa nối** với lộ trình planning. Định dạng khác với `LearningPath` (mục 5) |
| `static/js/roadmap.js` | Hiển thị lộ trình → giai đoạn → buổi học, trạng thái `completed` hoặc chưa | Chưa có chat, chưa gọi graph |
| Chat với graph | Không có endpoint nào gọi `make_roadmap_graph` (đã tìm trong `api`, `api_phuocmq`, `edu_ui`) | Toàn bộ luồng hội thoại hiện chỉ chạy qua `run_planning.py` (console) |

## 2. Điểm vào của graph [Đã có]
- Tạo graph: `make_roadmap_graph(retriever, llm_client, checkpointer=...)` (`roadmap_graph.py`).
- Mỗi tin nhắn học sinh = một lần `graph.invoke({"messages": [HumanMessage(...)]}, {"configurable": {"thread_id": <student_id>}})`. Cần checkpointer (ví dụ `MemorySaver` như `run_planning.py`) để giữ trạng thái giữa các lượt.
- Lần đầu truyền thêm `student_id`. Nếu đã có hồ sơ thì có thể truyền `student_model`, `model_done=True`, `entry_done=True` để bỏ qua bước hỏi hồ sơ và bài test (cách `MODE="plan"` đang dùng).
- Kết quả: danh sách `messages` mới (phần `AIMessage` sau tin nhắn học sinh cuối) và các khóa trạng thái, quan trọng nhất là `roadmap_status`.

## 3. Trạng thái `roadmap_status` và việc UI cần làm [Đã có]

| `roadmap_status` (khi kết thúc một lượt) | Ý nghĩa | UI hiển thị | Lượt kế tiếp của UI |
|---|---|---|---|
| (chưa có), `model_done` sai | Đang thu thập hồ sơ (`collect`) | Tin nhắn của bot | Học sinh trả lời tự do |
| `awaiting_test_answers` | Đã tạo bài test đầu vào (`entry_test`), chờ đáp án | Nội dung đề nằm trong text của `AIMessage` (không có dữ liệu cấu trúc) | Học sinh gửi đáp án dạng `1-a, 2-c, ...`. Guard bỏ qua lọc ở trạng thái này |
| `entry_test_failed` | Tạo đề lỗi | Thông báo lỗi và gợi ý nhắn "thử lại" | Bất kỳ tin nhắn nào sẽ chạy lại `entry_test` |
| `awaiting_feedback` | Đã hiện sườn lộ trình (`planning`), chờ phản hồi | Sườn dạng text | Học sinh chọn: chốt, yêu cầu chỉnh, hỏi thêm, hoặc yêu cầu sửa hồ sơ |
| `revising` | Đang sinh lại sườn (trạng thái trung gian) | — | Thường không thấy ở cuối lượt |
| `updating_profile` | Planning cần cập nhật hồ sơ trước khi chỉnh sườn | Câu hỏi của `collect` | Học sinh trả lời; sau đó graph quay lại planning (`profile_changed`) |
| `approved` | Học sinh đã chốt sườn | — | Trong cùng lượt, graph tự chạy `learning_path`, nên cuối lượt thường là `path_ready` hoặc `path_failed` |
| `path_ready` | Đã soạn xong lộ trình chi tiết | Tin nhắn có nút "Xem lộ trình" (xem mục 4) | Không cần gửi thêm; graph kết thúc ở trạng thái này |
| `path_failed` | Soạn lộ trình lỗi | Thông báo lỗi | Bất kỳ tin nhắn nào (ví dụ "thử lại") sẽ chạy lại `learning_path` |

Ghi chú: nút hoặc thao tác của UI (chốt, chỉnh) hiện không phải lệnh cấu trúc. Chúng là tin nhắn văn bản mà LLM `handle_feedback` phân loại thành `approve_roadmap`, `revise_roadmap`, `request_profile_update` hoặc trả lời thường. [Đề xuất] nếu UI muốn nút "Chốt sườn", nút chỉ cần gửi tin nhắn "chốt".

## 4. Các sự kiện UI → hệ thống

| Sự kiện từ UI | Gửi gì | Hệ thống làm | UI làm sau đó |
|---|---|---|---|
| Học sinh gõ tin nhắn | `HumanMessage` vào thread của học sinh | Chạy guard → bước tương ứng trạng thái. Guard có thể từ chối tin ngoài chủ đề (trả `tra_loi`) | Hiện `AIMessage` mới |
| Gửi đáp án bài test | Tin nhắn `1-a, 2-c, ...` | `entry_grade` chấm, cập nhật hồ sơ (`nang_luc`), rồi sang planning | Hiện kết quả chấm và sườn |
| Chốt sườn | Tin nhắn "chốt" (hoặc tương đương) | `approve_roadmap` → `learning_path` chạy liền (lâu, nhiều lần gọi LLM) | Hiện trạng thái đang soạn, sau đó nút xem lộ trình |
| Yêu cầu chỉnh sườn | Tin nhắn mô tả yêu cầu | Sinh lại sườn (tối đa `MAX_REVISION` lần, sau đó bot nhắc chốt) | Hiện sườn mới |
| Bấm "Xem lộ trình" | `AIMessage.additional_kwargs["action"]` = `{"type": "open_learning_path", "student_id", "file"}` | `present_node` đã lưu `store/learning_path/<student_id>.json` và `.md` | [Đề xuất] UI gọi API đọc lộ trình theo `student_id` (không đọc `file` trực tiếp vì đó là đường dẫn trên máy chủ) |
| Bật/tắt kiểm tra tài nguyên bằng LLM | Khóa `lp_verify` (đúng/sai) trong state của graph | `lp_resources` kiểm tài nguyên bằng LLM nếu bật. Mặc định lấy từ `.env`: `LP_VERIFY=true`. Kiểm bằng code luôn chạy | [Chưa xác minh] cách UI truyền khóa vào state của lượt chạy |
| Học sinh sửa hồ sơ trong trang Hồ sơ | `profile_api` ghi `store/student/<id>.json` | Lượt graph đang có trạng thái trong checkpointer vẫn giữ `student_model` cũ | [Chưa xác minh] [Cần quyết] nạp lại hồ sơ vào thread sau khi sửa như thế nào |
| Bấm "Tạo bài ôn tập" ở một buổi (chỉ khi `exam_enabled` = true) | Mục 9: `student_id`, `week_no`, `session_no` | Tạo bài ôn tập cho đúng bài của buổi, kèm danh sách bài tập tìm được | Hiện đề và danh sách bài tập (mục 9) |
| Đánh dấu hoàn thành buổi học | — | Hiện **chưa có** thành phần nào ghi tiến độ. `Session` không có trường `status` | [Đề xuất] làm cùng Progress Agent (chưa làm) |

## 5. Dữ liệu lộ trình UI cần hiển thị (`LearningPath`, `state_plan.py`) [Đã có]

```
LearningPath
├─ current_phase: int
├─ schedule: {start_date, end_date, total_weeks, sessions_per_week, minutes_per_session}
├─ outline: [{phase, weeks: [{week_no, goal, lessons[{chapter_id, lesson}], activity_types,
│             difficulty_trend, total_hours, has_assessment}]}]     # tuần mức vừa của mọi giai đoạn
├─ weeks: [ Week ]            # tuần chi tiết của giai đoạn hiện tại
└─ assumptions: [str]         # cảnh báo, ví dụ "Thiếu dữ liệu: ...", "chỉ xếp được 2/3 buổi ..."

Week     = {week_no, start_date, end_date, goal, sessions: [Session]}
Session  = {date, start_time, minutes, type: lesson|review|assessment, chapter_id, lesson,
            key_points[], must_know[], must_understand[], related[], difficulty,
            activities: [{type: lecture|reading|video|exercise|summary|review, content, minutes,
                          difficulty, problem_type}],
            resources: [{type: document|video|curriculum, title, url, note}],
            assessment: {chapter_ids, num_questions} | null,
            exam_enabled: bool}      # true: UI hiện nút "Tạo bài ôn tập"; mặc định chỉ buổi đầu tiên là true
```

Khác biệt với định dạng `roadmap_api` đang mong đợi (`phases[].sessions[]` với `title`, `duration_minutes`, `status`):
- Lộ trình của planning chia theo **tuần**, mỗi buổi có ngày và giờ cụ thể.
- Không có `title` (dùng `lesson`), không có `duration_minutes` (dùng `minutes`), không có `status`.
- [Cần quyết] đặt bộ chuyển đổi ở API (`roadmap_api`) hay sửa UI đọc thẳng `LearningPath`. [Đề xuất] đặt ở API để UI không phụ thuộc schema nội bộ.

## 6. Lưu ý khi UI chờ kết quả
- Một lượt `invoke` chạy `learning_path` là lệnh chặn, có thể mất lâu (nhiều lần gọi LLM và tìm kiếm). UI cần trạng thái "đang soạn" và đặt timeout hợp lý. [Đề xuất] dùng `graph.stream` để hiện tiến độ theo node (`outline`, `plan`, `execute`, `assemble`, `critic`, `present`). [Chưa xác minh] chế độ stream với graph con.
- Lượt cần học sinh trả lời (`awaiting_*`, `updating_profile`, hỏi hồ sơ) trả về nhanh.
- Terminal in chi tiết từng bước khi `LP_DEBUG` khác `0` (chỉ để debug; UI không đọc).
- Nếu cần chạy lại `learning_path`: gửi tin nhắn bất kỳ khi `roadmap_status == "path_failed"`.

## 7. Việc cần làm phía UI và API [Đề xuất, chưa làm]
1. Endpoint chat gọi `make_roadmap_graph` (giữ graph và checkpointer sống cùng tiến trình; `thread_id = student_id`).
2. Endpoint đọc lộ trình theo `student_id` từ `store/learning_path/<student_id>.json` và chuyển sang định dạng UI (mục 5).
3. Hiển thị nút từ `additional_kwargs["action"]` (loại `open_learning_path`).
4. Nút bật/tắt `lp_verify` và cách đưa vào state.
5. Quyết định cách nạp lại hồ sơ khi học sinh sửa ở trang Hồ sơ.
6. Tiến độ buổi học (`status`): làm cùng Progress Agent sau.
7. Nút "Tạo bài ôn tập" và endpoint tương ứng (mục 9).

## 8. Lỗi cần sửa trước khi nối UI
`roadmap_graph.py` gọi `make_learning_path_graph(retriever, llm_client)` mà **không truyền `plan_client`**. Hệ quả: `outline`, `knowledge` và `assemble` của lộ trình chi tiết chạy bằng `llm_client` (gpt-oss-120b) thay vì Luna. Cần truyền `plan_client=plan_client` (biến đã có ngay phía trên trong cùng hàm).

## 9. Bài ôn tập theo buổi học (nút "Tạo bài ôn tập")

### 9.1 Cờ `exam_enabled` [Đã có]
- Mỗi buổi (`Session`) trong `LearningPath` có trường `exam_enabled` (đúng/sai), do `present_node` đặt khi lưu lộ trình.
- **Mặc định chỉ một buổi là `true`: buổi đầu tiên của tuần đầu tiên.** Các buổi còn lại là `false`.
- Quy tắc cho UI: `true` thì hiện nút "Tạo bài ôn tập"; `false` thì ẩn hoặc làm mờ. UI không tự suy luận, chỉ đọc cờ.
- Cờ nằm trong file `store/learning_path/<student_id>.json`. Lộ trình cũ sinh trước thay đổi này không có trường này; UI coi thiếu trường là `false`.
- [Cần quyết] sau này bật cờ cho buổi nào (ví dụ buổi vừa học xong, hoặc mọi buổi đã qua ngày học) và ai ghi cờ. Hiện chỉ có mặc định ở trên.

### 9.2 Gọi tạo bài ôn tập [Đề xuất, chưa có endpoint]
- Yêu cầu từ UI: `student_id`, `week_no`, `session_no` (thứ tự buổi trong tuần, bắt đầu từ 1).
- API tra buổi trong file lộ trình. Từ chối nếu buổi không tồn tại hoặc `exam_enabled` là `false`.
- API gọi `handle_request` (`src/edu_exam/exam_for_session.py`) với `payload`: `student_model` (đọc từ `store/student/<student_id>.json`), `subject` (tên môn, ví dụ "Toán 10"; lộ trình không lưu môn nên API phải lấy từ hồ sơ) và `session`.
- Việc này chạy lâu (nhiều lần gọi LLM). UI hiện trạng thái "đang tạo đề" và khóa nút trong lúc chờ.

### 9.3 Kết quả trả về (`payload` của `handle_request`) [Đã có]

| Trường | Ý nghĩa | UI làm |
|---|---|---|
| `ok` | Đúng/sai | Sai thì hiện `error` (mục 9.4) |
| `questions` | Danh sách `{no, chapter_id, question, options{A,B,C,D}}`, không có đáp án | Hiện đề cho học sinh làm |
| `key_file` | Đường dẫn file đáp án trên máy chủ (có thể rỗng) | Không đọc trực tiếp; không gửi cho học sinh |
| `exam_id` | Mã đề | Dùng để nhận diện đề |
| `tests` | Danh sách bài tập tìm được: `{title, source, url}` | Hiện thành danh sách "Các bài tập theo chủ đề bạn có thể ôn tập": `tên đề : nguồn : link`, link mở ở tab mới |
| `tests_text` | Cùng nội dung `tests` dạng văn bản | Dùng khi chỉ cần hiện chữ (ví dụ trong khung chat) |

`tests` có thể rỗng (không tìm được). Khi đó UI chỉ hiện đề, không hiện mục bài tập.

### 9.4 Thông báo cho học sinh

| Tình huống | Nội dung gợi ý |
|---|---|
| Đang tạo | "Mình đang tạo bài ôn tập cho buổi này, bạn đợi một chút nhé." |
| Thành công | Hiện đề, rồi mục "Các bài tập theo chủ đề bạn có thể ôn tập" (nếu có) |
| `ok` sai | "Mình chưa tạo được bài ôn tập (`error`). Bạn thử lại nhé." và cho bấm lại nút |
| Buổi có `exam_enabled` = false | Không hiện nút. Nếu gọi API trực tiếp thì trả lỗi 4xx với thông báo "Buổi này chưa mở bài ôn tập" |

### 9.5 Chưa xác minh
- Chưa chạy `handle_request` với dữ liệu và LLM thật (chỉ test bằng LLM giả).
- Chưa kiểm tra kích thước phản hồi và thời gian tạo đề; UI nên đặt timeout dài.
- Cách chấm bài ôn tập khi học sinh làm xong chưa có (chưa quyết).
