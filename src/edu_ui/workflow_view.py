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


def skeleton_data(state):
    """Whitelist presentation fields from the structured roadmap, not from prose."""
    roadmap = state.get("master_roadmap") or {}
    if hasattr(roadmap, "model_dump"):
        roadmap = roadmap.model_dump(mode="json")
    phases = roadmap.get("giai_doan") if isinstance(roadmap, dict) else None
    if not isinstance(phases, list) or not phases:
        return None
    result = (state.get("entry_test") or {}).get("result") or {}
    assessment = None
    if isinstance(result, dict) and "total" in result:
        assessment = {k: result.get(k) for k in ("correct", "total")}
        assessment["chapters"] = [{"chapter_id": str(cid), **{k: item.get(k) for k in ("correct", "total", "ratio", "level")}}
                                  for cid, item in (result.get("chapters") or {}).items() if isinstance(item, dict)]
    return {"goal": roadmap.get("muc_tieu_tong", ""), "strategy": roadmap.get("chien_luoc", ""),
            "phases": [{k: phase.get(k) for k in ("thu_tu", "ten", "mon_hoc", "muc_tieu", "tieu_chi_hoan_thanh")}
                       | {"chapters": [{k: chapter.get(k) for k in ("chapter_id", "lessons", "ly_do")}
                                       for chapter in (phase.get("chapters") or []) if isinstance(chapter, dict)],
                          "resources": [{k: resource.get(k) for k in ("loai", "tieu_de", "url", "ghi_chu")}
                                        for resource in (phase.get("tai_nguyen") or []) if isinstance(resource, dict)]}
                       for phase in phases if isinstance(phase, dict)],
            "assumptions": roadmap.get("gia_dinh") or [], "assessment": assessment}


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
                                "chapter_id": chunk.get("chapter"),
                                "document_type": chunk.get("document_type") or (chunk.get("metadata") or {}).get("document_type", ""),
                                "source_type": chunk.get("source_type", "")})
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
            skeleton = skeleton_data(state)
            if skeleton:
                out["full_text"] = out["answer"]
                out["skeleton"] = skeleton
                out["answer"] = "Sườn lộ trình đã sẵn sàng. Bạn xem các mục bên dưới rồi xác nhận hoặc góp ý chỉnh sửa."
            out["actions"] = [{"label": "Xác nhận sườn", "value": "chốt"},
                              {"label": "Góp ý chỉnh sửa", "compose": True}]
        elif status == "path_ready":
            plan_id = (state.get("learning_path") or {}).get("plan_id")
            out["actions"] = [{"label": "Xem lộ trình", "url": f"/roadmap?plan={plan_id}" if plan_id else f"/roadmap?session={sid}"}]
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
