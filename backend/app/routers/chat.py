from fastapi import APIRouter
from pydantic import BaseModel

from app.services.search_service import search_documents

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):

    results = search_documents(request.question)

    return {
        "question": request.question,
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0],
        "distances": results["distances"][0]
    }