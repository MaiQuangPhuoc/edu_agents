from dotenv import load_dotenv
load_dotenv()
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from src.edu_qa.tools.tools_search_media import search_youtube_lecture
from src.clients.llm import LLMClient
from src.configs import env_config

llm_client = LLMClient(model=env_config.model, api_provider=env_config.api_provider)

results = search_youtube_lecture.invoke({
    "query": "phương trình bậc hai toán 10",
    "llm_client": llm_client,
    "max_results": 2
})
for r in results:
    print(r)