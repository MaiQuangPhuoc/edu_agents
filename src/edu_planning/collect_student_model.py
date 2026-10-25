import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import copy
from datetime import datetime, timedelta
from langchain_core.messages import AIMessage, HumanMessage
from src.clients.llm import LLMClient, build_prompt_messages
from src.edu_exam.curriculum import CURRICULUM
from src.edu_planning.student_store import save_student_model
from src.state_plan import PlanState, StudentModel, CollectTurn, CollectPatchTurn
from src.edu_qa.paths import (COLLECT_STUDENT_MODEL_PROMPT_PATH, COLLECT_UPDATE_PROMPT_PATH)
from difflib import SequenceMatcher
from src.edu_planning.query_builder import build_queries


MAX_HISTORY = 12        # số tin nhắn gần nhất đưa vào prompt
MAX_BOT_CHARS = 250    # tin cũ của bot cắt còn chừng này ký tự (tin cuối giữ nguyên)

def _history_text(messages: list) -> str:
    recent, lines = messages[-MAX_HISTORY:], []
    for i, m in enumerate(recent):
        text = str(m.content)
        if isinstance(m, HumanMessage):
            lines.append(f"Học sinh: {text}")
        else:
            if i < len(recent) - 1 and len(text) > MAX_BOT_CHARS:
                text = text[:MAX_BOT_CHARS].rstrip() + "…"
            lines.append(f"Trợ lý: {text}")
    return "\n".join(lines) or "(chưa có)"

def _compact(model: dict) -> str:
    """Hồ sơ dạng JSON gọn: bỏ trường rỗng, version, tien_do; thời gian cập nhật chỉ giữ HH:MM."""
    model = {k: v for k, v in model.items() if k not in ("version", "tien_do")}
    if model.get("updated_at"):
        model["cap_nhat_luc"] = str(model.pop("updated_at"))[11:16]
    def clean(x):
        if isinstance(x, dict):
            x = {k: clean(v) for k, v in x.items()}
            return {k: v for k, v in x.items() if v not in (None, "", [], {})}
        if isinstance(x, list):
            return [v for v in map(clean, x) if v not in (None, "", [], {})]
        return x
    return json.dumps(clean(model), ensure_ascii=False, separators=(",", ":"))

def _canon_subject(name: str) -> str:
    """"toán" -> "Toán 10": khớp không phân biệt hoa thường với tên môn trong chương trình."""
    n = (name or "").strip().lower()
    return next((k for k in CURRICULUM if n and k.lower().startswith(n)), name)

def _subjects_in(text: str) -> list[str]:
    t = text.lower()
    return [k for k in CURRICULUM if k.rsplit(" ", 1)[0].lower() in t]

def _curriculum_info(subjects: list[str]) -> str:
    if not subjects:      # chưa biết môn: chỉ liệt kê tên môn, chưa đưa chương
        return "Môn có tài liệu: " + ", ".join(CURRICULUM)
    return "\n".join(f"- {s}: " + ", ".join(f"{cid} ({ch['chapter_name']})" for cid, ch in CURRICULUM[s].items())
                     for s in subjects)

def _curriculum_lessons(subjects: list[str]) -> str:
    """Tên chương và tên các bài, để prompt query chỉ dùng tên có thật."""
    return "\n".join(
        f"- {s}:\n" + "\n".join(f"  {cid} ({ch['chapter_name']}): " + "; ".join(ch["lessons"])
                                for cid, ch in CURRICULUM[s].items())
        for s in subjects) or "(chưa rõ môn)"

