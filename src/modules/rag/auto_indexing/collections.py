"""Upload every lesson plan into one configured Qdrant collection."""
DEFAULT_COLLECTION_NAME = 'doc_final'


def validate_qdrant_configuration():
    from src.configs import env_config
    url = (env_config.qdrant_url or '').strip()
    name = (env_config.collect_name or DEFAULT_COLLECTION_NAME).strip() or DEFAULT_COLLECTION_NAME
    if not url:
        raise ValueError('Chưa cấu hình QDRANT_URL trong src/.env. Khởi động lại UI sau khi sửa .env.')
    return url, env_config.qdrant_api_key, name


def ensure_collection(client, collection_name, embeddings=None):
    """Use an existing hybrid collection; create only when absent, never recreate."""
    from qdrant_client import models
    if not client.collection_exists(collection_name):
        if embeddings is None:
            from src.clients.embedding import embeddings_qa
            embeddings = embeddings_qa
        dimension = len(embeddings.embed_query('Kiểm tra kích thước embedding'))
        client.create_collection(collection_name=collection_name,
            vectors_config={'dense': models.VectorParams(size=dimension, distance=models.Distance.COSINE)},
            sparse_vectors_config={'sparse': models.SparseVectorParams(modifier=models.Modifier.IDF)})
    info = client.get_collection(collection_name)
    vectors = info.config.params.vectors
    if not isinstance(vectors, dict) or 'dense' not in vectors or 'sparse' not in (info.config.params.sparse_vectors or {}):
        raise ValueError("Collection phải có named vectors 'dense' và 'sparse'; không tự ghi đè cấu trúc đang có.")
    for field in ('document_id', 'document_type', 'subject', 'chapter_id', 'textbook_series',
                  'section_types', 'content_type', 'sub_type', 'lesson_plan_name', 'lesson_plan_id'):
        key = f'metadata.{field}'
        existing = (info.payload_schema or {}).get(key)
        if existing is not None and existing.data_type != models.PayloadSchemaType.KEYWORD:
            raise ValueError(f'Index {key} phải là keyword.')
        if existing is None:
            client.create_payload_index(collection_name, key, models.PayloadSchemaType.KEYWORD, wait=True)


def upload_to_default_collection(chunks, *, batch_size=16, client=None, embeddings=None,
                                 sparse_embedding=None, collection_name=None, on_progress=None):
    from src.modules.rag.process_toan_10.push_giao_an_qdrant import push_chunks
    owned = client is None
    if owned:
        from qdrant_client import QdrantClient
        url, api_key, configured_name = validate_qdrant_configuration()
        collection_name = configured_name
        client = QdrantClient(url=url, api_key=api_key, check_compatibility=False)
    collection_name = collection_name or DEFAULT_COLLECTION_NAME
    try:
        if on_progress:
            on_progress({'stage': 'preparing_index', 'message': f'Kiểm tra collection {collection_name} và các index metadata.'})
        ensure_collection(client, collection_name, embeddings)
        return push_chunks(chunks, collection_name=collection_name, batch_size=batch_size,
                           client=client, embeddings=embeddings, sparse_embedding=sparse_embedding, on_progress=on_progress)
    finally:
        if owned:
            client.close()
