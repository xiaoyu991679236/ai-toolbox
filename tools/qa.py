"""智能问答"""
from fastapi import APIRouter
from pydantic import BaseModel
from config import call_glm

router = APIRouter(tags=["qa"])

class QARequest(BaseModel):
    question: str

@router.post("")
def ask(req: QARequest):
    reply = call_glm(req.question)
    return {"reply": reply}
