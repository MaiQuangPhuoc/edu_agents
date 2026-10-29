from pathlib import Path

# File này nằm tại: EDUAGENT/src/edu_qa/paths.py
# parents[0] = edu_qa, parents[1] = src, parents[2] = EDUAGENT (root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPT_DIR = PROJECT_ROOT / "prompt_edu" / "prompt"
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"PROMPT_DIR: {PROMPT_DIR}")



KNOWLEDGE_TOAN_PROMPT_PATH = PROMPT_DIR / "qa_knowledge_toan_prompt.txt"
KNOWLEDGE_VAN_PROMPT_PATH = PROMPT_DIR / "qa_knowledge_van_prompt.txt"
KNOWLEDGE_SU_PROMPT_PATH = PROMPT_DIR / "qa_knowledge_su_prompt.txt"
QA_RESPONSE_PROMPT_PATH = PROMPT_DIR / "qa_response_prompt.txt"
SOLVE_TOOL_SELECT_PROMPT_PATH = PROMPT_DIR / "qa_solve_tool_select_prompt.txt"
CHAT_LOG_PATH = PROMPT_DIR / "logs" / "chat_log.md"
SOLVE_LLM_FALLBACK_PROMPT_PATH = PROMPT_DIR / "qa_solve_llm_fallback_prompt.txt"

# ------ edu_exam ---
KNOWLEDGE_PROMPT_PATH = PROMPT_DIR / "build_knowledge_v2.txt"
ANALYZE_PROMPT_PATH = PROMPT_DIR / "analyze_knowledge_v2.txt"
COLLECT_INFO_PROMPT_PATH = PROMPT_DIR / "collect_info_v2.txt"
BUILD_MATRIX_PROMPT_PATH = PROMPT_DIR / "build_matrix_v2.txt"
BUILD_SPECS_PROMPT_PATH = PROMPT_DIR / "build_specs_v2.txt"
GENERATE_QUESTIONS_PROMPT_PATH = PROMPT_DIR / "generate_questions_v2.txt"
TEST_EXAM_PROMPT_PATH  = Path(r'D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\test_exam')
TOOL_SELECT_BATCH_PROMPT_PATH = PROMPT_DIR / "qa_solve_tool_select_batch_prompt.txt"


# planing
COLLECT_STUDENT_MODEL_PROMPT_PATH = PROMPT_DIR / "collect_student_model.txt"
PLANNING_PROMPT_PATH = PROMPT_DIR / "planning_agent.txt"
PLANNING_FINALIZE_PROMPT_PATH = PROMPT_DIR / "planning_finalize.txt"
PLANNING_FEEDBACK_PROMPT_PATH = PROMPT_DIR / "planning_feedback.txt"
GUARD_PROMPT_PATH = PROMPT_DIR / "guard.txt"
COLLECT_UPDATE_PROMPT_PATH = PROMPT_DIR / "collect_student_model_update.txt"
QUERY_TRANSFORM_PROMPT_PATH = PROMPT_DIR / "query_transform.txt"
LP_CHAPTER_KNOWLEDGE_PROMPT_PATH = PROMPT_DIR / "lp_chapter_knowledge.txt"


LP_RESOURCES_PROMPT_PATH = PROMPT_DIR / "lp_resources.txt"
LP_ASSEMBLE_PROMPT_PATH = PROMPT_DIR / "lp_assemble.txt"


LP_OUTLINE_PROMPT_PATH = PROMPT_DIR / "lp_outline.txt"
LP_REVIEW_PROMPT_PATH = PROMPT_DIR / "lp_review.txt"

LP_VERIFY_PROMPT_PATH = PROMPT_DIR / "lp_verify.txt"

PLANNING_OVERVIEW_PROMPT_PATH = PROMPT_DIR / "planning_overview.txt"

EXAM_COLLECT_AUTO_PROMPT_PATH = PROMPT_DIR / "exam_collect_auto.txt"





