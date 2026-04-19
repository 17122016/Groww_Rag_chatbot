import os
import json
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

def get_paths():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    processed_chunks_path = os.path.join(base_dir, "data", "processed", "chunks.json")
    return processed_chunks_path

def build_vector_store():
    # Load .env file
    load_dotenv()
    processed_path = get_paths()
    
    if not os.path.exists(processed_path):
        print(f"Error: {processed_path} not found. Run preprocessor first.")
        return

    # Chroma Cloud Configuration (Fixed to match User's .env)
    chroma_host = os.getenv("CHROMA_HOST")
    chroma_token = os.getenv("CHROMA_API_KEY")
    chroma_tenant = os.getenv("CHROMA_TENANT", "default_tenant")
    chroma_db = os.getenv("CHROMA_DATABASE", "default_database")
    
    if not chroma_host:
        print("Error: CHROMA_HOST not set in .env")
        return

    with open(processed_path, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)

    print(f"Preparing {len(chunk_data)} chunks for Chroma Cloud upload...")
    print(f"Target Host: {chroma_host} | Tenant: {chroma_tenant} | DB: {chroma_db}")
    
    # Initialize BGE Embeddings
    print("Generating BGE embeddings locally before upload...")
    model_name = "BAAI/bge-base-en-v1.5"
    embeddings_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Connect to Chroma Cloud
    try:
        client = chromadb.HttpClient(
            host=chroma_host,
            tenant=chroma_tenant,
            database=chroma_db,
            headers={"Authorization": f"Bearer {chroma_token}"} if chroma_token else None
        )
        
        collection = client.get_or_create_collection(
            name="mutual_fund_faq",
            metadata={"hnsw:space": "cosine"}
        )
    except Exception as e:
        print(f"Error connecting to Chroma Cloud: {e}")
        return

    # Prepare batches for upsert
    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for item in chunk_data:
        ids.append(item["metadata"]["chunk_id"])
        documents.append(item["text"])
        metadatas.append(item["metadata"])
        # Generate embedding locally to save cloud computation
        embeddings.append(embeddings_model.embed_query(item["text"]))

    # Upsert to Cloud in batches to avoid network timeouts
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        print(f"Upserting batch {i//batch_size + 1}...")
        collection.upsert(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size]
        )

    print(f"Success! Data successfully uploaded/updated on Chroma Cloud.")

if __name__ == "__main__":
    build_vector_store()
