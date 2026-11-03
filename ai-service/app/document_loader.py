from pathlib import PurePosixPath

from langchain_core.documents import Document


LANGUAGE_MAP = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".xml": "xml",
    ".md": "markdown",
}


def get_language(path: str) -> str:
    extension = PurePosixPath(path).suffix.lower()

    return LANGUAGE_MAP.get(extension, "unknown")



def create_documents(files: list[dict], repository_id: str) -> list[Document]:
    documents = []

    for file in files:
        path = file["path"]
        content = file["content"]

        document = Document(
            page_content=content,
            metadata={
                "repository_id": repository_id,
                "source": path,
                "language": get_language(path),
            },
        )

        documents.append(document)

    return documents