NO_MISSING = "(không còn thiếu)"
def _missing(m: dict) -> str:
    nl, mt = (m.get("nang_luc") or [{}])[0], (m.get("muc_tieu") or [{}])[0]
    lich, st = m.get("lich_hoc") or {}, m.get("so_thich_hoc") or {}
    checks = [
        ("môn học", mt.get("mon_hoc") or nl.get("mon_hoc")),
        ("mục tiêu điểm (thang 10)", mt.get("muc_tieu_diem")),
        ("thời hạn (ngày kết thúc hoặc số tuần còn lại)", mt.get("han_chot") or mt.get("ngay_ket_thuc") or mt.get("so_tuan_con_lai")),
        ("ưu tiên (điểm số / hiểu bản chất / cả hai)", mt.get("uu_tien")),
        ("số buổi học mỗi tuần", lich.get("so_buoi_tuan")),
        ("thời lượng mỗi buổi (phút)", st.get("thoi_luong_buoi_phut")),
        ("điểm hiện tại", nl.get("diem_hien_tai")),
        ("chương mạnh hoặc yếu", nl.get("diem_manh") or nl.get("diem_yeu")),
    ]
    lack = [name for name, v in checks if v in (None, "", [], {})]
    return "; ".join(lack) or NO_MISSING

SIM_LIMIT = 0.5          # giống nhau từ ngưỡng này trở lên thì coi là lặp lại tin trước
MAX_REPLY_CHARS = 400    # tin hỏi thêm không dài hơn mức này (tin tóm tắt hồ sơ không bị giới hạn)

def _last_bot(messages: list) -> str:
    return next((str(m.content) for m in reversed(messages) if isinstance(m, AIMessage)), "")

def _bad_reply(text: str, prev: str, lack: str) -> str:
    """Trả về lý do nếu tin nhắn lặp tin trước hoặc quá dài; rỗng nếu ổn."""
    if prev and SequenceMatcher(None, text, prev).ratio() >= SIM_LIMIT:
        return "trùng với tin nhắn trước"
    if lack != NO_MISSING and len(text) > MAX_REPLY_CHARS:
        return f"quá dài (tối đa {MAX_REPLY_CHARS} ký tự)"
    return ""

def _fill_deadline(model: dict) -> None:
    """Có số tuần mà chưa có ngày kết thúc thì tính ngày bằng code."""
    for mt in model.get("muc_tieu", []):
        if mt.get("so_tuan_con_lai") and not mt.get("ngay_ket_thuc"):
            mt["ngay_ket_thuc"] = (datetime.now() + timedelta(weeks=mt["so_tuan_con_lai"])).strftime("%Y-%m-%d")

def _prefill(model: dict, prev: str, last_user: str) -> None:
    """Bot vừa hỏi 'ưu tiên' và học sinh trả lời rõ thì code điền luôn, tránh hỏi lại."""
    if "ưu tiên" not in prev.lower():
        return
    t = last_user.lower()
    d, b = ("điểm số" in t or "điểm cao" in t), ("bản chất" in t or "hiểu sâu" in t)
    val = "ca_hai" if ("cả hai" in t or "cả 2" in t or (d and b)) else "diem_so" if d else "hieu_ban_chat" if b else ""
    for mt in model.get("muc_tieu", []):
        if val and not mt.get("uu_tien"):
            mt["uu_tien"] = val

def _dump(turn, prev: str, last_user: str) -> dict:
    model = turn.student_model.model_dump(mode="json")
    for k in ("nang_luc", "muc_tieu"):
        for x in model.get(k, []):
            x["mon_hoc"] = _canon_subject(x["mon_hoc"])
    _fill_deadline(model)
    _prefill(model, prev, last_user)
    return model

def _update_mode(state: PlanState, llm_client: LLMClient) -> dict:
    req = state["update_request"]
    fields = req.get("fields", [])
    current = state.get("student_model", {})
    shown = {k: v for k, v in current.items() if k != "tien_do"}

    messages = build_prompt_messages(
        COLLECT_UPDATE_PROMPT_PATH,
        {
            "fields": ", ".join(fields),
            "ly_do": req.get("ly_do", ""),
            "student_model": _compact(shown),
            "history": _history_text(state.get("messages", [])),
        },
    )

    turn = llm_client.invoke_structured(
        CollectPatchTurn,
        messages,
        max_tokens=3000,
    )
    if turn is None:
        return {"messages": [AIMessage(content="Bạn nhắc lại phần muốn đổi giúp mình nhé?")],
                "current_step": "collect_student_model"}

    out = {"messages": [AIMessage(content=turn.tin_nhan)], "current_step": "collect_student_model"}
    if not turn.hoan_tat:
        return out

    patch = turn.patch.model_dump(mode="json")
    applied = [f for f in fields if patch.get(f) is not None]     # chỉ nhận nhóm được yêu cầu đổi
    if not applied:
        return out

    new = dict(current)
    for f in applied:
        new[f] = patch[f]
    new["updated_at"] = datetime.now().isoformat()
    save_student_model(new)

    out.update({
        "student_model_prev": current,
        "student_model":      new,
        "roadmap_prev":       state.get("master_roadmap", {}),
        "search_queries":     build_queries(new),
        "update_request":     {},
        "roadmap_status":     "profile_changed",
    })
    return out

