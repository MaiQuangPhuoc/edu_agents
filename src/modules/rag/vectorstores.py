import logging 
from typing import Dict, List, Optional
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
# from langchain_openai import OpenAIEmbeddings
# from src.configs import env_config
# from src.clients.embedding import embeddings
# import sys , os 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".." "..")))

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """
    Manager for vector store operations using Qdrant.
    
    This class provides a high-level interface for creating and managing
    vector stores for document retrieval in RAG pipelines.
    """
    
    def __init__(
        self, 
        url: str,
        api_key: Optional[str] = None,
        prefer_grpc: bool = True
    ):
        """
        Initialize the VectorStoreManager.
        
        Args:
            url: Qdrant server URL
            api_key: Optional API key for authentication
            prefer_grpc: Whether to prefer gRPC over HTTP
        """
        self.url = url
        self.api_key = api_key
        self.prefer_grpc = prefer_grpc
        
        logger.info(f"VectorStoreManager initialized with URL: {url}")
    
    def create_vector_store(
        self,
        documents: List[Document],
        embeddings: Embeddings,
        collection_name: str = "documents_dangvantuan"
    ) -> QdrantVectorStore:
      
        if not documents:
            raise ValueError("Documents list cannot be empty")

        
        if not embeddings:
            raise ValueError("Embeddings model is required")
            
        try:
            vector_store = QdrantVectorStore.from_documents(
                documents,
                embeddings,
                url=self.url,
                prefer_grpc=self.prefer_grpc,
                api_key=self.api_key,
                collection_name=collection_name,
            )
            
            logger.info(f"Created vector store with {len(documents)} documents "
                       f"in collection '{collection_name}'")
            return vector_store
            
        except Exception as e:
            logger.error(f"Failed to create vector store: {str(e)}")
            raise
    
    def get_client(self) -> QdrantClient:
        """
        Get a Qdrant client instance.
        
        Returns:
            QdrantClient instance
        """
        return QdrantClient(
            url=self.url,
            api_key=self.api_key,
            prefer_grpc=self.prefer_grpc 
        )
    
    

