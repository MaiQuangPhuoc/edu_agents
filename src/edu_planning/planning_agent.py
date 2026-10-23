import json, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from src.edu_planning.feedback_tools import FEEDBACK_TOOLS
from src.edu_planning.chapter_utils import fix_chapters


from src.state_plan import PlanState, MasterRoadmap, HandoffMessage, BatchPlan, Overview
from src.edu_qa.paths import PLANNING_PROMPT_PATH, PLANNING_FINALIZE_PROMPT_PATH, PLANNING_FEEDBACK_PROMPT_PATH, PLANNING_OVERVIEW_PROMPT_PATH
from src.edu_planning.plan_context import time_text, levels_text, lesson_plan_text, make_batches

from src.clients.llm import LLMClient

from langchain.agents import create_agent
from langgraph.errors import GraphRecursionError

from src.edu_exam.curriculum import get_subject_curriculum
from src.edu_qa.paths import PLANNING_PROMPT_PATH, PLANNING_FINALIZE_PROMPT_PATH
from src.edu_planning.planning_tools import make_planning_tools

MAX_STEPS = 3         # số lượt tool tối đa mỗi lô
BATCH_SIZE = 2        # số chương mỗi lô
DEBUG_PROMPT = True   # True: in prompt của từng lô để kiểm tra


MAX_REVISION = 3

def _curriculum_text(sm: dict, batch: dict | None = None) -> str:
    items = (sm.get("nang_luc") or []) + (sm.get("muc_tieu") or [])
    subjects = [batch["subject"]] if batch else sorted({x["mon_hoc"] for x in items if x.get("mon_hoc")})
    lines = []
    for subject in subjects:
        for ch_id, ch in get_subject_curriculum(subject).items():
            if batch and ch_id not in batch["chapters"]:
                continue
            lines.append(f"[{subject}] chapter_id={ch_id}: {ch['chapter_name']}")
            lines += [f"    - {lesson}" for lesson in ch["lessons"]]
    return "\n".join(lines)


def _diff_text(old: dict, new: dict) -> str:
    lines = []
    for k in new:
        if k in ("tien_do", "updated_at"):
            continue
        if old.get(k) != new.get(k):
            lines.append(f"- {k}: trước = {json.dumps(old.get(k), ensure_ascii=False)} | sau = {json.dumps(new.get(k), ensure_ascii=False)}")
    return "\n".join(lines) or "(không có thay đổi)"


def _change_text(state: PlanState) -> str:
    status = state.get("roadmap_status")
    if status == "profile_changed" and state.get("roadmap_prev"):
        return ("Học sinh vừa đổi thông tin. Sườn cũ được lập theo hồ sơ cũ nên có thể không còn phù hợp.\n"
                "SƠ ĐỒ CŨ:\n" + json.dumps(state["roadmap_prev"], ensure_ascii=False, indent=2)
                + "\n\nTHÔNG TIN ĐÃ ĐỔI:\n" + _diff_text(state.get("student_model_prev", {}), state.get("student_model", {}))
                + "\n\nHãy lập lại sườn theo hồ sơ MỚI: giữ phần còn phù hợp, bỏ hoặc thay phần không còn phù hợp.")
    if status == "revising" and state.get("master_roadmap"):
        return ("SƠ ĐỒ HIỆN TẠI:\n" + json.dumps(state["master_roadmap"], ensure_ascii=False, indent=2)
                + "\n\nYÊU CẦU CHỈNH SỬA CỦA HỌC SINH:\n" + state.get("feedback", ""))
    return "Không có (lần lập đầu tiên)."


def _queries_text(state: PlanState, batch: dict | None = None) -> str:
    qs = state.get("search_queries") or []
    if batch:
        qs = [q for q in qs if q["subject"] == batch["subject"]
              and (not q.get("chapter_id") or q["chapter_id"] in batch["chapters"])]
    if not qs:
        return "(không có)"
    return "\n".join(
        f"- [{q['subject']}{' | chương ' + q['chapter_id'] if q.get('chapter_id') else ''} | {q['nguon']}] {q['query']}"
        for q in qs)

