import os
from flask import Flask, request, jsonify
import io
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Git管理外なのでローカル or Render環境に設置

def upload_to_gdrive(file_url, file_name):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)

    slack_token = os.getenv("SLACK_BOT_TOKEN")
    headers = {"Authorization": f"Bearer {slack_token}"}
    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        file_stream = io.BytesIO(response.content)
        media = MediaIoBaseUpload(file_stream, mimetype='application/octet-stream', resumable=True)
        file_metadata = {'name': file_name, 'parents': [os.getenv("GOOGLE_FOLDER_ID")]}
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded file with ID: {file.get('id')}")
    else:
        print(f"Failed to download file from Slack: {response.status_code}")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # URL検証用チャレンジリクエスト対応
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # 通常イベント処理
    print("Received Slack event:", data)

    # ここにファイルアップロードイベントなどの処理を入れる

    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
