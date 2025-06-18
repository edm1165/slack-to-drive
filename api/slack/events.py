from flask import Flask

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()

    # URL検証リクエストへの対応
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # 通常のイベント処理
    print("Received Slack event:", data)
    return "", 200
