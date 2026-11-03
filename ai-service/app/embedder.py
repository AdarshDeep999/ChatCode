from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(chunks):
    texts = [chunk.page_content for chunk in chunks]

    embeddings = model.encode(texts)

    return embeddings