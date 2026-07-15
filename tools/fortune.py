"""AI运势"""
from fastapi import APIRouter
from pydantic import BaseModel
from config import call_glm

router = APIRouter(tags=["fortune"])

class FortuneRequest(BaseModel):
    sign: str     # 星座名称
    year: str = ""

@router.post("")
def tell_fortune(req: FortuneRequest):
    prompt = f"""你是星座运势专家。请为{req.sign}（{req.year or '未知'}年出生）生成今日运势。
包含：整体运势、爱情、事业、财运、幸运色、幸运数字。
格式活泼有趣，300字以内。"""

    reply = call_glm(
        prompt,
        temperature=1.0,
        max_tokens=800
    )
    return {"reply": reply}
