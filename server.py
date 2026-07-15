"""AI工具箱 - FastAPI 后端"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI工具箱")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"name": "AI工具箱", "tools": ["qa", "translate", "naming", "fortune", "doc-qa"]}

# ═══════════════════════════════════════════
# 工具路由 — 每个工具一个文件，用 include 导入
# ═══════════════════════════════════════════

from tools.qa import router as qa_router
from tools.translate import router as translate_router
from tools.naming import router as naming_router
from tools.fortune import router as fortune_router
from tools.doc_qa import router as doc_qa_router

app.include_router(qa_router, prefix="/qa")
app.include_router(translate_router, prefix="/translate")
app.include_router(naming_router, prefix="/naming")
app.include_router(fortune_router, prefix="/fortune")
app.include_router(doc_qa_router, prefix="/doc-qa")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
