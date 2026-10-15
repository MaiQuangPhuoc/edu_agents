# Chức năng Lộ trình học cá nhân hóa (EDUAGENT)

## 1. Mục tiêu
Xây dựng lộ trình học thích nghi cho học sinh lớp 10 (Toán, Ngữ văn, Lịch sử): thu thập hồ sơ, lập sườn lộ trình, soạn kế hoạch chi tiết cho giai đoạn đang học, sau đó theo dõi và cập nhật khi học sinh tiến bộ hoặc đổi thông tin.

## 2. Kiến trúc tổng thể

| Agent | Vai trò | Trạng thái |
|---|---|---|
| Collect (Student Model) | Hỏi và lưu hồ sơ học sinh | Đã viết code, chưa chạy thành công |
| Planning | Lập sườn lộ trình (các giai đoạn lớn), nhận góp ý | Đã viết code, chưa chạy thành công |
| Learning Path | Soạn kế hoạch chi tiết theo tuần/buổi cho giai đoạn hiện tại | Đã có schema, prompt, 3 tool; **chưa có graph** |
| Progress | Theo dõi tiến độ, kích hoạt lập lại kế hoạch | Chưa làm |
| Report | Báo cáo cho học sinh và phụ huynh | Chưa làm |

- Trong chức năng này các agent chuyển việc cho nhau qua **state dùng chung (LangGraph)**, cờ `roadmap_status` quyết định agent nào chạy tiếp. Không dùng A2A chuẩn.
- **A2A chuẩn** chỉ dùng ở lớp ngoài cùng, giữa các chức năng lớn (hỏi đáp `edu_qa`, tạo bài test `edu_exam`, lộ trình).
- Nguyên tắc: phần cần chính xác (tính toán, kiểm tra hợp lệ) do code/tool làm; phần cần linh hoạt do agent quyết.

## 3. Luồng tổng (graph `roadmap_graph.py`)

```
START → guard ─ không hợp lệ → trả lời lịch sự, dừng
          ├─ chưa có hồ sơ / đang cập nhật hồ sơ → collect
          ├─ đã có hồ sơ, chưa có sườn → planning
          └─ chờ góp ý → planning (handle_feedback)
collect xong → planning
planning → trình bày sườn → chờ học sinh → (chốt | giải thích | sửa sườn | đổi hồ sơ → collect → planning)
```

Các giá trị `roadmap_status`: `draft`, `awaiting_feedback`, `revising`, `updating_profile`, `profile_changed`, `approved`.

## 4. Agent thu thập hồ sơ (Collect)
- Mỗi lượt gọi `invoke_structured` một lần (schema `CollectTurn`: hồ sơ cập nhật, tin nhắn, cờ hoàn tất).
- Trường bắt buộc: môn, mục tiêu (điểm + thời hạn), ưu tiên (điểm số/hiểu bản chất), lịch học (số buổi/tuần, khung giờ rảnh, thời lượng buổi), năng lực (điểm mạnh yếu bằng lời).
- Khuyến khích: sở thích học (tài liệu/video/bài tập/tóm tắt), dạng bài trọng tâm, sở thích cá nhân, lịch bận.
- Chế độ cập nhật: khi học sinh đổi thông tin, chỉ hỏi và thay đúng nhóm trường cần đổi (`ProfilePatch`), nhóm khác giữ nguyên.
- Khi hồ sơ được xác nhận: lưu `data/students/<id>.json` và tạo `search_queries` (truy vấn viết lại, tách ý) cho Planning.
- `guard` đặt ở cửa vào graph: lọc nội dung vô nghĩa, bạo lực, nhạy cảm, lạc đề (không phạt, trả lời lịch sự; nếu học sinh có dấu hiệu khó khăn thì trả lời quan tâm).
- Bài test đầu vào chưa có: trường `da_test_dau_vao` tạm đặt `True`.

## 5. Planning Agent (sườn lộ trình)
- **planner**: ReAct (`create_agent`) với tool tra cứu, tối đa 10 lượt.
  - `search_documents` (chỉ retrieve), `search_documents_reranked` (retrieve + rerank), `search_web_documents` (Tavily, domain giáo dục), `search_videos` (YouTube).
- **finalize**: `invoke_structured` ra `MasterRoadmap` (giai đoạn, chương/bài, lý do, tiêu chí hoàn thành, gợi ý tài nguyên, giả định). Tài nguyên có url không xuất hiện trong kết quả tra cứu bị loại.
- **present_roadmap**: gửi sườn cho học sinh, dừng chờ.
- **handle_feedback**: LLM chọn đúng một hướng:
  - `approve_roadmap`: chốt.
  - `revise_roadmap`: sửa sườn (chỉ chạy lại `finalize`, tối đa 3 lần).
  - `request_profile_update`: sang Collect cập nhật; sau đó `planner` chạy lại từ đầu, prompt mang theo sườn cũ và danh sách thông tin đã đổi (tính bằng code).
  - `reply_to_student`: giải thích hoặc hỏi lại khi góp ý mơ hồ.
- Dùng checkpointer (`MemorySaver` khi thử) để giữ state giữa các lượt.

## 6. Learning Path Agent (kế hoạch chi tiết)

### Đầu vào và phạm vi
- Đầu vào: `student_model` và `master_roadmap` (chỉ lấy cấu trúc giai đoạn và chương). Kiến thức, thời gian, độ khó, tài nguyên đều lấy mới qua tool của chính nó.
- Chỉ chi tiết **giai đoạn hiện tại**, cửa sổ **1 tuần**; giai đoạn sau để sườn, hệ thống cập nhật khi học.

