
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=payload)


token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
message = "Ola Mundo!!!"

send_telegram_message(token, chat_id, message)