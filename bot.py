import os
import re
import time
import requests
from telegram import Bot

# بيانات البوت ومنصة بينانس
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "حط_توكن_البوت_هنا_اذا_بدك")
BINANCE_COOKIE = os.getenv("BINANCE_COOKIE", "حط_كوكي_بينانس_هنا")

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
            print(f"تم قنص الظرف بنجاح! الكود: {code}")
        else:
            print(f"فشل السحب للكود {code}: {res_json.get('message')}")
    except Exception as e:
        print(f"خطأ في الاتصال بينانس: {e}")

# منطق المراقبة السريع
print("بدأ تشغيل بوت قنص الظروف الحمراء...")
# هنا يتم ربط مراقبة القنوات بالبوت الجديد بدون الحاجة لرقم هاتف شخصي
