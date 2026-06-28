import uuid
import chromadb

client = chromadb.PersistentClient(path="vectorstore")

collection = client.get_or_create_collection(name="documents")


def store_chunks(chunks: list[str], embeddings: list[list[float]], filename: str) -> int:
    document_id = str(uuid.uuid4())

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)