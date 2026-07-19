from pathlib import Path

# File này nằm tại: EDUAGENT/src/edu_qa/paths.py
# parents[0] = edu_qa, parents[1] = src, parents[2] = EDUAGENT (root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPT_DIR = PROJECT_ROOT / "prompt_edu" / "prompt"
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"PROMPT_DIR: {PROMPT_DIR}")