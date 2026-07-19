from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generate_response
router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    ai_response=generate_response(request.message)

    return ChatResponse(
        response=ai_response,
        status=f"Success"
    )

@router.get("/hello/{name}")
def great(name:str):
    return{"message":f"hello{name}"}      

@router.get("/square")
def square(number: int):
    return{"message":number*number}