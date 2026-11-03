
import chromadb
import hashlib
from collections import defaultdict

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "codebase"


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def delete_repository_chunks(repository_id: str):
    collection = get_collection()

    collection.delete(
        where={"repository_id": repository_id}
    )


def generate_chunk_id(repository_id: str, source: str, chunk_index: int):
    unique_string = f"{repository_id}:{source}:{chunk_index}"

    return hashlib.sha256(
        unique_string.encode()
    ).hexdigest()


def store_chunks(repository_id: str, chunks, embeddings):
    collection = get_collection()

    file_chunk_counts = defaultdict(int)
    ids = []

    for chunk in chunks:
        source = chunk.metadata["source"]

        chunk_index = file_chunk_counts[source]
        file_chunk_counts[source] += 1

        chunk_id = generate_chunk_id(
            repository_id,
            source,
            chunk_index
        )

        ids.append(chunk_id)

        chunk.metadata["repository_id"] = repository_id

    documents = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    return collection