def collect_student_model(state: PlanState, llm_client: LLMClient) -> dict:
    if state.get("roadmap_status") == "updating_profile" and state.get("update_request"):
        return _update_mode(state, llm_client)

    if state.get("model_done", False):
        return {"current_step": "collect_student_model"}

    student_id = state.get("student_id", "")
    msgs = state.get("messages", [])
    prev = _last_bot(msgs)
    last_user = next((str(m.content) for m in reversed(msgs) if isinstance(m, HumanMessage)), "")
    current = copy.deepcopy(state.get("student_model") or StudentModel(student_id=student_id).model_dump(mode="json"))
    _fill_deadline(current)
    _prefill(current, prev, last_user)
    known = [x["mon_hoc"] for k in ("muc_tieu", "nang_luc") for x in current.get(k, [])]
    subjects = [s for s in dict.fromkeys(_canon_subject(n) for n in known) if s in CURRICULUM] or _subjects_in(last_user)

    messages = build_prompt_messages(
        COLLECT_STUDENT_MODEL_PROMPT_PATH,
        {
            "thong_tin_da_co": _compact(current),
            "con_thieu": _missing(current),
            "chuong_co_tai_lieu": _curriculum_info(subjects),
            "history": _history_text(msgs),
        },
    )

    print("\n" + "=" * 70)
    print("PROMPT collect_student_model")
    print("=" * 70)

    for message in messages:
        print(f"\n[{message['role'].upper()}]")
        print("-" * 70)
        print(message["content"])

    print("\n" + "=" * 70)

    turn = llm_client.invoke_structured(
        CollectTurn,
        messages,
        max_tokens=3000,
    )
    if turn is None:
        return {"messages": [AIMessage(content="Bạn nhắc lại giúp mình nhé?")], "current_step": "collect_student_model"}
    
    lack = _missing(_dump(turn, prev, last_user))
    why = _bad_reply(turn.tin_nhan, prev, lack)
    if why:
        note = f"\n\nLƯU Ý: tin_nhan lần trước {why}. Viết lại ngắn gọn, không lặp câu cũ."
        retry_messages = messages + [
            {"role": "user", "content": note}
        ]

        again = llm_client.invoke_structured(
            CollectTurn,
            retry_messages,
            max_tokens=3000,
        )
        if again and not _bad_reply(again.tin_nhan, prev, lack):
            turn = again
        elif lack != NO_MISSING:
            turn.tin_nhan = f"Mình cần thêm thông tin: {lack}. Bạn bổ sung giúp mình nhé?"

    model = _dump(turn, prev, last_user)

    for nl in model.get("nang_luc", []):
        # chu_de do code dựng từ điểm mạnh/yếu: chưa có số đo nên muc_nam = None, do_tin_cay = 0
        ids = list(dict.fromkeys(nl.get("diem_yeu", []) + nl.get("diem_manh", [])))
        nl["chu_de"] = [{"chapter_id": c, "lesson": "", "muc_nam": None, "do_tin_cay": 0.0,
                         "nguon": "tu_danh_gia", "cap_nhat": None} for c in ids]
    model["student_id"] = student_id
    model["tien_do"] = current.get("tien_do", {})      # phần của Progress Agent, không để LLM ghi đè
    model["updated_at"] = datetime.now().isoformat()

    if turn.hoan_tat:
        save_student_model(model)
    
    queries = state.get("search_queries", [])      # query tạo sau bài test (entry_grade_node)
    return {
        "messages":      [AIMessage(content=turn.tin_nhan)],
        "student_model": model,
        "search_queries": queries,
        "model_done":    turn.hoan_tat,
        "current_step":  "collect_student_model",
    }