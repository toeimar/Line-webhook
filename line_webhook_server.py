from flask import Flask, request, jsonify
import requests
import hashlib
import hmac
import base64
import os

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
def verify_line_signature(body, signature):
    hash_ = hmac.new(
        LINE_CHANNEL_SECRET.encode("utf-8"),
        body,
        hashlib.sha256,
    ).digest()
    expected = base64.b64encode(hash_).decode("utf-8")
    return hmac.compare_digest(expected, signature)

def get_line_profile(user_id):
    url = "https://api.line.me/v2/bot/profile/" + user_id
    headers = {"Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN}
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return {}

def send_telegram_photo(photo_url, caption):
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendPhoto"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "photo": photo_url, "caption": caption, "parse_mode": "HTML"}
    requests.post(url, json=payload, timeout=10)

def send_telegram_text(message):
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload, timeout=10)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body_bytes = request.get_data()
    if not verify_line_signature(body_bytes, signature):
        return jsonify({"error": "Invalid signature"}), 403
    data = request.get_json(silent=True) or {}
    for event in data.get("events", []):
        event_type = event.get("type")
        user_id = event.get("source", {}).get("userId", "unknown")
        if event_type == "follow":
            profile = get_line_profile(user_id)
            name = profile.get("displayName", "unknown")
            pic = profile.get("pictureUrl", "")
            status = profile.get("statusMessage", "")
            caption = "New follower: " + name + "\nID: " + user_id
            if status:
                caption += "\nStatus: " + status
            if pic:
                send_telegram_photo(pic, caption)
            else:
                send_telegram_text(caption)
        elif event_type == "unfollow":
            send_telegram_text("Unfollowed: " + user_id)
    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