def _context(prompt: str, sm: dict, retriever, batch=None, done=()) -> str:
    pham_vi = (f"{batch['subject']}, chương {', '.join(batch['chapters'])}" if batch
               else "tất cả các chương trong cấu trúc chương trình")
    return (prompt
            .replace("{thoi_gian}", time_text(sm))
            .replace("{muc_do}", levels_text(sm, batch))
            .replace("{giao_an}", lesson_plan_text(retriever, sm, batch))
            .replace("{pham_vi}", pham_vi)
            .replace("{da_sinh}", "\n".join(f"- {t}" for t in done) or "Chưa có lô nào được sinh trước."))

def _build_prompt(state: PlanState, retriever, batch=None, done=()) -> str:
    sm = state.get("student_model", {})
    return _context(PLANNING_PROMPT_PATH.read_text(encoding="utf-8")
            .replace("{student_model}", json.dumps(sm, ensure_ascii=False, indent=2))
            .replace("{curriculum}", _curriculum_text(sm, batch))
            .replace("{thay_doi}", _change_text(state))
            .replace("{queries}", _queries_text(state, batch)), sm, retriever, batch, done)

def _build_finalize_prompt(state, transcript, retriever, batch=None, done=()) -> str:
    sm = state.get("student_model", {})
    return _context(PLANNING_FINALIZE_PROMPT_PATH.read_text(encoding="utf-8")
            .replace("{student_model}", json.dumps(sm, ensure_ascii=False, indent=2))
            .replace("{curriculum}", _curriculum_text(sm, batch))
            .replace("{transcript}", transcript)
            .replace("{chinh_sua}", _change_text(state)), sm, retriever, batch, done)

def _debug(title: str, text: str):
    if DEBUG_PROMPT:
        print(f"\n===== {title} =====\n{text}\n===== hết {title} =====")

def _transcript(msgs: list) -> str:
    lines = []
    for m in msgs[1:]:
        if isinstance(m, AIMessage):
            calls = ", ".join(f"{c['name']}({c['args']})" for c in (m.tool_calls or []))
            lines.append(f"[Planner] {m.content} {('-> gọi: ' + calls) if calls else ''}".strip())
        elif isinstance(m, ToolMessage):
            lines.append(f"[Kết quả tool] {str(m.content)[:3000]}")
    return "\n".join(lines) or "(không gọi tool)"

# format roadmap MasterRoadmap thành text để học sinh đọc và góp ý
def _format_roadmap(rm: dict) -> str:
    lines = [f"**Mục tiêu tổng:** {rm['muc_tieu_tong']}", f"**Chiến lược:** {rm['chien_luoc']}", ""]
    for gd in rm["giai_doan"]:
        lines.append(f"**Giai đoạn {gd['thu_tu']}: {gd['ten']}** ({gd['mon_hoc']})")
        lines.append(f"- Mục tiêu: {gd['muc_tieu']}")
        for ch in gd["chapters"]:
            lines.append(f"- Chương {ch['chapter_id']}: {', '.join(ch['lessons'])} — {ch['ly_do']}")
        lines.append(f"- Hoàn thành khi: {gd['tieu_chi_hoan_thanh']}")
        for tn in gd.get("tai_nguyen", []):
            nhan = {"tai_lieu": "Tài liệu", "video": "Video", "giao_trinh": "Giáo trình"}[tn["loai"]]
            link = f" ({tn['url']})" if tn.get("url") else ""
            note = f" — {tn['ghi_chu']}" if tn.get("ghi_chu") else ""
            lines.append(f"- {nhan}: {tn['tieu_de']}{link}{note}")
        lines.append("")
    if rm.get("gia_dinh"):
        lines.append("**Điểm mình đang giả định (bạn kiểm tra giúp):**")
        lines += [f"- {g}" for g in rm["gia_dinh"]]
    if any(gd.get("tai_nguyen") for gd in rm["giai_doan"]):
        lines.append("\n*Tài liệu và video là gợi ý tìm tự động, bạn nên xem qua trước khi dùng.*")
    lines.append("\nBạn thấy sườn này thế nào? Bạn có thể góp ý, hỏi lý do, đổi thông tin cá nhân, hoặc nói 'chốt' nếu đồng ý.")
    return "\n".join(lines)

