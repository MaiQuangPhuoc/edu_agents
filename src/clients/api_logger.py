import os
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from langchain_core.callbacks import BaseCallbackHandler

LOG_DIR = Path(os.getenv("EDU_API_LOG_DIR", str(Path(__file__).resolve().parents[2] / "logs" / "api_usage")))
HEADER = ("| NO | Gửi | Provider | Model | Input | Cached | Output | Nhận | Tổng (s) | Server (s) | Mạng ≈ (s) | Lỗi |\n"
          "|---:|---|---|---|---:|---:|---:|---|---:|---:|---:|---|\n")
_lock = threading.Lock()
# Giá USD / 1 triệu token: (input chưa cache, input từ cache, output). Groq không tính tiền.
PRICES = {"gpt-6-luna": (0.10, 0.01, 0.50)}

def _write_row(sent: datetime, cells: list):
    path = LOG_DIR / f"{sent:%Y-%m-%d}.md"
    with _lock:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        new = not path.exists()
        no = 1 if new else 1 + sum(1 for l in path.read_text(encoding="utf-8").splitlines()
                                   if l.startswith("| ") and l[2:3].isdigit())
        with path.open("a", encoding="utf-8") as f:
            if new:
                f.write(f"# Nhật ký gọi API {sent:%Y-%m-%d}\n\n{HEADER}")
            f.write("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in [no] + cells) + " |\n")


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


def _price(model: str):
    return next((p for k, p in PRICES.items() if k in model), None)


def usage_summary(day: str | None = None) -> dict:
    """Thống kê theo model và cả ngày. day dạng 'YYYY-MM-DD', mặc định hôm nay."""
    day = day or f"{datetime.now():%Y-%m-%d}"
    path = LOG_DIR / f"{day}.md"
    keys = ("calls", "input", "cached", "fresh", "output", "cost")
    per = defaultdict(lambda: dict.fromkeys(keys, 0))
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            off = 1 if c and c[0].isdigit() else 0             # file cũ chưa có cột NO
            if not line.startswith("| ") or len(c) < 6 + off or not c[off].startswith("20"):
                continue
            i, ca, o = _num(c[off + 3]), _num(c[off + 4]), _num(c[off + 5])
            r = per[c[off + 2]]
            r["calls"] += 1
            r["input"] += i
            r["cached"] += ca
            r["fresh"] += max(i - ca, 0)                         # input không từ cache
            r["output"] += o
            p = _price(c[off + 2])
            if p:
                r["cost"] += (max(i - ca, 0) * p[0] + ca * p[1] + o * p[2]) / 1_000_000
    total = {k: sum(r[k] for r in per.values()) for k in keys}
    return {"day": day, "models": dict(per), "all": total}


def print_usage_summary(day: str | None = None):
    s = usage_summary(day)
    print(f"Thống kê ngày {s['day']}")
    for m, r in {**s["models"], "TỔNG": s["all"]}.items():
        cost = f" | ${r['cost']:.4f}" if _price(m) else ""
        print(f"- {m}: {r['calls']} lần | in {r['input']} (cache {r['cached']}, chưa cache {r['fresh']}) | out {r['output']}{cost}")
    print(f"Tổng tiền (chỉ model có giá niêm yết): ${s['all']['cost']:.4f}")

if __name__ == "__main__":
    print_usage_summary(sys.argv[1] if len(sys.argv) > 1 else None)