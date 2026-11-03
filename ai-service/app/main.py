from app.vector_store import get_collection

collection = get_collection()

all_records = collection.get(include=["metadatas"])

legacy_ids = [
    record_id
    for record_id, metadata in zip(
        all_records["ids"],
        all_records["metadatas"]
    )
    if "repository_id" not in metadata
]

print("Legacy chunks to delete:", len(legacy_ids))

if legacy_ids:
    collection.delete(ids=legacy_ids)

print("Remaining chunks:", collection.count())