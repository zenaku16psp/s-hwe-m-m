from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
from maythusharmusic import app
from maythusharmusic.utils.database import get_assistant

# (၁) Clone Bot ကို Group ထဲထည့်ရင် Main Bot ကို Assistant က လိုက်ထည့်ပေးမည့် Function
@Client.on_message(filters.new_chat_members)
async def auto_join_main_bot(client: Client, message: Message):
    try:
        # Main Bot အချက်အလက်ယူခြင်း
        main_bot = await app.get_me()
        
        # ဝင်လာသူများထဲတွင် Clone Bot ပါမပါ စစ်ခြင်း
        new_members = [u.id for u in message.new_chat_members]
        
        if client.me.id in new_members:
            # Clone Bot ဝင်လာပြီ၊ Main Bot ရှိမရှိ စစ်မယ်
            try:
                await client.get_chat_member(message.chat.id, main_bot.id)
            except:
                # Main Bot မရှိသေးရင် Assistant နဲ့ ဆွဲထည့်မယ်
                try:
                    userbot = await get_assistant(message.chat.id)
                    await userbot.add_chat_members(message.chat.id, main_bot.username)
                    await message.reply_text(f"✅ <b>ᴛʜᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ ʜᴀꜱ ᴀᴅᴅᴇᴅ ᴛʜᴇ ᴍᴀɪɴ ʙᴏᴛ (@{main_bot.username})</b> .")
                except Exception as e:
                    await message.reply_text(f" ᴜɴᴀʙʟᴇ ᴛᴏ ᴄᴀɴɴᴏᴛ ᴀᴅᴅ ᴍᴀɪɴ ʙᴏᴛ (ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴀᴅᴍɪɴ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ).\nᴘʟᴇᴀꜱᴇ ᴀᴅᴅ @{main_bot.username} manually.")
    except Exception as e:
        print(f"Auto Join Error: {e}")


# (၂) Clone Bot ကို Admin ပေးလိုက်ရင် Main Bot ကိုပါ Auto Admin ပေးမည့် Function
@Client.on_chat_member_updated(filters.group)
async def auto_promote_main_bot(client: Client, member: ChatMemberUpdated):
    try:
        # ပြောင်းလဲသွားသူသည် Clone Bot ကိုယ်တိုင် ဟုတ်မဟုတ် စစ်ခြင်း
        if member.new_chat_member.user.id == client.me.id:
            # Clone Bot သည် Admin ဖြစ်သွားပြီလား စစ်ခြင်း
            if member.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
                
                # Main Bot အချက်အလက်ယူခြင်း
                main_bot = await app.get_me()
                
                # Main Bot ကို Promote လုပ်ခြင်း
                try:
                    await client.promote_chat_member(
                        member.chat.id,
                        main_bot.id,
                        privileges=ChatPrivileges(
                            can_manage_chat=True,
                            can_delete_messages=True,
                            can_manage_video_chats=True,
                            can_invite_users=True,
                            can_pin_messages=True,
                            can_promote_members=True, # Admin ထပ်ပေးနိုင်အောင်
                            can_restrict_members=True,
                            can_change_info=False
                        )
                    )
                    await client.send_message(member.chat.id, f"✅ <b>ᴛʜᴇ ᴍᴀɪɴ ʙᴏᴛ (@{main_bot.username})</b> ʜᴀꜱ ʙᴇᴇɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴘᴘᴏɪɴᴛᴇᴅ ᴀꜱ <b>ᴀᴅᴍɪɴ</b> .")
                except Exception as e:
                    # Clone Bot မှာ Add Admin ပိုင်ခွင့်မရှိရင် Error တက်နိုင်သည်
                    print(f"Auto Promote Error: {e}")
                    
    except Exception as e:
        pass
