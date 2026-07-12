from langchain_core.tools import tool


def build_search_tool(retriever, collected_docs: list):
    """Tạo tool search_documents gắn với 1 retriever cụ thể (dependency
    injection qua closure, giống pattern functools.partial đang dùng
    cho node). collected_docs là list rỗng được truyền từ ngoài vào,
    dùng để lưu lại doc thật (kèm rerank_score) cho node đọc lại sau
    khi agent chạy xong.
    """

    @tool
    def search_documents(query: str) -> str:
        """Tìm kiếm tài liệu Toán 10 (Kết nối tri thức) liên quan đến
        một truy vấn cụ thể, dùng vector search (hybrid dense + sparse)
        và cross-encoder rerank thật — không phải suy đoán bằng ngôn ngữ.

        Dùng tool này khi câu hỏi của học sinh cần tra cứu khái niệm,
        công thức, định nghĩa, hoặc quy tắc cụ thể từ SGK.

        KHÔNG dùng tool này khi:
        - Câu hỏi chỉ là một phép tính/phương trình thuần túy, không cần
          công thức hay quy tắc nào để tra cứu.
        - Câu hỏi còn quá mơ hồ để tạo ra một truy vấn tìm kiếm có nghĩa
          (trường hợp này hãy gọi request_clarification thay vào đó).

        Sau khi nhận kết quả, hãy tự đọc rerank_score đi kèm mỗi chunk:
        - rerank_score >= 0.5: đủ tin cậy để dùng cho câu trả lời.
        - rerank_score < 0.5 ở TẤT CẢ chunk: kết quả có thể chưa đủ liên
          quan. Bạn có thể viết lại query cụ thể hơn (thêm tên công thức/
          quy tắc/chương bài nếu suy luận được từ câu hỏi gốc) và gọi lại
          tool này thêm 1 lần. Không gọi quá 2 lần cho cùng 1 câu hỏi.

        Args:
            query: truy vấn tìm kiếm, nên chứa từ khóa cụ thể (tên khái
                niệm, công thức, chương/bài nếu xác định được).

        Returns:
            Danh sách chunk tìm được, mỗi chunk kèm rerank_score, dạng
            văn bản. Nếu không tìm thấy chunk nào, trả về thông báo
            tương ứng.
        """
        raw = retriever.hybrid_search(query)
        reranked = retriever.rerank(query, raw, top_k=5)

        collected_docs.clear()
        collected_docs.extend(reranked)

        if not reranked:
            return "Không tìm thấy tài liệu nào liên quan đến truy vấn này."

        lines = []
        for i, doc in enumerate(reranked):
            score = doc.metadata.get("rerank_score", 0.0)
            lines.append(f"[chunk {i} | rerank_score={score:.3f}]\n{doc.page_content}")
        return "\n---\n".join(lines)

    return search_documents


def build_clarify_tool(outcome: dict):
    """Tạo tool request_clarification. outcome là dict rỗng truyền từ
    ngoài vào, dùng để node biết agent đã quyết định dừng lại chờ học
    sinh trả lời thêm hay chưa.
    """

    @tool
    def request_clarification(clarify_question: str) -> str:
        """Gọi tool này khi câu hỏi của học sinh quá mơ hồ để xác định
        cần tìm tài liệu gì hoặc cần xử lý tính toán gì.

        KHÔNG gọi tool này nếu câu hỏi đã đủ rõ để tìm tài liệu hoặc để
        xử lý tiếp, kể cả khi bạn chưa chắc chắn tuyệt đối về nội dung —
        chỉ gọi khi thực sự không xác định được ý định của học sinh.

        Args:
            clarify_question: một câu hỏi ngắn gọn, cụ thể, giúp học sinh
                bổ sung thông tin còn thiếu (ví dụ hỏi rõ bài/dạng bài,
                hoặc hỏi rõ đang vướng ở bước nào). Không đoán chủ đề câu
                hỏi gốc, không hỏi nhiều câu cùng lúc.

        Returns:
            Xác nhận đã ghi nhận câu hỏi làm rõ, dừng xử lý ở đây.
        """
        outcome["awaiting_user"] = True
        outcome["clarify_question"] = clarify_question
        return "Đã ghi nhận câu hỏi làm rõ, dừng xử lý tại đây."

    return request_clarification
