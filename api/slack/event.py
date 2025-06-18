from flask import Flask

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    # Slackのイベント処理ロジック
    return "OK"