import os
import json
from dotenv import load_dotenv
import chromadb
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

class VectorRetriever:
    def __init__(self):
        load_dotenv()
        self.chroma_host = os.getenv("CHROMA_HOST")
        self.chroma_token = os.getenv("CHROMA_API_KEY")
        self.chroma_tenant = os.getenv("CHROMA_TENANT", "default_tenant")
        self.chroma_db = os.getenv("CHROMA_DATABASE", "default_database")
        
        # Initialize BGE Embeddings
        model_name = "BAAI/bge-base-en-v1.5"
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Connect to Chroma
        self.vectorstore = self._connect_to_cloud()
        
        # Initialize Hybrid Search (BM25)
        self.hybrid_retriever = self._init_hybrid_search()

    def _connect_to_cloud(self):
        try:
            client = chromadb.HttpClient(
                host=self.chroma_host,
                tenant=self.chroma_tenant,
                database=self.chroma_db,
                headers={"Authorization": f"Bearer {self.chroma_token}"} if self.chroma_token else None
            )
            return Chroma(
                client=client,
                collection_name="mutual_fund_faq",
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Error connecting to Chroma: {e}")
            return None

    def _init_hybrid_search(self):
        """Phase 7: Optional Hybrid Search (BM25 + Vector)"""
        try:
            # Load chunks for BM25 (Keyword matching)
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            processed_path = os.path.join(base_dir, "data", "processed", "chunks.json")
            
            if not os.path.exists(processed_path):
                return None

            with open(processed_path, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
            
            docs = [Document(page_content=c['text'], metadata=c['metadata']) for c in chunk_data]
            
            # Keyword Retriever
            bm25_retriever = BM25Retriever.from_documents(docs)
            bm25_retriever.k = 2 # Top keyword matches
            
            # Vector Retriever
            vector_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # Ensemble (Hybrid)
            ensemble_retriever = EnsembleRetriever(
                retrievers=[bm25_retriever, vector_retriever],
                weights=[0.3, 0.7] # Prioritize vector but use keywords for technical terms
            )
            return ensemble_retriever
        except Exception as e:
            print(f"Hybrid Search Init Error: {e}")
            return None

    def retrieve_relevant_chunks(self, query, k=3):
        print(f"Retriever: Searching for: '{query}'")
        
        # Use Hybrid if available, fallback to Vector
        if self.hybrid_retriever:
            print("  -> Using Hybrid Search (BM25 + Vector)")
            return self.hybrid_retriever.get_relevant_documents(query)
        elif self.vectorstore:
            print("  -> Using Vector Search Only")
            return self.vectorstore.similarity_search(query, k=k)
        
        return []

if __name__ == "__main__":
    retriever = VectorRetriever()
    test_query = "What is a mutual fund?"
    results = retriever.retrieve_relevant_chunks(test_query)
    for res in results:
        print(f"\nChunk: {res.page_content[:100]}...")
