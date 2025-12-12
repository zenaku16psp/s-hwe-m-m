import asyncio
from maythusharmusic import app
from maythusharmusic.utils.database import get_expired_messages, remove_clean_message

async def clean_mode_task():
    """နောက်ကွယ်မှ အလုပ်လုပ်မည့် Clean Mode စနစ်"""
    while True:
        try:
            # ၁၀ စက္ကန့်တစ်ခါ စစ်ဆေးမည်
            await asyncio.sleep(10)
            
            # အချိန်ပြည့်သွားသော စာများကို ရှာမည်
            expired_msgs = await get_expired_messages()
            
            # သန့်ရှင်းရေးလုပ်လိုက်သော Group များကို မှတ်သားရန် (ထပ်ခါတလဲလဲ စာမပို့မိစေရန်)
            cleaned_chats = set()
            
            for msg in expired_msgs:
                chat_id = msg["chat_id"]
                message_id = msg["message_id"]
                
                try:
                    # Telegram Group ထဲမှ စာကို ဖျက်မည်
                    await app.delete_messages(chat_id, message_id)
                    # အောင်မြင်ရင် Chat ID ကို မှတ်ထားမယ်
                    cleaned_chats.add(chat_id)
                except Exception:
                    # ဖျက်မရရင် (ဥပမာ Bot Admin မဟုတ်တော့ရင်) ကျော်သွားမယ်
                    pass
                
                # Database ထဲကနေ စာရင်းဖျက်မည်
                await remove_clean_message(chat_id, message_id)
            
            # --- သန့်ရှင်းရေးလုပ်ပြီးကြောင်း စာပြန်ပို့ခြင်း ---
            for chat_id in cleaned_chats:
                try:
                    # Notification ပို့မည်
                    sent = await app.send_message(
                        chat_id,
                        "> 🦋𝐆𝐫𝐨𝐮𝐩 𝐂𝐥𝐞𝐚𝐧 𝐌𝐨𝐝𝐞, အချိန်ပြည့်သွားသော စာများကို အလိုအလျောက် ရှင်းလင်းပြီးပါပြီ။🦋"
                    )
                    
                    # Notification ကိုပါ ၁၀ စက္ကန့်နေရင် ပြန်ဖျက်မည် (Group မရှုပ်အောင်)
                    await asyncio.sleep(10)
                    await sent.delete()
                except:
                    pass
            # ---------------------------------------------
                
        except Exception as e:
            print(f"Clean Mode Error: {e}")
