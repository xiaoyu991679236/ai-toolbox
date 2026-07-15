"""共享配置 + API 调用"""
import requests, json

KEY = "3763dcfcf32740acad89044ea7b8e0b7.YmrD87nj8Gab7ioa"

def call_glm(prompt: str, system: str = "", temperature: float = 0.7, max_tokens: int = 2000) -> str:
    """统一的 GLM API 调用"""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    r = requests.post(
        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        headers={"Authorization": f"Bearer {KEY}"},
        json={
            "model": "glm-4-flash",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
    )
    return r.json()["choices"][0]["message"]["content"]
