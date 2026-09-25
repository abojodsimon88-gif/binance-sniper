import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# جلب التوكن والكوكي من المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN", "حط_التوكن_هنا")
BINANCE_COOKIE = os.getenv("BINANCE_COOKIE", "حط_الكوكي_هنا")

def claim_red_packet(code):
    url = "https://www.binance.com/bapi/pay/v1/private/camp/gift-code/red-packet-claim"
    headers = {
        "Content-Type": "application/json",
        "Cookie": BINANCE_COOKIE,
        "User-Agent": "Mozilla/5.0"
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text or update.message.caption or ""
    match = re.search(r'(BP[A-Z0-9]{8,10})', message_text)
    if match:
        code = match.group(1)
        print(f"🎯 تم العثور على كود: {code}")
        claim_red_packet(code)

if __name__ == '__main__':
    print("🚀 جاري بدء تشغيل البوت...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
