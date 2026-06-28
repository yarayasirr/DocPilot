from fastapi import APIRouter
from pydantic import BaseModel

from app.services.search_service import search_documents
from app.services.llm_service import generate_answer

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):
    results = search_documents(request.question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context = "\n\n".join(documents)

    answer = generate_answer(
        question=request.question,
        context=context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": metadatas,
        "distances": distances
    }