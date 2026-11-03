from .embedder import model
from .vector_store import get_collection


def search_code(repository_id: str, query: str, k: int = 5):
    collection = get_collection()

    # Convert the user's question into an embedding
    query_embedding = model.encode([query])

    # Search only within the requested repository
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=k,
        where={"repository_id": repository_id}
    )
    for i, metadata in enumerate(results["metadatas"][0]):
        print(
            i + 1,
            metadata["source"],
            metadata["start_line"],
            metadata["end_line"]
        )

    return results