### Kiến trúc: Plan-and-Execute + ReAct + Critic nhẹ (hybrid)
```
plan → execute (ReAct từng bước) → replan (tối đa 1 lần) → assemble (mỗi tuần 1 lần) → critic (code) → trình bày
```
- **Plan** = danh sách bước làm việc nội bộ (mục tiêu, không phải tên tool). Học sinh không thấy.
  - 2 bước **cố định** (code viết): F1 nắm kiến thức các chương trong tuần; F2 xác định buổi học và độ khó.
  - Tối đa 3 bước **LLM sinh thêm** (ví dụ tìm tài nguyên cho chủ đề yếu, xét quan hệ giữa chương); LLM không được sinh bước tính thời gian hay lặp bước cố định.
- **Execute**: mỗi bước chạy ReAct, tự chọn tool (tối đa 3 lần gọi cho bước LLM sinh); bước độc lập chạy song song.
- **Replan**: chỉ khi kết quả thiếu hoặc cho thấy cần đổi (ví dụ không đủ thời gian cho hai chương).
- **Assemble**: `invoke_structured` sinh từng tuần (schema `Week`).
- **Critic**: chỉ kiểm tra bằng code (`chapter_id` hợp lệ, tổng thời lượng hoạt động bằng thời lượng buổi, đủ buổi theo lịch, url có trong kết quả tra cứu, tỉ lệ độ khó); sửa tối đa 1 lần; lỗi ghi vào `lp_issues` để sau này agent đánh giá chất lượng và góp ý học sinh dùng chung.

### Tool (`lp_tools.py`)
| Tool | Làm gì |
|---|---|
| `analyze_chapter_knowledge(chapter_id)` | Với mỗi bài: ý chính, cần nắm, cần hiểu, dạng bài, liên hệ (chapter_id, lesson, relation). Cache theo chương |
| `compute_schedule()` | Xếp các buổi học cụ thể (ngày, giờ, thời lượng) từ lịch học, tính số tuần còn lại, gợi ý số buổi mỗi chương, cảnh báo |
| `compute_difficulty_ratio()` | Tỉ lệ easy/medium/hard theo điểm mục tiêu (dùng bảng của `build_matrix_v2.py`), số buổi mỗi mức |

Hồ sơ, môn và cửa sổ được nạp sẵn vào tool (closure) nên LLM không thể điền sai dữ liệu hồ sơ.

### Cấu trúc kết quả (schema tiếng Anh)
`LearningPath` → `Schedule`, `Week` → `Session` (ngày, giờ, thời lượng, loại `lesson`/`review`/`assessment`, chương/bài, `key_points`, `must_know`, `must_understand`, `related`, độ khó, `activities`, `resources`, `assessment`) → `Activity` (loại, nội dung, phút, độ khó, dạng bài).

### Nút trên giao diện (A2A lớp ngoài)
- Mọi buổi học đều có nút **hỏi đáp** và **test nhanh** (UI dựng từ chương/bài của buổi, không lưu trong dữ liệu buổi).
- Buổi cuối tuần (loại `assessment`) kèm bài test định kì và là buổi đánh giá lại trình độ.
- Hai việc này không chạy khi đang sinh lộ trình.

## 7. Các file chính
| Nhóm | File |
|---|---|
| Schema, state | `src/state_plan.py` |
| Collect | `src/edu_planning/collect_student_model.py`, `student_store.py` |
| Planning | `planning_agent.py`, `planning_tools.py`, `feedback_tools.py`, `roadmap_graph.py` |
| Learning Path | `lp_tools.py` (đã có), graph (chưa) |
| Chạy thử | `run_planning.py`, `test_lp_tools.py` |
| Prompt | `collect_student_model`, `collect_student_model_update`, `guard`, `query_transform`, `planning_agent`, `planning_finalize`, `planning_feedback`, `lp_planner`, `lp_executor`, `lp_assemble`, `lp_chapter_knowledge` |
| Đường dẫn prompt | `src/edu_qa/paths.py` |

## 8. Tiến độ và rủi ro
- **Chưa có lần chạy nào thành công.** Lần chạy thử dừng khi khởi tạo `VectorStoreRetriever` (không có traceback; nghi ngờ nạp reranker hoặc BM25), nên toàn bộ code chưa được kiểm chứng.
- Chưa kiểm tra: `create_agent` có khớp phiên bản LangGraph, model Groq có xử lý tốt structured output nhiều tầng (`ProfilePatch`, `Week`), các hàm `hybrid_search_qa` và `rerank_batch` trên dữ liệu thật.
- Hệ thống chậm; các biện pháp đã đưa vào thiết kế: cache phân tích chương, cửa sổ 1 tuần, giới hạn số bước và số lần gọi tool, giới hạn replan và sửa.
- `MasterRoadmap` chưa có số tuần mỗi giai đoạn: dự kiến chia thời gian theo trọng số (quy tắc tự đặt, cần duyệt).
- `khung_gio_ranh` và `lich_bận` là văn bản tự do nên phần đọc giờ rảnh dài và có thể sai; nên đổi sang dạng có cấu trúc.
- Khóa YouTube đọc bằng `os.getenv`, có thể cần `load_dotenv()`.

## 9. Việc tiếp theo
1. Sửa lỗi khởi tạo retriever và chạy thử luồng Collect → Planning.
2. Chạy `test_lp_tools.py` kiểm tra hai tool tính toán.
3. Viết graph Learning Path (plan, execute, replan, assemble, critic) và thêm state `lp_*`.
4. Thêm tool giáo trình giáo viên (Qdrant collection riêng).
5. Progress Agent, Report Agent, theo dõi học tập trong `edu_qa`, A2A lớp ngoài, chế độ test không hỏi lại cho `edu_exam`, bài test đầu vào.