"""AI取名"""
from fastapi import APIRouter
from pydantic import BaseModel
from config import call_glm

router = APIRouter(tags=["naming"])

class NamingRequest(BaseModel):
    keyword: str
    ntype: str = "宝宝起名"     # 宝宝起名 / 公司命名 / 网名
    extra: str = ""

@router.post("")
def generate(req: NamingRequest):
    prompt = f"请为「{req.keyword}」生成5个{req.ntype}"
    if req.extra:
        prompt += f"，要求：{req.extra}"
    prompt += "，每个名字附简要寓意说明。"

    reply = call_glm(
        prompt,
        system="你是专业取名专家，只输出名字和寓意，格式美观。",
        temperature=1.0,
        max_tokens=1200
    )
    return {"reply": reply}
