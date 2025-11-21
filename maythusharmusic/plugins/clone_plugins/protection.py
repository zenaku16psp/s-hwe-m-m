import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, Message
from pyrogram.enums import ChatMemberStatus
from maythusharmusic import app
from maythusharmusic.utils.database import get_assistant

@Client.on_chat_member_updated(filters.group)
async def auto_unban_main_bot(client: Client, member: ChatMemberUpdated):
    try:
        # Main Bot အချက်အလက် ရယူခြင်း
        if not app.me:
            await app.get_me()
        main_bot_id = app.me.id
        main_bot_username = app.me.username

        # အပြောင်းအလဲဖြစ်သွားသူသည် Main Bot ဟုတ်မဟုတ် စစ်ခြင်း
        if member.new_chat_member.user.id == main_bot_id:
            
            # Main Bot သည် BANNED (ပိတ်ပင်ခံရခြင်း) ဖြစ်သွားလျှင်
            if member.new_chat_member.status == ChatMemberStatus.BANNED:
                chat_id = member.chat.id
                
                # ၁။ Clone Bot က Unban လုပ်ရန် ကြိုးစားမည်
                try:
                    await client.unban_chat_member(chat_id, main_bot_id)
                    await client.send_message(
                        chat_id, 
                        f"𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗔𝗹𝗲𝗿𝘁\n"
                        f"𝗜 𝗳𝗼𝘂𝗻𝗱 𝗠𝗮𝗶𝗻 𝗕𝗼𝘁 (@{main_bot_username}) 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗯𝗮𝗻𝗻𝗲𝗱.\n"
                        f"✅𝗨𝗻𝗯𝗮𝗻𝗻𝗲𝗱."
                    )
                except Exception:
                    # Clone Bot က Admin မဟုတ်ရင် Unban မရနိုင်ပါ (ကျော်သွားမည်)
                    pass

                # ၂။ Assistant က Unban လုပ်ပြီး ပြန်ထည့်ရန် ကြိုးစားမည်
                try:
                    userbot = await get_assistant(chat_id)
                    
                    # Assistant ကလည်း Unban လုပ်ကြည့်မယ် (Sure ဖြစ်အောင်)
                    try:
                        await userbot.unban_chat_member(chat_id, main_bot_id)
                    except:
                        pass
                    
                    # အရေးအကြီးဆုံး - Assistant က Main Bot ကို Group ထဲ ပြန်ဆွဲထည့်မယ်
                    await asyncio.sleep(1)
                    await userbot.add_chat_members(chat_id, main_bot_username)
                    await client.send_message(chat_id, f"✅𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙝𝙖𝙨 𝙧𝙚-𝙖𝙙𝙙𝙚𝙙 𝙩𝙝𝙚 𝙈𝙖𝙞𝙣 𝘽𝙤𝙩 𝙩𝙤 𝙩𝙝𝙚 𝙂𝙧𝙤𝙪𝙥.")
                    
                except Exception as e:
                    # Assistant Admin မဟုတ်ရင် ထည့်လို့မရနိုင်ပါ
                    print(f"Failed to add main bot back: {e}")

    except Exception as e:
        print(f"Protection Module Error: {e}")
