# EDUAGENT

Hệ thống hỗ trợ học tập AI dành cho học sinh lớp 10 (chương trình GDPT 2018), xây dựng trong khuôn khổ thực tập doanh nghiệp tại **Rikai Technology**. Hệ thống kết hợp **LLM + RAG + kiến trúc multi-agent LangGraph** để cung cấp: hỏi đáp theo chương trình học, sinh đề kiểm tra tự động, và lập kế hoạch học tập cá nhân hóa.

---

## 1. Mục tiêu

- Hỗ trợ học sinh lớp 10 tự học/ôn tập các môn **Toán, Ngữ Văn, Lịch Sử**.
- Trả lời câu hỏi bám sát nội dung sách giáo khoa (Kết nối tri thức / Cánh Diều), hạn chế tối đa việc LLM "bịa" kiến thức ngoài tài liệu.
- Tự động sinh đề kiểm tra theo ma trận đề, đúng phạm vi chương/bài do học sinh chỉ định.
- Tách bạch rõ ràng: **LLM xử lý ngôn ngữ**, **code (SymPy/numpy) xử lý tính toán số học** — LLM không được tự suy luận các phép tính nhiều bước.

## 2. Kiến trúc tổng quan

```
                    ┌─────────────┐
                    │   main.py   │  (CLI chọn module)
                    └──────┬──────┘
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌─────▼──────┐
   │ edu_qa  │       │ edu_exam  │      │ edu_planning│
   │ (Q&A)   │       │(Sinh đề)  │      │ (Lộ trình)  │
   └─────────┘       └───────────┘      └────────────┘
        │                  │                  │
        └──────────┬───────┴──────────────────┘
                    │
         ┌──────────▼──────────┐
         │  llm_client / retriever (dùng chung) │
         └───────────────────────────────────────┘
```

Cả 3 module đều dùng chung `LLMClient` (khởi tạo lazy qua `get_llm()`, inject bằng `functools.partial`) và `VectorStoreRetriever` (Qdrant).

### 2.1 Module `edu_exam` — Sinh đề kiểm tra

Pipeline LangGraph gồm **7 bước tuần tự**:

```
collect_info → retrieve_docs → build_knowledge → build_matrix
     → build_specs → generate_questions → evaluate_exam
```

| Bước | Trạng thái | Mô tả |
|---|---|---|
| `collect_info` | ✅ Hoàn thành | Thu thập hồ sơ học sinh (môn, phạm vi chương, mục tiêu điểm, thời gian, số câu) |
| `retrieve_docs` | ✅ Hoàn thành | Truy xuất tài liệu theo phạm vi chương đã chọn |
| `build_knowledge` | ✅ Hoàn thành | Xây hồ sơ kiến thức theo từng chương/bài |
| `build_matrix` | ✅ Hoàn thành | Tính ma trận đề (phân bổ số câu theo mức độ nhận thức) |
| `build_specs` | ✅ Hoàn thành | Sinh đặc tả chi tiết từng câu hỏi |
| `generate_questions` | ✅ Hoàn thành | Sinh câu hỏi theo đặc tả |
| `evaluate_exam` | ⏸️ Đang thiết kế | Kiểm định đáp án + chất lượng đề (xem mục 5) |

### 2.2 Module `edu_qa` — Hỏi đáp

Pipeline 4 agent:

```
qa_router_agent → qa_rag_agent → qa_solve_agent → qa_format_agent
```

- **qa_router_agent**: Phân loại câu hỏi (loại 1: cần làm rõ / loại 2: tra cứu lý thuyết / loại 3: cần tính toán), tách thành các `sub_query`.
- **qa_rag_agent**: Hybrid search (dense + sparse/BM25) + rerank bằng cross-encoder, ngưỡng điểm giảm dần theo tầng (0.6 → 0.5 → Tavily web fallback) để đảm bảo đủ ngữ cảnh.
- **qa_solve_agent**: Với câu hỏi cần tính toán, LLM chọn tool phù hợp (SymPy) trong 4 meta-tool, không tự tính tay.
- **qa_format_agent**: Tổng hợp câu trả lời cuối cùng, giữ giọng văn phù hợp học sinh.

Lịch sử hội thoại (`chat_history`) lưu trong RAM theo phiên (session).

### 2.3 Module `edu_planning` — Lộ trình học tập

Sinh kế hoạch học tập cá nhân hóa dựa trên mục tiêu và thời gian của học sinh.

## 3. Pipeline dữ liệu (RAG)

