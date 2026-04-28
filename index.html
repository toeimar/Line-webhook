from flask import Flask, request, jsonify
import requests
import hashlib
import hmac
import base64
import os

app = Flask(**name**)

# ดึงค่าจาก Environment Variables

LINE_CHANNEL_SECRET       = os.environ.get(“LINE_CHANNEL_SECRET”, “”)
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get(“LINE_CHANNEL_ACCESS_TOKEN”, “”)
TELEGRAM_BOT_TOKEN        = os.environ.get(“TELEGRAM_BOT_TOKEN”, “”)
TELEGRAM_CHAT_ID          = os.environ.get(“TELEGRAM_CHAT_ID”, “”)

def verify_line_signature(body: bytes, signature: str) -> bool:
hash_ = hmac.new(
LINE_CHANNEL_SECRET.encode(“utf-8”),
body,
hashlib.sha256,
).digest()
expected = base64.b64encode(hash_).decode(“utf-8”)
return hmac.compare_digest(expected, signature)

def get_line_profile(user_id: str) -> dict:
url = f”https://api.line.me/v2/bot/profile/{user_id}”
headers = {“Authorization”: f”Bearer {LINE_CHANNEL_ACCESS_TOKEN}”}
resp = requests.get(url, headers=headers, timeout=10)
if resp.status_code == 200:
return resp.json()
return {}

def send_telegram_photo(photo_url: str, caption: str):
url = f”https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto”
payload = {
“chat_id”: TELEGRAM_CHAT_ID,
“photo”: photo_url,
“caption”: caption,
“parse_mode”: “HTML”,
}
resp = requests.post(url, json=payload, timeout=10)
resp.raise_for_status()

def send_telegram_text(message: str):
url = f”https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage”
payload = {
“chat_id”: TELEGRAM_CHAT_ID,
“text”: message,
“parse_mode”: “HTML”,
}
resp = requests.post(url, json=payload, timeout=10)
resp.raise_for_status()

@app.route(”/webhook”, methods=[“POST”])
def webhook():
signature = request.headers.get(“X-Line-Signature”, “”)
body_bytes = request.get_data()

```
if not verify_line_signature(body_bytes, signature):
    return jsonify({"error": "Invalid signature"}), 403

data = request.get_json(silent=True) or {}
for event in data.get("events", []):
    event_type = event.get("type")
    source     = event.get("source", {})
    user_id    = source.get("userId", "ไม่ทราบ")

    if event_type == "follow":
        profile      = get_line_profile(user_id)
        display_name = profile.get("displayName", "ไม่ทราบชื่อ")
        picture_url  = profile.get("pictureUrl", "")
        status_msg   = profile.get("statusMessage", "")

        caption = (
            "🔔 <b>มีคนแอด LINE ใหม่!</b>\n"
            f"👤 ชื่อ: <b>{display_name}</b>\n"
            f"🆔 User ID: <code>{user_id}</code>\n"
        )
        if status_msg:
            caption += f"💬 สถานะ: {status_msg}"

        if picture_url:
            send_telegram_photo(picture_url, caption)
        else:
            send_telegram_text(caption + "\n🖼 ไม่มีรูปโปรไฟล์")

    elif event_type == "unfollow":
        msg = (
            "❌ <b>มีคนบล็อก LINE OA</b>\n"
            f"🆔 User ID: <code>{user_id}</code>"
        )
        send_telegram_text(msg)

return jsonify({"status": "ok"}), 200
```

@app.route(”/”, methods=[“GET”])
def health():
return “LINE Webhook Server is running ✅”, 200

if **name** == “**main**”:
port = int(os.environ.get(“PORT”, 5000))
app.run(host=“0.0.0.0”, port=port)
