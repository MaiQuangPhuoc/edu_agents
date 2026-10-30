"""Chunk giáo án Markdown và push Qdrant. Có thể gọi từ UI hoặc chạy riêng."""
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).resolve().parents[4]
LESSON_PLAN_DIR = ROOT_DIR / 'src/modules/documents/lesson_plans/chan_troi_sang_tao/lich_su_10'


def build_all_chunks(folder=LESSON_PLAN_DIR, *, files=None, on_progress=None):
    from src.modules.rag.process_toan_10.chunk_markdown_giao_an import chunk_file
    paths = [Path(path) for path in files] if files is not None else sorted(Path(folder).glob('*.md'))
    if not paths:
        raise ValueError(f'Không tìm thấy file .md trong: {folder}')
    chunks = []
    for file_index, path in enumerate(paths, 1):
        result = chunk_file(path)
        chunks.extend(result['chunks'])
        print(f'{path.name}: {len(result["chunks"])} chunks')
        if on_progress:
            on_progress({'stage': 'chunking_prepared_markdown', 'message': f'{path.name}: {len(result["chunks"])} chunks',
                         'current': file_index, 'total': len(paths), 'total_chunks': len(chunks)})
    return chunks


def point_id(chunk):
    metadata = chunk['metadata']
    fields = ('document_id', 'document_type', 'subject', 'textbook_series', 'chunk_id')
    if any(not metadata.get(key) for key in fields):
        raise ValueError('Chunk thiếu metadata để tạo ID.')
    identity = '\x1f'.join(str(metadata[key]) for key in fields)
    if metadata.get('lesson_plan_id'):
        identity += '\x1f' + str(metadata['lesson_plan_id'])
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'eduagent:prepared_markdown:' + identity))


def push_chunks(chunks, *, collection_name, batch_size=16, client=None,
                embeddings=None, sparse_embedding=None, on_progress=None):
    """Push các chunk vào collection đã tạo; IDs ổn định trong collection đó."""
    if not chunks or batch_size < 1:
        raise ValueError('Cần có chunks và batch_size > 0.')
    ids = [point_id(chunk) for chunk in chunks]
    if len(set(ids)) != len(ids):
        raise ValueError('Trùng chunk ID; chưa upload.')
    from langchain_core.documents import Document
    from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse
    from qdrant_client import QdrantClient
    owned = client is None
    if owned:
        from src.configs import env_config
        client = QdrantClient(url=env_config.qdrant_url, api_key=env_config.qdrant_api_key, check_compatibility=False)
    try:
        info = client.get_collection(collection_name)
        vectors = info.config.params.vectors
        if not isinstance(vectors, dict) or 'dense' not in vectors or 'sparse' not in (info.config.params.sparse_vectors or {}):
            raise ValueError("Collection phải có named vectors 'dense' và 'sparse'.")
        if on_progress:
            on_progress({'stage': 'preparing_index', 'message': 'Chuẩn bị mô hình embedding và tìm kiếm kết hợp.'})
        if embeddings is None:
            from src.clients.embedding import embeddings_qa
            embeddings = embeddings_qa
        store = QdrantVectorStore(client=client, collection_name=collection_name,
            embedding=embeddings, vector_name='dense', sparse_vector_name='sparse',
            retrieval_mode=RetrievalMode.HYBRID, distance=vectors['dense'].distance,
            sparse_embedding=sparse_embedding if sparse_embedding is not None else FastEmbedSparse(model_name='Qdrant/bm25'))
        if on_progress:
            on_progress({'stage': 'uploading_prepared_markdown', 'message': f'Bắt đầu xử lý {len(chunks)} chunks.', 'current': 0, 'total': len(chunks)})
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            store.add_documents([Document(page_content=c['content'], metadata=c['metadata']) for c in batch],
                                ids=ids[start:start + batch_size], batch_size=batch_size)
            if on_progress:
                done = start + len(batch)
                on_progress({'stage': 'uploading_prepared_markdown', 'message': f'Đã embedding và ghi {done}/{len(chunks)} chunks.',
                             'current': done, 'total': len(chunks)})
        return {'collection_name': collection_name, 'uploaded_chunks': len(chunks),
                'point_ids': ids, 'source_mode': 'prepared_markdown'}
    finally:
        if owned:
            client.close()


def main():
    from src.configs import env_config
    if not env_config.collect_name.strip():
        raise ValueError('Chưa cấu hình COLLECT_NAME trong src/.env')
    result = push_chunks(build_all_chunks(), collection_name=env_config.collect_name)
    print(f"Đã upload {result['uploaded_chunks']} chunks giáo án.")


if __name__ == '__main__':
    main()
