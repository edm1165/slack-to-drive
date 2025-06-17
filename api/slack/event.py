from fastapi import FastAPI, Request
import os
from slack_utils import get_file_info, download_file
from drive_utils import upload_to_drive

app = FastAPI()

@app.post("/api/slack/events")
async def slack_event_handler(request: Request):
    data = await request.json()

    # SlackのURL検証
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    event = data.get("event", {})
    if event.get("type") == "file_shared":
        file_id = event.get("file_id")
        file_info = get_file_info(file_id)
        content, file_name, mime = download_file(file_info)
        uploaded_id = upload_to_drive(content, file_name, mime)
        return {"status": "uploaded", "drive_file_id": uploaded_id}

    return {"status": "ignored"}
