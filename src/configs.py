from pydantic_settings import BaseSettings
from typing import Literal
import os , sys 
# ==

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
class EnvConfig(BaseSettings):
    # OpenAI API
    # openai_api_key: str
    api_key_tavily: str
    google_api_key: str
    # groq_api_key: str
    model: str
    embedding_model: str =""
    # api_provider: Literal["openai", "anthropic", "google", "groq"] = "groq"
    api_provider: Literal["openai", "anthropic", "google", "groq"] = "google"


    # MongoDB
    # mongodb_uri: str = "mongodb://localhost:27017"
    
    # #QdrantDB
    # qdrant_url: str = "http://localhost:6333"  
    qdrant_url: str  
    qdrant_api_key: str  
    
    # Logging
    console_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    file_log_format: str = "%(asctime)s %(levelname)s %(message)s"
    console_log_format: str = "%(levelname)s %(message)s"
    
    class Config:
        env_file = r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\.env"
        #  env_file = os.path.join(os.path.dirname(__file__), ".env")

env_config = EnvConfig()

# Setup logging after config is loaded
from src.app_logging import setup_logging
setup_logging()
# print(env_config.model)
# print(env_config.qdrant_url)
# print(env_config.qdrant_api_key)
            
# print(env_config.api_key_tavily)

