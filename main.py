from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def format_signal(data):
    entry = data["candle"]["close"]
    sl = round(entry - 9, 2)
    tp1 = round(entry + 18, 2)
    tp2 = round(entry + 36, 2)

    reasons = f"""
✅ {data['pattern']} at {data['zone']}
✅ Sweep: {data['liquidity']}
✅ Structure: {data['structure']}
✅ Trend: {data['mtf']['H4']} / {data['mtf']['H1']}
    """.strip()

    message = f"""🚨 BUY SIGNAL - {data['pair']} 🚨
TF: {data['tf']} (Confirm {data['mtf']['H4']})
ENTRY: {entry}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

REASON:
{reasons}
"""
    return message

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    if data:
        message = format_signal(data)
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message}
        )
        return {"status": "sent"}, 200
    return {"error": "no data"}, 400

@app.route('/', methods=['GET'])
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
