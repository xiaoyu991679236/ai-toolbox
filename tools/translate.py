"""AI翻译"""
from fastapi import APIRouter
from pydantic import BaseModel
from config import call_glm

router = APIRouter(tags=["translate"])

class TransRequest(BaseModel):
    text: str
    target: str = "Chinese"

@router.post("")
def translate(req: TransRequest):
    try:
        reply = call_glm(
            f"Translate to {req.target}, only output the translation:\n\n{req.text}",
            system="You are a translator. Only output the translated text.",
            temperature=0.3,
            max_tokens=500
        )
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
