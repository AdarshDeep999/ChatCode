# Codebase Chat

A web application that lets a user inspect a public GitHub repository and ask
questions about its code with file and line references.

## Architecture (MVP)

```text
React frontend -> FastAPI RAG backend -> GitHub API / Chroma / LLM
```

## Build progress

- [x] Project setup
- [x] Inspect a public GitHub repository's source-file tree
- [ ] Download source files as LangChain Documents
- [ ] Code-aware chunking
- [ ] Embeddings and Chroma retrieval
- [ ] Answer questions with sources
- [ ] React interface and Docker

## Run the current backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` and try `POST /api/repositories/inspect`
with a public GitHub repository URL.

