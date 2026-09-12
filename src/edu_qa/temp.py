# from qdrant_client import QdrantClient
# import sys, os, asyncio
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# from dotenv import load_dotenv
# from qdrant_client.models import PayloadSchemaType
# from src.configs import env_config

# client = QdrantClient(url=env_config.qdrant_url, api_key=env_config.qdrant_api_key)

# client.create_payload_index(
#     collection_name="doc_final",
#     field_name="metadata.subject",
#     field_schema=PayloadSchemaType.KEYWORD,
# )
# print("Đã tạo index cho metadata.subject")

# import torch
# from sentence_transformers import CrossEncoder

# print("CUDA khả dụng:", torch.cuda.is_available())

# # Khởi tạo mô hình (thay tên mô hình bạn đang dùng)
# reranker = CrossEncoder("BAAI/bge-reranker-base")

# # Kiểm tra thiết bị thực tế
# print("Thiết bị mô hình đang chạy:", reranker.model.device)

print("OK")