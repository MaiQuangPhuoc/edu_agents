# from langchain_openai import OpenAIEmbeddings
# from src.configs import env_config

# embeddings = OpenAIEmbeddings(
#     model=env_config.embedding_model,
#     api_key=env_config.
# )


# from langchain.embeddings import HuggingFaceBgeEmbeddings
# embeddings = HuggingFaceBgeEmbeddings(
#     model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# )


# from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(
#     model_name="dangvantuan/vietnamese-embedding"
# )


# from sentence_transformers import SentenceTransformer
# embeddings_qa = SentenceTransformer('bkai-foundation-models/vietnamese-bi-encoder')

# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

# khởi tạo model embeddings (ví dụ dùng sentence-transformers)
embeddings_qa = HuggingFaceEmbeddings(
    model_name="bkai-foundation-models/vietnamese-bi-encoder"
)

print('Embeddings model initialized successfully.')
