"""文档问答 RAG"""
from fastapi import APIRouter
from pydantic import BaseModel
from config import call_glm
import requests, json, math, os, re

router = APIRouter(tags=["doc-qa"])
KEY = "3763dcfcf32740acad89044ea7b8e0b7.YmrD87nj8Gab7ioa"
STORE_FILE = "doc_store.json"

# ═══════════════════════════════════════════
# Embedding
# ═══════════════════════════════════════════

def get_embedding(text):
    r = requests.post(
        "https://open.bigmodel.cn/api/paas/v4/embeddings",
        headers={"Authorization": f"Bearer {KEY}"},
        json={"model": "embedding-3", "input": text}
    )
    return r.json()["data"][0]["embedding"]

def cosine(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    m1 = math.sqrt(sum(a * a for a in v1))
    m2 = math.sqrt(sum(b * b for b in v2))
    return dot / (m1 * m2) if m1 * m2 > 0 else 0

# ═══════════════════════════════════════════
# 文档存储
# ═══════════════════════════════════════════

def chunk_text(text, chunk_size=300):
    """按句号分块，每块约 300 字"""
    sentences = re.split(r'[。！？\n]+', text)
    chunks = []
    current = ""
    for s in sentences:
        s = s.strip()
        if not s: continue
        if len(current) + len(s) > chunk_size and current:
            chunks.append(current)
            current = s
        else:
            current += s + "。"
    if current: chunks.append(current)
    return chunks

def save_document(doc_id: str, text: str):
    store = load_store()
    chunks = chunk_text(text)
    store[doc_id] = {
        "text": text,
        "chunks": [{"text": c, "vector": get_embedding(c)} for c in chunks]
    }
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False)

def load_store():
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ═══════════════════════════════════════════
# 搜索
# ═══════════════════════════════════════════

def search_document(doc_id: str, query: str, top_k=3):
    store = load_store()
    doc = store.get(doc_id)
    if not doc:
        return "Document not found. Upload a document first."

    query_vec = get_embedding(query)
    scored = []
    for c in doc["chunks"]:
        score = cosine(query_vec, c["vector"])
        scored.append((score, c["text"]))
    scored.sort(key=lambda x: x[0], reverse=True)

    context = "\n---\n".join(c for _, c in scored[:top_k])
    return context

# ═══════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════

class UploadRequest(BaseModel):
    doc_id: str
    text: str

class AskRequest(BaseModel):
    doc_id: str
    question: str

@router.post("/upload")
def upload(req: UploadRequest):
    save_document(req.doc_id, req.text)
    return {"status": "ok", "doc_id": req.doc_id, "length": len(req.text)}

@router.post("/ask")
def ask(req: AskRequest):
    context = search_document(req.doc_id, req.question)
    if context.startswith("Document not found"):
        return {"reply": context}

    prompt = f"""根据以下文档内容回答用户问题。如果文档中没有相关信息，请说"文档中未提及"。

【文档内容】
{context}

【用户问题】
{req.question}

请用中文回答，不超过 300 字。"""

    reply = call_glm(prompt, system="你是文档问答助手。", temperature=0.3)
    return {"reply": reply, "context_length": len(context)}
