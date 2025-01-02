from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingsManager:
    def __init__(self):
        self.embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(
            path=os.getenv("CHROMA_DB_PATH", "./chromadb_store"),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_document(self, text: str, metadata: dict = None):
        """Add a document to the collection"""
        embeddings = self.embedder.encode([text])
        self.collection.add(
            documents=[text],
            embeddings=[embeddings.tolist()],
            metadatas=[metadata] if metadata else None,
            ids=[str(hash(text))]
        )

    def search_documents(self, query: str, n_results: int = 3):
        """Search for relevant documents"""
        query_embedding = self.embedder.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        return results["documents"][0]

    def clear_collection(self):
        """Clear all documents from the collection"""
        self.collection.delete(where={}) 