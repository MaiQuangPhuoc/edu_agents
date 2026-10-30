"""Public UI projections. Never serialize raw graph state or answer keys."""


def public_questions(questions):
    return [{"no": q.get("no", i), "question": q.get("question", ""),
             "options": q.get("options", {}), "chapter_id": q.get("chapter_id", "")}
            for i, q in enumerate(questions, 1)]


def latest_messages(state):
    result = []
    for message in reversed(state.get("messages", [])):
        if getattr(message, "type", "") == "human":
            break
        if getattr(message, "type", "") == "ai" and isinstance(message.content, str):
            result.append(message)
    return list(reversed(result))


def interests(state, chapter_lookup):
    pending = state.get("knowledge_pending")
    if not pending or state.get("knowledge_done"):
        return []
    if pending.get("type") == "retry":
        return [{"chapter": c, "lesson": l, "section": s} for c, l, s in pending["missing"]]
    cid = pending["chuong"]
    chapter = chapter_lookup(state["student_profile"]["mon_hoc"], cid)
    return [{"chapter": cid, "lesson": lesson, "section": section}
            for lesson, sections in chapter["lessons"].items() for section in sections]


def project(session, chapter_lookup=None):
    state, mode, sid = session["state"], session["mode"], session["id"]
    out = {"session_id": sid, "mode": mode, "revision": session["revision"],
           "answer": "", "actions": [], "suggestions": [], "sources": []}
    if mode == "qa":
        out.update(answer=state.get("final_answer", ""), suggestions=state.get("suggestions", []))
        sources, seen = [], set()
        for result in state.get("rag_results", []):
            result = result.model_dump() if hasattr(result, "model_dump") else result
            for chunk in result.get("chunks", []):
                chunk = chunk.model_dump() if hasattr(chunk, "model_dump") else chunk
                key = (chunk.get("source"), chunk.get("content"))
                if key in seen:
                    continue
                seen.add(key)
                sources.append({"title": chunk.get("source", "Tài liệu"), "content": chunk.get("content", ""),
                                "chapter_id": chunk.get("chapter")})
        for source in sources:
            if str(source["title"]).startswith(("https://", "http://")):
                source["url"] = source["title"]
        out["sources"] = sources[:12]
        return out
    messages = latest_messages(state)
    out["answer"] = "\n\n".join(m.content for m in messages)
    if messages and messages[-1].additional_kwargs.get("ui_confirm"):
        out["actions"].append({"label": "Xác nhận", "value": "xác nhận đúng"})
    if mode == "exam":
        rows = interests(state, chapter_lookup) if chapter_lookup else []
        if rows:
            out.update(interests=rows, answer="Chọn mức quan tâm cho từng chủ đề bên dưới, rồi gửi đánh giá.")
        matrix = state.get("exam_matrix")
        if matrix and not state.get("matrix_done"):
            out.update(matrix=matrix, answer="Ma trận đề đã sẵn sàng. Bạn có thể xác nhận hoặc nhập yêu cầu chỉnh sửa.",
                       actions=[{"label": "Xác nhận ma trận", "value": "ok"}])
        if state.get("evaluate_done") and session.get("exam_url"):
            out["actions"] = [{"label": "Xem đề", "url": session["exam_url"]}]
    else:
        status = state.get("roadmap_status")
        out["status"] = status
        if status == "awaiting_test_answers":
            out.update(answer="Bài kiểm tra đầu vào đã sẵn sàng. Hoàn thành bài để mình xây dựng lộ trình phù hợp.",
                       actions=[{"label": "Làm bài test", "url": f"/study?session={sid}&view=entry"}])
        elif status == "awaiting_feedback":
            out["actions"] = [{"label": "Xác nhận sườn", "value": "chốt"}]
        elif status == "path_ready":
            out["actions"] = [{"label": "Xem lộ trình", "url": f"/roadmap?session={sid}"}]
        elif status in ("path_failed", "entry_test_failed"):
            out["actions"] = [{"label": "Thử lại", "value": "thử lại"}]
    return out


def answer_text(questions, answers):
    expected = {str(q["no"]): q for q in questions}
    if set(answers) != set(expected):
        raise ValueError("Vui lòng trả lời đầy đủ các câu hỏi trước khi nộp.")
    if any(answers[k] not in q["options"] for k, q in expected.items()):
        raise ValueError("Đáp án không hợp lệ.")
    return ", ".join(f"{q['no']}-{answers[str(q['no'])]}" for q in questions)
