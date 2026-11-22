
import os
import time
import requests

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://botapi.rubika.ir/v3/{TOKEN}"

CHANNEL = "@ghanonkar"

HELP = """🤖 مدیر هوشمند قانون کار

دستورات ربات:

/start - شروع
/help - راهنما
/rules - قوانین گروه
/channel - معرفی کانال
/id - نمایش شناسه گروه

📢 کانال رسمی:
@ghanonkar
"""

RULES = """📌 قوانین گروه قانون کار و تأمین اجتماعی

۱. احترام به تمام اعضا الزامی است.
۲. از ارسال تبلیغات نامرتبط خودداری کنید.
۳. اخبار و مطالب را با منبع معتبر منتشر کنید.
۴. از توهین و بحث‌های خارج از موضوع خودداری کنید.
۵. اطلاعات شخصی دیگران را منتشر نکنید.

با تشکر از همراهی شما 🌹
"""

def api(method, data=None):
    response = requests.post(
        f"{API}/{method}",
        json=data or {},
        timeout=30
    )
    response.raise_for_status()
    result = response.json()

    if result.get("status") not in (None, "OK"):
        raise RuntimeError(str(result))

    return result.get("data", result)

def send(chat_id, text):
    return api("sendMessage", {
        "chat_id": chat_id,
        "text": text
    })

def handle(update):
    if update.get("type") != "NewMessage":
        print("Other event:", update.get("type"))
        return

    message = update.get("new_message", {})
    chat_id = update.get("chat_id")
    sender_type = message.get("sender_type")

    if not chat_id or sender_type == "Bot":
        return

    text = (message.get("text") or "").strip()
    command = text.split()[0].lower() if text else ""

    if command in ("/start", "/help"):
        send(chat_id, HELP)

    elif command == "/rules":
        send(chat_id, RULES)

    elif command == "/channel":
        send(chat_id, "📢 کانال رسمی اخبار قانون کار:\n" + CHANNEL)

    elif command == "/id":
        send(chat_id, f"شناسه این گفتگو:\n{chat_id}")

def main():
    print("Rubika bot starting...")

    info = api("getMe")
    print("Bot connected successfully")

    offset = None

    while True:
        try:
            payload = {"limit": 20}

            if offset:
                payload["offset_id"] = offset

            result = api("getUpdates", payload)

            for update in result.get("updates", []):
                try:
                    handle(update)
                except Exception as error:
                    print("Update error:", error)

            offset = result.get("next_offset_id") or offset

            if not result.get("updates"):
                time.sleep(2)

        except Exception as error:
            print("Connection error:", error)
            time.sleep(5)

if __name__ == "__main__":
    main()
