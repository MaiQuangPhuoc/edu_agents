import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))   # chỉnh theo vị trí file
from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType
from src.configs import env_config

client = QdrantClient(url=env_config.qdrant_url, api_key=env_config.qdrant_api_key, check_compatibility=False)
for key in ["metadata.document_type", "metadata.subject", "metadata.chapter_id", "metadata.section_types"]:
    client.create_payload_index(collection_name="doc_final", field_name=key, field_schema=PayloadSchemaType.KEYWORD)
    print("đã tạo index:", key)