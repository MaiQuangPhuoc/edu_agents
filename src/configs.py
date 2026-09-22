
from pydantic_settings import BaseSettings
from typing import Literal, Optional
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class EnvConfig(BaseSettings):
    # ── API keys (để trống nếu không dùng, không bắt buộc) ──
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None

    # tavily/weather giữ optional luôn cho an toàn
    api_key_tavily: Optional[str] = None
    api_key_weather: Optional[str] = None

    # ── chọn provider đang dùng ──
    api_provider: Literal["openai", "groq", "openrouter"] = "openai"

    model: str
    embedding_model: str = ""

    qdrant_url: str
    qdrant_api_key: str

    console_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    file_log_format: str = "%(asctime)s %(levelname)s %(message)s"
    console_log_format: str = "%(levelname)s %(message)s"

    class Config:
        env_file = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\.env"
        extra = "ignore"

env_config = EnvConfig()

# from src.app_logging import setup_logging
# setup_logging()
# print(env_config.model)
# print(env_config.openrouter_api_key)