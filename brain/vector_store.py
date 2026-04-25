import chromadb
from chromadb.config import Settings
from django.conf import settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Task 5B.3.2: Initialize persistent ChromaDB client
# Using a singleton-like pattern for the client to avoid multiple connections
chroma_client = chromadb.PersistentClient(
    path=str(settings.CHROMA_DB_PATH),
    settings=Settings(allow_reset=True)
)

# Load the embedding model (cached globally in the module)
# Task 5B.1.3: Reference settings for model name
embedding_model = SentenceTransformer(
    getattr(settings, 'EMBEDDING_MODEL_NAME', 'paraphrase-multilingual-MiniLM-L12-v2')
)

def get_or_create_collection(collection_name: str = 'crivopy_resumes'):
    '''
    Task 5B.3.3: Return the ChromaDB collection.
    '''
    return chroma_client.get_or_create_collection(name=collection_name)

def index_document_chunks(document_id: int, chunks: List[str]) -> None:
    '''
    Task 5B.3.4: Generate embeddings and index chunks into ChromaDB 
    with document_id metadata.
    '''
    if not chunks:
        return

    collection = get_or_create_collection()
    
    # Generate embeddings for all chunks at once (batch processing)
    embeddings = embedding_model.encode(chunks).tolist()
    
    # Prepare IDs and Metadata
    ids = [f'doc_{document_id}_chunk_{i}' for i in range(len(chunks))]
    metadatas = [{'document_id': document_id} for _ in range(len(chunks))]
    
    # Add to ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=chunks
    )

def search_similar_chunks(query: str, document_id: int, n_results: int = 5) -> List[str]:
    '''
    Task 5B.3.5: Search semanticly similar chunks filtered by document_id.
    '''
    collection = get_or_create_collection()
    
    # Generate embedding for the search query
    query_embedding = embedding_model.encode([query]).tolist()
    
    # Query the collection with a metadata filter
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        where={'document_id': document_id}
    )
    
    # Return list of text chunks (documents)
    return results['documents'][0] if results['documents'] else []

def delete_document_chunks(document_id: int) -> None:
    '''
    Task 5B.3.6: Remove all chunks associated with a specific document.
    Crucial for data cleanup (linked to signals.py).
    '''
    collection = get_or_create_collection()
    collection.delete(where={'document_id': document_id})