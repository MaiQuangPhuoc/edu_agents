"""
Cấu hình chung cho prototype RIKAI — dựa trên configs.py do Auditor cung cấp,
điều chỉnh 2 điểm để phù hợp prototype chạy local, nhiều máy:
1. qdrant_url / qdrant_api_key chuyển thành Optional (Qdrant hiện là stub,
   chưa bắt buộc — theo đúng quyết định trước đó).
2. env_file dùng đường dẫn tương đối (cùng thư mục với file này) thay vì
   đường dẫn Windows cứng, để chạy được trên mọi máy.
"""
import os
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Đọc EDUAGENT/.env, không phụ thuộc vị trí đặt dự án.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH, encoding="utf-8-sig", override=False)


class EnvConfig(BaseSettings):
    # ── API keys (để trống nếu không dùng, không bắt buộc) ──
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    # anthropic_api_key: Optional[str] = None

    groq_api_key_1: Optional[str] = None
    groq_api_key_2: Optional[str] = None
    groq_api_key_3: Optional[str] = None
    groq_api_key_4: Optional[str] = None
    groq_api_key_5: Optional[str] = None
    groq_api_key_6: Optional[str] = None
    guard_model: str = "openai/gpt-oss-20b"      # model cho guard; đổi bằng GUARD_MODEL trong .env

    plan_model: str = "openai/gpt-6-luna"          # model cho bước sinh sườn; đổi bằng PLAN_MODEL
    plan_provider: Literal["openai", "groq", "openrouter"] = "openrouter"   # PLAN_PROVIDER


    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None   # tùy chọn: REASONING_EFFORT=low để giảm token suy luận
    llm_timeout_seconds: float = 60.0
    # Fixed is useful when measuring cache hits; round_robin preserves existing behavior.
    groq_key_strategy: Literal["round_robin", "fixed"] = "round_robin"
    openrouter_provider: Optional[str] = None
    llm_cache_key: Optional[str] = None
    # Enable only for reusable system/developer prefixes >= 1024 visible tokens.
    llm_explicit_cache: bool = False

    @property
    def groq_api_keys(self) -> list[str]:
        keys = [getattr(self, f"groq_api_key_{i}") for i in range(1, 7)]
        keys = [k for k in keys if k]
        return keys or ([self.groq_api_key] if self.groq_api_key else [])
    
    # tavily/weather giữ optional luôn cho an toàn
    api_key_tavily: Optional[str] = None
    api_key_weather: Optional[str] = None

    collect_name: str = ""
    # Gemini API
    # gemini_api_key: Optional[str] = None
    # gemini_model: str = "gemini-3.8-flash"

    # ── chọn provider đang dùng ──
    api_provider: Literal["openai", "groq", "openrouter", "anthropic","gemini"] = "groq"

    model: str = ""
    embedding_model: str = ""

    # Qdrant: OPTIONAL ở giai đoạn prototype này (core/vectorstore.py là stub,
    # REPORT_AGENT vẫn chạy tốt không cần Qdrant). Sẽ bắt buộc khi tích hợp thật.
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None
    qdrant_collection: str = ""

    # ── lộ trình chi tiết: LLM kiểm ngữ nghĩa tài nguyên (UI có thể ghi đè bằng state['lp_verify']) ──
    lp_verify: bool = True

    console_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    file_log_format: str = "%(asctime)s %(levelname)s %(message)s"
    console_log_format: str = "%(levelname)s %(message)s"


    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8-sig",
        extra="ignore",
        env_ignore_empty=True,
    )

env_config = EnvConfig()
from dotenv import dotenv_values

# Chỉ kiểm tra trạng thái, không in API key.
values = dotenv_values(ENV_PATH, encoding="utf-8-sig")

print("CONFIG_FILE:", Path(__file__).resolve())
print("ENV_PATH:", ENV_PATH)
print("ENV_EXISTS:", ENV_PATH.is_file())
print("FILE_HAS_QDRANT_URL:", bool(values.get("QDRANT_URL")))
print("CONFIG_HAS_QDRANT_URL:", bool(env_config.qdrant_url))
print("FILE_HAS_MODEL:", bool(values.get("MODEL")))
print("CONFIG_HAS_MODEL:", bool(env_config.model))

# ---------------------------------------------------------------------------
# Hằng số dùng chung ngoài phần LLM (đường dẫn lưu trữ local, giới hạn upload)
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
SAMPLE_DIR = os.path.join(DATA_DIR, "sample")
os.makedirs(SESSIONS_DIR, exist_ok=True)

MAX_UPLOAD_MB = 20


print("model",env_config.model)
# Never print API keys to logs.
print("tavily api key:", env_config.api_key_tavily is not None)
# print("qdrant url:", env_config.qdrant_collection)
# print("open api key:", env_config.openai_api_key)
# print("gemini model:", env_config.gemini_model)