def make_planning_graph(retriever, llm_client: LLMClient, checkpointer=None):
    tools = make_planning_tools(retriever, llm_client)
    react = create_agent(llm_client._llm, tools)
    llm_decide = llm_client._llm.bind_tools(FEEDBACK_TOOLS)

    def entry(state: PlanState) -> str:
        return "handle_feedback" if state.get("roadmap_status") == "awaiting_feedback" else "planner"

    def planner(state: PlanState) -> dict:
        sm = state.get("student_model", {})
        done, giai_doan, gia_dinh, logs = [], [], [], []
        for batch in make_batches(sm, BATCH_SIZE):
            print(f"[planning] lô: {batch['subject']} chương {batch['chapters']}")
            prompt = _build_prompt(state, retriever, batch, done)
            _debug("PROMPT AGENT", prompt)
            msgs = []
            try:
                for chunk in react.stream({"messages": [HumanMessage(content=prompt)]},
                                          config={"recursion_limit": 2 * MAX_STEPS + 1},
                                          stream_mode="values"):
                    msgs = chunk["messages"]
                    if isinstance(msgs[-1], AIMessage):
                        for c in (msgs[-1].tool_calls or []):
                            print(f"[planning] gọi tool: {c['name']} {c['args']}")
            except GraphRecursionError:
                print("[planning] vượt giới hạn vòng, dùng kết quả đã tra được")
                
            msgs = msgs or [HumanMessage(content=prompt)]
            transcript = _transcript(msgs)
            fprompt = _build_finalize_prompt(state, transcript, retriever, batch, done)
            _debug("PROMPT SINH SƯỜN", fprompt)
            res = llm_client.invoke_structured(BatchPlan, [{"role": "user", "content": fprompt}], max_tokens=3000)
            if res is None:
                return {"plan_draft": {}}
            part = res.model_dump()
            for gd in part["giai_doan"]:     # bỏ tài nguyên có url không xuất hiện trong kết quả tra cứu
                gd["tai_nguyen"] = [t for t in gd.get("tai_nguyen", []) if t.get("url") and t["url"] in transcript]
            giai_doan += part["giai_doan"]
            gia_dinh += part["gia_dinh"]
            done += part["tom_tat"]
            logs.append(transcript)
        return {"plan_draft": {"giai_doan": giai_doan, "gia_dinh": gia_dinh, "tom_tat": done},
                "plan_transcript": "\n".join(logs)}

    def _fail() -> dict:
        return {"master_done": False, "roadmap_status": "draft", "current_step": "planning"}

    def finalize(state: PlanState) -> dict:
        sm = state.get("student_model", {})
        if state.get("roadmap_status") == "revising":      # chỉnh sửa: sinh lại cả sườn một lần
            transcript = state.get("plan_transcript", "")
            prompt = _build_finalize_prompt(state, transcript, retriever)
            _debug("PROMPT CHỈNH SỬA", prompt)
            result = llm_client.invoke_structured(MasterRoadmap, [{"role": "user", "content": prompt}], max_tokens=4000)
            if result is None:
                return _fail()
            roadmap = result.model_dump()
            for gd in roadmap["giai_doan"]:
                gd["tai_nguyen"] = [t for t in gd.get("tai_nguyen", []) if t.get("url") and t["url"] in transcript]
        else:                                               # lập mới: ghép các lô + sinh 2 trường tổng
            draft = state.get("plan_draft") or {}
            if not draft.get("giai_doan"):
                return _fail()
            for i, gd in enumerate(draft["giai_doan"], 1):
                gd["thu_tu"] = i
            ds_gd = "\n".join(f"- Giai đoạn {gd['thu_tu']}: {gd['ten']} ({gd['mon_hoc']}; chương "
                              f"{', '.join(c['chapter_id'] for c in gd['chapters'])})" for gd in draft["giai_doan"])
            prompt = (PLANNING_OVERVIEW_PROMPT_PATH.read_text(encoding="utf-8")
                      .replace("{student_model}", json.dumps(sm, ensure_ascii=False, indent=2))
                      .replace("{thoi_gian}", time_text(sm))
                      .replace("{giai_doan}", ds_gd)
                      .replace("{tom_tat}", "\n".join(f"- {t}" for t in draft["tom_tat"])))
            _debug("PROMPT TỔNG QUAN", prompt)
            ov = llm_client.invoke_structured(Overview, [{"role": "user", "content": prompt}], max_tokens=800)
            if ov is None:
                return _fail()
            roadmap = {**ov.model_dump(), "giai_doan": draft["giai_doan"], "gia_dinh": draft.get("gia_dinh", [])}
        notes = fix_chapters(roadmap)
        roadmap["gia_dinh"] = list(roadmap.get("gia_dinh", [])) + notes
        return {"master_roadmap": roadmap, "master_done": True,
                "roadmap_status": "draft", "current_step": "planning"}

    def present_roadmap(state: PlanState) -> dict:
        rm = state.get("master_roadmap")
        if not rm:
            return {"messages": [AIMessage(content="Mình chưa lập được sườn lộ trình, bạn thử lại nhé.")]}
        return {"messages": [AIMessage(content=_format_roadmap(rm))], "roadmap_status": "awaiting_feedback"}

    def handle_feedback(state: PlanState) -> dict:
        feedback = next((m.content for m in reversed(state.get("messages", [])) if isinstance(m, HumanMessage)), "")
        prompt = (PLANNING_FEEDBACK_PROMPT_PATH.read_text(encoding="utf-8")
                  .replace("{student_model}", json.dumps(state.get("student_model", {}), ensure_ascii=False, indent=2))
                  .replace("{roadmap}", json.dumps(state.get("master_roadmap", {}), ensure_ascii=False, indent=2))
                  .replace("{feedback}", feedback))
        resp = llm_decide.invoke([HumanMessage(content=prompt)])
        if not resp.tool_calls:
            return {"feedback": feedback, "decision": "reply_to_student",
                    "decision_args": {"noi_dung": resp.content or "Bạn nói rõ hơn giúp mình nhé?"}}
        call = resp.tool_calls[0]
        print(f"[planning] quyết định: {call['name']} {call['args']}")
        return {"feedback": feedback, "decision": call["name"], "decision_args": call["args"]}

    def route_decision(state: PlanState) -> str:
        return {"approve_roadmap": "do_approve", "revise_roadmap": "do_revise",
                "request_profile_update": "do_profile_update"}.get(state["decision"], "do_reply")

    def do_reply(state: PlanState) -> dict:
        return {"messages": [AIMessage(content=state["decision_args"].get("noi_dung", ""))]}

    def do_approve(state: PlanState) -> dict:
        inbox = list(state.get("inbox", []))
        inbox.append(HandoffMessage(sender="planning", receiver="roadmap", type="result",
                                    payload={"master_roadmap": state["master_roadmap"]}).model_dump(mode="json"))
        return {"roadmap_status": "approved", "inbox": inbox,
                "messages": [AIMessage(content="Mình đã chốt sườn lộ trình.")]}

    def do_revise(state: PlanState) -> dict:
        n = state.get("revision_count", 0)
        if n >= MAX_REVISION:
            return {"messages": [AIMessage(content=f"Mình đã chỉnh {n} lần rồi. Bạn xem lại bản hiện tại, hoặc nói 'chốt' nếu đồng ý nhé.")]}
        return {"roadmap_status": "revising", "feedback": state["decision_args"].get("yeu_cau", state.get("feedback", "")),
                "revision_count": n + 1}

    def after_revise(state: PlanState) -> str:
        return "finalize" if state.get("roadmap_status") == "revising" else END

    def do_profile_update(state: PlanState) -> dict:
        args = state["decision_args"]
        inbox = list(state.get("inbox", []))
        inbox.append(HandoffMessage(sender="planning", receiver="collect", type="update_profile",
                                    payload=args).model_dump(mode="json"))
        return {"update_request": args, "inbox": inbox, "roadmap_status": "updating_profile",
                "messages": [AIMessage(content="Mình cần cập nhật lại thông tin của bạn trước khi chỉnh sườn.")]}

    g = StateGraph(PlanState)
    for name, fn in [("planner", planner), ("finalize", finalize), ("present_roadmap", present_roadmap),
                     ("handle_feedback", handle_feedback), ("do_reply", do_reply), ("do_approve", do_approve),
                     ("do_revise", do_revise), ("do_profile_update", do_profile_update)]:
        g.add_node(name, fn)

    g.add_conditional_edges(START, entry, {"planner": "planner", "handle_feedback": "handle_feedback"})
    g.add_edge("planner", "finalize")
    g.add_edge("finalize", "present_roadmap")
    g.add_edge("present_roadmap", END)
    g.add_conditional_edges("handle_feedback", route_decision,
                            {"do_reply": "do_reply", "do_approve": "do_approve",
                             "do_revise": "do_revise", "do_profile_update": "do_profile_update"})
    g.add_conditional_edges("do_revise", after_revise, {"finalize": "finalize", END: END})
    for n in ("do_reply", "do_approve", "do_profile_update"):
        g.add_edge(n, END)
    return g.compile(checkpointer=checkpointer)