- Nguồn: SGK lớp 10 — Toán ("Kết nối tri thức"), Ngữ Văn & Lịch Sử ("Cánh Diều").
- Chunking theo ranh giới đoạn văn, `MIN_WORDS=100 / MAX_WORDS=180` (an toàn trong giới hạn 256 token của bi-encoder tiếng Việt).
- Header (bài/chương/mục) được lặp lại ở mọi sub-chunk khi một mục bị tách nhỏ.
- Vector DB: **Qdrant**, một collection `"documents"` duy nhất, lọc theo metadata `mon_hoc`.
- Embedding: `bkai-foundation-models/vietnamese-bi-encoder` *(đang cân nhắc nâng cấp lên `AITeamVN/Vietnamese_Embedding_v2`)*.
- Reranker: `BAAI/bge-reranker-base` *(đang cân nhắc nâng cấp lên `AITeamVN/Vietnamese_Reranker`)*.

## 4. Cấu trúc thư mục (rút gọn)

```
EDUAGENT/
├── main.py                     # Entry point, chọn module qua CLI
├── src/
│   ├── clients/
│   │   ├── llm.py               # LLMClient (Groq/OpenAI/OpenRouter/Google)
│   │   └── embedding.py         # Embedding model
│   ├── modules/rag/
│   │   └── process_toan_10/
│   │       └── retrievers2.py   # VectorStoreRetriever (Qdrant + rerank)
│   ├── edu_exam/
│   │   ├── collect_info.py
│   │   ├── retrieve_docs.py
│   │   ├── build_knowledge.py
│   │   ├── build_matrix.py
│   │   ├── build_specs.py
│   │   ├── generate_questions.py
│   │   ├── evaluate_exam.py     # đang thiết kế
│   │   └── curriculum.py        # CHAPTER_MAP, normalize_chapter_key()
│   ├── edu_qa/
│   │   ├── qa_router_agent.py
│   │   ├── qa_rag_agent.py
│   │   ├── qa_solve_agent.py
│   │   ├── qa_format_agent.py
│   │   ├── graph.py              # build_qa_graph()
│   │   ├── state.py
│   │   ├── paths.py
│   │   ├── prompts/               # file .txt, placeholder {var}
│   │   └── tools/
│   │       ├── math_tools.py      # SymPy meta-tools
│   │       └── web_search_tool.py # Tavily fallback
│   ├── edu_planning/
│   ├── state.py / state_edu.py
│   └── configs.py                 # pydantic-settings, đọc .env
├── run_qa.py
├── run_exam.py
└── requirements.txt
```

## 5. Trạng thái phát triển — `evaluate_exam` (Bước 7, edu_exam)

Đang ở giai đoạn thiết kế, hướng đã thống nhất:

1. **Tách luồng kiểm tra đáp án** dựa trên từ khóa trong `dang_bai` / `bai`:
   - Câu lý thuyết/đơn giản → LLM review, nhưng bắt buộc bám sát chunk đã retrieve, không suy luận tự do.
   - Câu công thức phức tạp (đạo hàm, phương trình, lượng giác...) → bắt buộc dùng công cụ (SymPy/numpy) để xác minh, LLM không tự xử lý nhiều bước.
2. Nếu tool không tính được → fallback về LLM, nhưng gắn cờ `verify_method: llm_fallback` để hạ mức độ tin cậy khi dùng downstream.
3. Sau khi hoàn thiện luồng xác minh đáp án, tiếp tục triển khai 7 tiểu bước còn lại: kiểm tra khớp ma trận, độ phủ kiến thức, phát hiện trùng lặp, chất lượng đáp án nhiễu (distractor), độ phù hợp với học sinh, vòng lặp sửa lỗi (repair loop).

## 6. Nguyên tắc thiết kế cốt lõi

- **LLM không được sở hữu phép tính số học**: mọi phân bổ tỉ lệ, tính toán nhiều bước đều nằm ở code (SymPy/numpy).
- **Ngưỡng điểm (score threshold) quyết định việc retrieval đã đủ hay chưa**, không để LLM tự phán đoán.
- **Pipeline tất định (deterministic) thay vì ReAct** cho lĩnh vực giáo dục — ưu tiên độ tin cậy và khả năng kiểm chứng hơn tính linh hoạt.
- **`mon_hoc_override`** ở tầng UI ghi đè trực tiếp lên state, bỏ qua bước LLM nhận diện môn học khi người dùng đã chọn sẵn.
- **`verify_method`** luôn được gắn nhãn (tool / llm_fallback) để tầng downstream biết mức độ tin cậy của kết quả.

## 7. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| LLM backend | Groq (chính), OpenAI, OpenRouter, Google (toggle qua `.env` `API_PROVIDER`) |
| Orchestration | LangChain, LangGraph |
| Vector DB | Qdrant (hybrid dense + sparse/BM25) |
| Embedding | `bkai-foundation-models/vietnamese-bi-encoder` |
| Reranker | `BAAI/bge-reranker-base` (CrossEncoder) |
| Tính toán | SymPy, numpy |
| Tìm kiếm web fallback | Tavily |
| Tìm kiếm video | YouTube Data API v3 |
| Config | `pydantic-settings` |
| Ngôn ngữ / Env | Python 3.12, venv, Windows + VS Code |

