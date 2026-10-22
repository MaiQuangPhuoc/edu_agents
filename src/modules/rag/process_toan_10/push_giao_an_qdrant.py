"""Đặt tại src/modules/rag/process_toan_10/push_giao_an_qdrant.py.
Chạy: python -m src.modules.rag.process_toan_10.push_giao_an_qdrant
Không cần xuất hoặc đọc file JSON trung gian.
"""
import sys
from pathlib import Path
from langchain_core.documents import Document
from src.modules.rag.vectorstores2 import VectorStoreManager
from src.configs import env_config


ROOT_DIR = Path(__file__).resolve().parents[4]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Chỉ sửa đường dẫn tương đối này nếu thư mục giáo án nằm nơi khác.
LESSON_PLAN_DIR = (
    ROOT_DIR / 'src' / 'modules' / 'documents' / 'lesson_plans'
    / 'chan_troi_sang_tao' / 'toan_10'
)


def build_all_chunks(folder=LESSON_PLAN_DIR):
    from src.modules.rag.process_toan_10.chunk_markdown_giao_an import chunk_file

    files = sorted(Path(folder).glob('*.md'))
    if not files:
        raise ValueError(f'Không tìm thấy file .md trong: {folder}')
    all_chunks = []
    for file_path in files:
        result = chunk_file(file_path)
        all_chunks.extend(result['chunks'])
        print(f'{file_path.name}: {len(result["chunks"])} chunks')
    return all_chunks


def main():


    if not env_config.collect_name.strip():
        raise ValueError('Chưa cấu hình COLLECT_NAME trong .env')
    all_chunks = build_all_chunks()
    documents = [
        Document(
            page_content=chunk['content'],
            metadata=chunk['metadata'],
        )
        for chunk in all_chunks
    ]
    if not documents:
        raise ValueError('Không có chunk để upload')

    from src.clients.embedding import embeddings_qa

    vector_manager = VectorStoreManager(
        url=env_config.qdrant_url,
        api_key=env_config.qdrant_api_key,
    )
    vector_manager.create_vector_store(
        documents=documents,
        embeddings=embeddings_qa,
        collection_name=env_config.collect_name,
    )
    print(f'Đã upload {len(documents)} chunks giáo án.')


if __name__ == '__main__':
    main()
