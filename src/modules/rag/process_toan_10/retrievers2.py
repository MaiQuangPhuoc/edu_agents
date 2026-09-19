# src/modules/rag/retrievers.py
import os
import sys
print("Python đang chạy:", sys.executable)
# os.environ["FASTEMBED_CACHE_PATH"] = r"C:\Users\Phuoc\fastembed_cache"
import logging
import torch
import time
from langchain_qdrant import QdrantVectorStore, RetrievalMode, FastEmbedSparse
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import CrossEncoder
from fastembed import LateInteractionTextEmbedding
import numpy as np
logger = logging.getLogger(__name__)


class VectorStoreRetriever:
    def __init__(
        self,
        url: str,
        api_key: str,
        embeddings: Embeddings,
        collection_name: str = "tools",
        tools_collection_name: str | None = None,
        top_k: int = 10,
        reranker_model = "BAAI/bge-reranker-v2-m3",
        enable_colbert_prefilter: bool = False,
        colbert_model: str = "colbert-ir/colbertv2.0",
    ):

        self._client = QdrantClient(
            url=url,
            api_key=api_key,
            check_compatibility=False,
        )

        # Semantic search (dense only)
        self._dense_store = QdrantVectorStore(
            client=self._client,
            collection_name=collection_name,
            embedding=embeddings,
            vector_name="dense",
            retrieval_mode=RetrievalMode.DENSE,
        )

        # Text search (sparse only)
        self._sparse_store = QdrantVectorStore(
            client=self._client,
            collection_name=collection_name,
            embedding=embeddings,
            vector_name="dense",
            sparse_vector_name="sparse",
            retrieval_mode=RetrievalMode.SPARSE,
            sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
        )

        # Hybrid search
        self._hybrid_store = QdrantVectorStore(
            client=self._client,
            collection_name=collection_name,
            embedding=embeddings,
            vector_name="dense",
            sparse_vector_name="sparse",
            retrieval_mode=RetrievalMode.HYBRID,
            sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
        )

        # Tools store (collection riêng, dùng chung client + reranker)
        self._tools_store = None
        if tools_collection_name:
            self._tools_store = QdrantVectorStore(
                client=self._client,
                collection_name=tools_collection_name,
                embedding=embeddings,
                vector_name="dense",
                sparse_vector_name="sparse",
                retrieval_mode=RetrievalMode.HYBRID,
                sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
            )

        self.top_k = top_k


        self.enable_colbert_prefilter = enable_colbert_prefilter
        self._colbert = LateInteractionTextEmbedding(colbert_model) if enable_colbert_prefilter else None

        # Reranker
        # self._reranker = CrossEncoder(reranker_model)
        # logger.info(f"Reranker loaded: {reranker_model}")

        # Reranker — tự động dùng GPU nếu có
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._reranker = CrossEncoder(reranker_model, device=device)
        if device == "cuda":
            self._reranker.model.half()
        print(f"Using device: {device}")

    

    # def filter_by_subject(docs: list, subject: str) -> list:
    #     """Chỉ giữ chunk có metadata['subject'] == subject."""
    #     return [d for d in docs if d.metadata.get("subject") == subject]

    # def _build_filter(
    #     self,
    #     subject: str | None = None,
    #     use_filter: bool = True,
    # ) -> Filter | None:
    #     """Build Qdrant filter theo subject. use_filter=False => tắt filter, trả None."""
    #     if not use_filter or not subject:
    #         return None
    #     return Filter(must=[FieldCondition(key="metadata.subject", match=MatchValue(value=subject))])

    def filter_by_subject(self, docs: list, subject: str) -> list:
        """Chỉ giữ chunk có metadata['subject'] == subject."""
        return [d for d in docs if d.metadata.get("subject") == subject]
    
    def semantic_search(self, query: str, subject: str | None = None, use_filter: bool = True) -> list[Document]:
        fetch_k = self.top_k * 5 if (use_filter and subject) else self.top_k
        results = self._dense_store.similarity_search(query, k=fetch_k)
        if use_filter and subject:
            results = self.filter_by_subject(results, subject)[: self.top_k]
        print(f" ========== semantic search : {len(results)} ========== ")
        return results

    def text_search(self, query: str, subject: str | None = None, use_filter: bool = True) -> list[Document]:
        fetch_k = self.top_k * 5 if (use_filter and subject) else self.top_k
        results = self._sparse_store.similarity_search(query, k=fetch_k)
        if use_filter and subject:
            results = self.filter_by_subject(results, subject)[: self.top_k]
        print(f" ========== Text search : {len(results)} ========== ")
        return results

    def hybrid_search(self, query: str, subject: str | None = None, use_filter: bool = True) -> list[Document]:
        fetch_k = self.top_k * 5 if (use_filter and subject) else self.top_k
        results = self._hybrid_store.similarity_search(query, k=fetch_k)
        if use_filter and subject:
            results = self.filter_by_subject(results, subject)[: self.top_k]
        print(f" ========== hibird search : {len(results)} ========== ")
        return results

    def hybrid_search_qa(
        self, query: str, k: int | None = None, subject: str | None = None, use_filter: bool = True
    ) -> list[Document]:
        base_k = k or self.top_k
        fetch_k = base_k * 5 if (use_filter and subject) else base_k
        results = self._hybrid_store.similarity_search(query, k=fetch_k)
        if use_filter and subject:
            results = self.filter_by_subject(results, subject)[:base_k]
        print(f" ========== hibird search : {len(results)} ========== ")
        return results

    def hybrid_search_tools(self, query: str, k: int | None = None) -> list[Document]:
        """Tìm kiếm trong collection tools (hybrid semantic + BM25)."""
        if self._tools_store is None:
            raise ValueError("tools_collection_name chưa được cấu hình khi khởi tạo retriever")
        results = self._tools_store.similarity_search(query, k=k or self.top_k)
        print(f" ========== tools search : {len(results)} ========== ")
        return results
    
    #new methods for colbert prefilter and rerank
    def colbert_prefilter(self, query: str, docs: list[Document], keep_top: int = 10) -> list[Document]:
        """[THỬ NGHIỆM] Dùng ColBERT (late-interaction) lọc bớt docs trước khi vào CrossEncoder."""
        if not self._colbert or not docs:
            return docs
        query_emb = list(self._colbert.query_embed(query))[0]
        doc_embs = list(self._colbert.embed([d.page_content for d in docs]))
        scores = [float(np.sum(np.max(np.matmul(query_emb, de.T), axis=1))) for de in doc_embs]
        ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
        return [d for _, d in ranked[:keep_top]]

    
    # def rerank(self, query: str, docs: list, top_k: int = 3) -> list[Document]:
    #     if not docs:
    #         return []

    #     if self.enable_colbert_prefilter:
    #         before_count = len(docs)
    #         docs = self.colbert_prefilter(query, docs, keep_top=max(top_k * 3, 10))
    #         print(f" ========== ColBERT prefilter: {before_count} -> {len(docs)} docs ========== ")

    #     pairs = [[query, doc.page_content] for doc in docs]
    #     scores = self._reranker.predict(pairs)

    #     ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)

    #     # logger.info(f"Rerank scores: {[round(float(s), 4) for s, _ in ranked]}")
    #     print(f" ========== Rerank scores: {[round(float(s), 4) for s, _ in ranked]} ========== ")

    #     top_docs = []
    #     for score, doc in ranked[:top_k]:
    #         doc.metadata["rerank_score"] = float(score)
    #         top_docs.append(doc)
    #     return top_docs


    def rerank(self, query: str, docs: list, top_k: int = 3) -> list[Document]:
        if not docs:
            return []

        if self.enable_colbert_prefilter:
            before_count = len(docs)
            start = time.perf_counter()
            docs = self.colbert_prefilter(query, docs, keep_top=max(top_k * 3, 10))
            elapsed = time.perf_counter() - start
            print(f" ========== ColBERT prefilter: {before_count} -> {len(docs)} docs -> {elapsed:.0f}s ========== ")

        start = time.perf_counter()
        pairs = [[query, doc.page_content] for doc in docs]
        # scores = self._reranker.predict(pairs)
        scores = self._reranker.predict(pairs, batch_size=1)
        torch.cuda.empty_cache()
        elapsed = time.perf_counter() - start

        ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)

        print(f" ========== Rerank scores -> {elapsed:.0f}s: {[round(float(s), 4) for s, _ in ranked]} ========== ")

        top_docs = []
        for score, doc in ranked[:top_k]:
            doc.metadata["rerank_score"] = float(score)
            top_docs.append(doc)
        return top_docs


    # def rerank(self, query: str, docs: list, top_k: int = 3) -> list[Document]:
    #     """Rerank docs bằng cross-encoder, chỉ giữ top_k chính xác nhất."""
    #     if not docs:
    #         return []

    #     pairs = [[query, doc.page_content] for doc in docs]
    #     scores = self._reranker.predict(pairs)

    #     ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)

    #     # logger.info(f"Rerank scores: {[round(float(s), 4) for s, _ in ranked]}")
    #     print(f" ========== Rerank scores: {[round(float(s), 4) for s, _ in ranked]} ========== ")

    #     top_docs = []
    #     for score, doc in ranked[:top_k]:
    #         doc.metadata["rerank_score"] = float(score)
    #         top_docs.append(doc)
    #     return top_docs
    
