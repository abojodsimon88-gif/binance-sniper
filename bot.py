import os
import re
import time
import requests
from telethon import TelegramClient, events

# قراءة المتغيرات البيئية بأمان من Railway
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BINANCE_COOKIE = os.getenv("BINANCE_COOKIE", "")

if not BOT_TOKEN or not API_ID:
    print("خطأ: يرجى التأكد من إضافة BOT_TOKEN و API_ID في المتغيرات البيئية على Railway.")

# إنشاء عميل البوت
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def claim_red_packet(code):
    url = "https://www.binance.com/bapi/pay/v1/private/camp/gift-code/red-packet-claim"
    headers = {
        "Content-Type": "application/json",
        "Cookie": BINANCE_COOKIE,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    data = {"redPacketCode": code}
    try:
        response = requests.post(url, json=data, headers=headers)
        res_json = response.json()
        if res_json.get("code") == "000000":
            print(f"🔥 تم قنص الظرف بنجاح! الكود: {code}")
        else:
            print(f"⚠️ فشل السحب للكود {code}: {res_json.get('message')}")
    except Exception as e:
        print(f"❌ خطأ في الاتصال مع بينانس: {e}")

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text
    # البحث عن أكواد الظروف الحمراء لبينانس (عادة تبدأ بـ BP أو تتكون من حروف وأرقام معينة)
    match = re.search(r'(BP[A-Z0-9]{8,10})', text)
    if match:
        code = match.group(1)
        print(f"🎯 تم العثور على كود ظرف أحمر: {code}")
        claim_red_packet(code)

print("🚀 بدأ تشغيل بوت قنص الظروف الحمراء بنجاح وهو يراقب الآن...")
client.run_until_disconnected()
