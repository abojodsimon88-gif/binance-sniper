import os
import re
import requests
from telethon import TelegramClient, events

# بيانات تيليجرام التي حصلت عليها
API_ID = 36367094
API_HASH = "81845243e38b36547b66ad36719264a4"

# مفاتيح بينانس الخاصة بك
BINANCE_API_KEY = "oCUAtyBzy7iWAh7g6CjeCioeynMqTxNgh9fObdGcmUsWi4seuUpQMp3hORHv738M"
BINANCE_SECRET_KEY = "INuKxG1LqKNWEVePaB2oTRahKbe1BSxP808LG2GTxpahuNW37tE757otiduea"

# إنشاء جلسة تيليجرام
client = TelegramClient('crypto_sniper_session', API_ID, API_HASH)

# تعبير نمطي (Regex) للبحث عن كواد الظروف الحمراء
CODE_REGEX = r"(?:https?:\/\/)?(?:binance\.com[^\s]*|pay[^\s]*|bpay[^\s]*)\/([a-zA-Z0-9]{8,16})"

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    message_text = event.raw_text
    
    # البحث عن الكود في رسائل القنوات
    match = re.search(CODE_REGEX, message_text)
    if match:
        red_packet_code = match.group(1)
        print(f"[!] تم رصد كود ظرف أحمر محتمل: {red_packet_code}")
        
        # إرسال الكود تلقائياً إلى بينانس
        claim_red_packet(red_packet_code)

def claim_red_packet(code):
    url = "https://api.binance.com/binance/pay/wapi/sub/redpack/claim"
    
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY,
    }
    
    payload = {
        "code": code
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"[شغل عالي!] تم استلام الظرف بنجاح: {code}")
        else:
            print(f"[-] فشل الاستلام أو الكود مستخدم مسبقاً: {response.text}")
    except Exception as e:
        print(f"[خطأ في الاتصال]: {e}")

def main():
    print("[*] جاري تشغيل بوت صيد الظروف الحمراء على تيليجرام...")
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
