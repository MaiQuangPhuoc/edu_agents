import os
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from langchain_core.callbacks import BaseCallbackHandler

LOG_DIR = Path(os.getenv("EDU_API_LOG_DIR", str(Path(__file__).resolve().parents[2] / "logs" / "api_usage")))
HEADER = ("| Gửi | Provider | Model | Input | Cached | Output | Nhận | Tổng (s) | Server (s) | Mạng ≈ (s) | Lỗi |\n"
          "|---|---|---|---:|---:|---:|---|---:|---:|---:|---|\n")
_lock = threading.Lock()


def _write_row(sent: datetime, cells: list):
    path = LOG_DIR / f"{sent:%Y-%m-%d}.md"
    with _lock:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        new = not path.exists()
        with path.open("a", encoding="utf-8") as f:
            if new:
                f.write(f"# Nhật ký gọi API {sent:%Y-%m-%d}\n\n{HEADER}")
            f.write("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in cells) + " |\n")


class ApiLogHandler(BaseCallbackHandler):
    """Ghi mỗi lần gọi LLM thành một dòng bảng trong logs/api_usage/YYYY-MM-DD.md."""

    def __init__(self, provider: str, model: str):
        self.provider, self.model = provider, model
        self._start = {}

    def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        self._start[run_id] = (time.perf_counter(), datetime.now())

    def on_llm_start(self, serialized, prompts, *, run_id, **kwargs):
        self._start[run_id] = (time.perf_counter(), datetime.now())

    def on_llm_end(self, response, *, run_id, **kwargs):
        t0, sent = self._start.pop(run_id, (None, None))
        if t0 is None:
            return
        total = time.perf_counter() - t0
        msg = None
        if response.generations and response.generations[0]:
            msg = getattr(response.generations[0][0], "message", None)
        usage = (getattr(msg, "usage_metadata", None) or {})
        meta = (getattr(msg, "response_metadata", None) or {})
        tu = meta.get("token_usage") or {}
        cached = (usage.get("input_token_details") or {}).get("cache_read")
        if cached is None:
            cached = (tu.get("prompt_tokens_details") or {}).get("cached_tokens")
        server = tu.get("total_time")            # chỉ Groq trả về
        net = f"{max(total - server, 0):.2f}" if server is not None else "-"
        _write_row(sent, [f"{sent:%Y-%m-%d %H:%M:%S}", self.provider, meta.get("model_name") or self.model,
                          usage.get("input_tokens", tu.get("prompt_tokens", "-")),
                          cached if cached is not None else "-",
                          usage.get("output_tokens", tu.get("completion_tokens", "-")),
                          f"{datetime.now():%H:%M:%S}", f"{total:.2f}",
                          f"{server:.2f}" if server is not None else "-", net, ""])

    def on_llm_error(self, error, *, run_id, **kwargs):
        t0, sent = self._start.pop(run_id, (None, None))
        if t0 is None:
            return
        _write_row(sent, [f"{sent:%Y-%m-%d %H:%M:%S}", self.provider, self.model, "-", "-", "-",
                          f"{datetime.now():%H:%M:%S}", f"{time.perf_counter() - t0:.2f}", "-", "-",
                          f"{type(error).__name__}: {str(error)[:120]}"])


def _num(s: str) -> int:
    s = s.strip()
    return int(s) if s.isdigit() else 0


def usage_summary(day: str | None = None) -> dict:
    """Tổng token theo từng model và cả ngày. day dạng 'YYYY-MM-DD', mặc định hôm nay."""
    day = day or f"{datetime.now():%Y-%m-%d}"
    path = LOG_DIR / f"{day}.md"
    per = defaultdict(lambda: {"calls": 0, "input": 0, "output": 0, "total": 0})
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| 20"):
                continue
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            row = per[c[2]]
            i, o = _num(c[3]), _num(c[5])
            row["calls"] += 1
            row["input"] += i
            row["output"] += o
            row["total"] += i + o
    total = {k: sum(r[k] for r in per.values()) for k in ("calls", "input", "output", "total")}
    return {"day": day, "models": dict(per), "all": total}


def print_usage_summary(day: str | None = None):
    s = usage_summary(day)
    print(f"Tổng token ngày {s['day']}")
    for m, r in s["models"].items():
        print(f"- {m}: {r['calls']} lần | in {r['input']} | out {r['output']} | total {r['total']}")
    a = s["all"]
    print(f"- TỔNG: {a['calls']} lần | in {a['input']} | out {a['output']} | total {a['total']}")


if __name__ == "__main__":
    print_usage_summary(sys.argv[1] if len(sys.argv) > 1 else None)