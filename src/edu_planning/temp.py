from dotenv import load_dotenv
load_dotenv()
import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType
from src.configs import env_config

client = QdrantClient(url=env_config.qdrant_url, api_key=env_config.qdrant_api_key, check_compatibility=False)
client.create_payload_index(collection_name="doc_final", field_name="metadata.sub_type",
                            field_schema=PayloadSchemaType.KEYWORD)
print("ok")