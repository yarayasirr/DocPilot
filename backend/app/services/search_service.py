from sentence_transformers import SentenceTransformer
from app.services.vector_store import collection

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_documents(question: str, n_results: int = 3):
    # Convert the question into an embedding
    question_embedding = model.encode(question).tolist()

    # Search the vector database
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results