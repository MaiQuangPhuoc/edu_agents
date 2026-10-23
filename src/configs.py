"""
Cấu hình chung cho prototype RIKAI — dựa trên configs.py do Auditor cung cấp,
điều chỉnh 2 điểm để phù hợp prototype chạy local, nhiều máy:
1. qdrant_url / qdrant_api_key chuyển thành Optional (Qdrant hiện là stub,
   chưa bắt buộc — theo đúng quyết định trước đó).
2. env_file dùng đường dẫn tương đối (cùng thư mục với file này) thay vì
   đường dẫn Windows cứng, để chạy được trên mọi máy.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional
import os



class EnvConfig(BaseSettings):
    # ── API keys (để trống nếu không dùng, không bắt buộc) ──
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    # anthropic_api_key: Optional[str] = None

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

    console_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    file_log_format: str = "%(asctime)s %(levelname)s %(message)s"
    console_log_format: str = "%(levelname)s %(message)s"


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        extra="ignore",
        env_ignore_empty=True,
    )

env_config = EnvConfig()


# ---------------------------------------------------------------------------
# Hằng số dùng chung ngoài phần LLM (đường dẫn lưu trữ local, giới hạn upload)
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
SAMPLE_DIR = os.path.join(DATA_DIR, "sample")
os.makedirs(SESSIONS_DIR, exist_ok=True)

MAX_UPLOAD_MB = 20


print("model",env_config.model)
print("api key:", env_config.openrouter_api_key)
# print("tavily api key:", env_config.api_key_tavily)
# print("qdrant url:", env_config.qdrant_collection)
# print("open api key:", env_config.openai_api_key)
# print("gemini model:", env_config.gemini_model)
