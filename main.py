import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message_text):
    """Sends formatted alert directly to your Telegram app."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

@app.route('/', methods=['GET'])
def home():
    return "Photon Alert Backend is Live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receives alert data and pushes to Telegram."""
    try:
        data = request.get_json(force=True) if request.is_json else request.form
        
        pair = data.get("pair", "FX Pair")
        timeframe = data.get("tf", "15M / 1M")
        setup = data.get("setup", "4H POI Tap / 15M CHOCH")
        price = data.get("price", "Market Price")
        
        bot_message = (
            f"🚨 *PHOTON STRATEGY ALERT* 🚨\n\n"
            f"📊 *Pair:* `{pair}`\n"
            f"⏱ *Timeframe:* `{timeframe}`\n"
            f"🎯 *Setup:* {setup}\n"
            f"💰 *Price:* `{price}`\n\n"
            f"⚡ *Action:* Open MT5 to review 1M entry confirmation!"
        )
        
        send_telegram_alert(bot_message)
        return "Alert Sent!", 200

    except Exception as e:
        print(f"Error processing alert: {e}")
        return "Failed", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
