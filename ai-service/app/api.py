
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from .ingestion_service import (
    index_repository,
    reindex_repository
)
from .chat_service import chat_with_repository

app = FastAPI(
    title="ChatCode AI Service",
    description="AI service for indexing and querying GitHub repositories",
    version="1.0.0"
)


class IndexRequest(BaseModel):
    repositoryId: str
    repositoryUrl: HttpUrl

class ChatRequest(BaseModel):
    repositoryId: str
    question: str

@app.get("/")
def home():
    return {
        "message": "Codebase Chat AI Service is running"
    }


@app.post("/api/index")
def index(request: IndexRequest):

    try:
        result = index_repository(
            str(request.repositoryId),
            str(request.repositoryUrl)
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/api/reindex")
def reindex(request: IndexRequest):

    try:
        result = reindex_repository(
            str(request.repositoryId),
            str(request.repositoryUrl)
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/api/chat")
def chat(request: ChatRequest):

    try:
        return chat_with_repository(
            repository_id=request.repositoryId,
            question=request.question
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )