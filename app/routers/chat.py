from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from app.services.gemini_service import generate_response
router = APIRouter()


class ChatRequest(BaseModel):
    message: str= Field(
        min_length=1,
        max_length=2000,
        description ="Message of the user"
    )


class ChatResponse(BaseModel):
    response: str
    status: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    ai_response = generate_response(request.message)

    return ChatResponse(
        response=ai_response,
        status="Success"
    )

@router.get("/hello/{name}")
def great(name:str):
    return{"message":f"hello{name}"}      

@router.get("/square")
def square(number: int):
    return{"message":number*number}