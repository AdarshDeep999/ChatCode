
from .github_loader import get_repository_files
from .document_loader import create_documents
from .chunker import split_documents
from .embedder import create_embeddings
from .vector_store import (
    delete_repository_chunks,
    store_chunks
)


def prepare_repository(repository_id: str, repository_url: str):
    # 1. Fetch repository files
    files = get_repository_files(repository_url)

    if not files:
        raise ValueError("No supported files found in repository")

    # 2. Convert files into Documents
    documents = create_documents(files, repository_id)

    # 3. Split documents into chunks
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No chunks generated from repository")

    # 4. Generate embeddings
    embeddings = create_embeddings(chunks)

    return files, chunks, embeddings


def index_repository(repository_id: str, repository_url: str):

    # Prepare repository
    files, chunks, embeddings = prepare_repository(
        repository_id,
        repository_url
    )

    # Store new chunks. No deletion here.
    store_chunks(repository_id, chunks, embeddings)

    return {
        "repositoryId": repository_id,
        "filesProcessed": len(files),
        "chunksStored": len(chunks),
        "status": "INDEXED"
    }


def reindex_repository(repository_id: str, repository_url: str):

    # Prepare the updated repository first
    files, chunks, embeddings = prepare_repository(
        repository_id,
        repository_url
    )

    # Delete only this repository's old chunks
    delete_repository_chunks(repository_id)

    # Store the updated chunks
    store_chunks(repository_id, chunks, embeddings)

    return {
        "repositoryId": repository_id,
        "filesProcessed": len(files),
        "chunksStored": len(chunks),
        "status": "REINDEXED"
    }
