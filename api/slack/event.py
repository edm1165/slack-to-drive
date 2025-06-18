# api/slack/events.py
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/api/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    # Slack URL確認用の応答
    if data.get("type") == "url_verification":
        return {"challenge": data.get("challenge")}
    
    # その他のイベント処理（例：file_sharedなど）
    # ここに処理を書いていく
    return {"ok": True}
