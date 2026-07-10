from langchain_qdrant import QdrantVectorStore
import sys , os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from pymongo import MongoClient
from src.configs import env_config

from src.clients.embedding import embeddings, embeddings_qa

# mongo_client = MongoClient(
#     host=env_config.mongodb_uri
# )

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    api_key = env_config.qdrant_api_key,
    collection_name="documents_new",
    url=env_config.qdrant_url
)

# qdrant_overview = QdrantVectorStore.from_existing_collection(
#     embedding=embeddings_1,
#     api_key = env_config.qdrant_api_key,
#     collection_name="documents",
#     url=env_config.qdrant_url
# )

qdrant_qa = QdrantVectorStore.from_existing_collection(
    embedding=embeddings_qa,
    api_key = env_config.qdrant_api_key,
    collection_name="toan_10",
    url=env_config.qdrant_url
)
