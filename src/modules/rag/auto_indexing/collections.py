"""Create an empty collection with the requested book name and live schema."""

import copy
from .name_registry import DuplicateCollectionName, validate_name


def clone_collection_schema(client, template: str, destination: str) -> None:
    """Copy vector/index configuration, never template points or aliases."""
    from qdrant_client import models

    destination = validate_name(destination)
    if destination == template or client.collection_exists(destination):
        raise DuplicateCollectionName(f"Collection đích đã tồn tại: {destination}; hãy nhập tên khác.")
    info = client.get_collection(template)
    config = info.config
    params = config.params
    if not isinstance(params.vectors, dict) or "dense" not in params.vectors or "sparse" not in (params.sparse_vectors or {}):
        raise ValueError("Collection mẫu phải có named vectors 'dense' và 'sparse'.")
    options = {
        "vectors_config": copy.deepcopy(params.vectors),
        "sparse_vectors_config": copy.deepcopy(params.sparse_vectors),
        "on_disk_payload": params.on_disk_payload,
        "hnsw_config": models.HnswConfigDiff(**config.hnsw_config.model_dump()),
        "optimizers_config": models.OptimizersConfigDiff(**config.optimizer_config.model_dump()),
        "quantization_config": copy.deepcopy(config.quantization_config),
    }
    client.create_collection(collection_name=destination, **options)
    for field, schema in (info.payload_schema or {}).items():
        client.create_payload_index(destination, field,
                                    copy.deepcopy(schema.params) if schema.params is not None else schema.data_type,
                                    wait=True)
    for field in ('document_id', 'document_type', 'subject', 'chapter_id', 'textbook_series',
                  'section_types', 'content_type', 'sub_type'):
        key = f'metadata.{field}'
        existing = (info.payload_schema or {}).get(key)
        if existing is not None and existing.data_type != models.PayloadSchemaType.KEYWORD:
            raise ValueError(f'Index {key} của collection mẫu phải là keyword.')
        if existing is None:
            client.create_payload_index(destination, key, models.PayloadSchemaType.KEYWORD, wait=True)


def upload_new_collection(chunks: list[dict], *, destination: str,
                          template_collection: str | None = None, batch_size: int = 16,
                          client=None, embeddings=None, sparse_embedding=None) -> dict:
    """Only production entry point: one new collection for every run."""
    from src.modules.rag.process_toan_10.push_giao_an_qdrant import push_chunks
    owned = client is None
    if owned:
        from src.configs import env_config
        from qdrant_client import QdrantClient
        template_collection = template_collection or env_config.collect_name
        if not env_config.qdrant_url:
            raise ValueError("Chưa cấu hình QDRANT_URL.")
        client = QdrantClient(url=env_config.qdrant_url, api_key=env_config.qdrant_api_key,
                              check_compatibility=False)
    try:
        if not template_collection or not template_collection.strip():
            raise ValueError("Đặt COLLECT_NAME thành collection mẫu, hoặc truyền template_collection.")
        clone_collection_schema(client, template_collection, destination)
        result = push_chunks(chunks, collection_name=destination, batch_size=batch_size,
                               client=client, embeddings=embeddings, sparse_embedding=sparse_embedding)
        result["template_collection"] = template_collection
        result["created_new_collection"] = True
        return result
    finally:
        if owned:
            client.close()
