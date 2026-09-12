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
