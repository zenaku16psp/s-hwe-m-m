import re
import logging
import traceback
import os
import shutil
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from pyrogram.errors import AccessTokenInvalid, UserNotParticipant

from config import API_ID, API_HASH, OWNER_ID
from maythusharmusic import app
from maythusharmusic.utils.database import get_assistant

# --- DATABASE UTILS FOR PERMISSION (You might need to add these to database.py) ---
# For now, I will simulate these functions. 
# You should add 'clone_whitelist' collection to your MongoDB in database.py
from maythusharmusic.core.mongo import mongodb

clone_whitelist_db = mongodb.clone_whitelist

async def is_user_allowed(user_id: int) -> bool:
    user = await clone_whitelist_db.find_one({"user_id": user_id})
    return bool(user)

async def allow_user(user_id: int):
    await clone_whitelist_db.update_one(
        {"user_id": user_id},
        {"$set": {"allowed": True}},
        upsert=True
    )

async def disallow_user(user_id: int):
    await clone_whitelist_db.delete_one({"user_id": user_id})

# --------------------------------------------------------------------------------

CLONES = set()

# --- (၁) AUTO CHECK MAIN BOT FUNCTION ---
async def auto_check_main_bot(clone_client):
    """Clone Bot ရှိသော Group များတွင် Main Bot ရှိမရှိ စစ်ဆေးပြီး မရှိရင် ထည့်သည်"""
    try:
        if not app.me:
            await app.get_me()
        main_bot_username = app.me.username
        main_bot_id = app.me.id

        async for dialog in clone_client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                chat_id = dialog.chat.id
                try:
                    await clone_client.get_chat_member(chat_id, main_bot_id)
                except UserNotParticipant:
                    try:
                        userbot = await get_assistant(chat_id)
                        await userbot.add_chat_members(chat_id, main_bot_username)
                    except Exception:
                        pass 
                except Exception:
                    pass
                await asyncio.sleep(2)
                
    except Exception as e:
        print(f"Auto Sync Error for {clone_client.me.username}: {e}")


# --- (NEW) OWNER COMMANDS TO MANAGE PERMISSIONS ---

@app.on_message(filters.command("authorize") & filters.user(OWNER_ID))
async def authorize_cloning(client, message: Message):
    """Owner မှ User တစ်ယောက်ကို Clone ပြုလုပ်ခွင့်ပေးခြင်း"""
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/authorize [User_ID]`")
    
    try:
        user_id = int(message.text.split(None, 1)[1])
        await allow_user(user_id)
        await message.reply_text(f"✅ **User {user_id} has been authorized to create Clone Bots.**")
    except ValueError:
        await message.reply_text("❌ Invalid User ID.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@app.on_message(filters.command("unauthorize") & filters.user(OWNER_ID))
async def unauthorize_cloning(client, message: Message):
    """Owner မှ User တစ်ယောက်ကို Clone ပြုလုပ်ခွင့်ပြန်ရုတ်သိမ်းခြင်း"""
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/unauthorize [User_ID]`")
    
    try:
        user_id = int(message.text.split(None, 1)[1])
        await disallow_user(user_id)
        await message.reply_text(f"🚫 **User {user_id} has been unauthorized.**")
    except ValueError:
        await message.reply_text("❌ Invalid User ID.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")


# --- MODIFIED CLONE COMMAND ---

@app.on_message(filters.command("clone") & filters.private)
async def clone_txt(client, message: Message):
    # Variable Initialization
    bot_token = None
    user_id = message.from_user.id
    
    try:
        try:
            from maythusharmusic.utils.database import save_clone, get_clone_by_user, is_clones_active
        except ImportError:
            return await message.reply_text("❌ Database Error: Module Import Failed")

        # --- (၁) OWNER PERMISSION CHECK ---
        # Owner ကိုယ်တိုင်မဟုတ်ရင် Database မှာ ခွင့်ပြုထားခြင်းရှိမရှိ စစ်မယ်
        if user_id != OWNER_ID:
            if not await is_user_allowed(user_id):
                return await message.reply_text(
                    "⚠️ **Permission Denied!**\n\n"
                    "Clone Bot ပြုလုပ်ခွင့်ကို **Owner** မှ တိုက်ရိုက်ခွင့်ပြုချက်ရမှသာ အသုံးပြုနိုင်ပါသည်။\n"
                    "ကျေးဇူးပြု၍ Bot ပိုင်ရှင် (@iwillgoforwardsalone) ထံ ဆက်သွယ်ပြီး ခွင့်ပြုချက်တောင်းခံပါ။\n\n"
                    f"Your ID: `{user_id}`"
                )
        # ----------------------------------

        # --- (၂) SYSTEM ON/OFF CHECK ---
        if not await is_clones_active():
            return await message.reply_text(
                "> •**𝙎𝙮𝙨𝙩𝙚𝙢 𝙈𝙖𝙞𝙣𝙩𝙚𝙣𝙖𝙣𝙘𝙚**\n"
                ">\n"
                "> •𝘾𝙡𝙤𝙣𝙚 𝙗𝙤𝙩 စနစ်ကို 𝙊𝙬𝙣𝙚𝙧 မှ ယာယီပိတ်ထားပါသည်။\n"
                "> •ခေတ္တစောင့်ဆိုင်းပြီးမှ ပြန်လည်ကြိုးစားပါ။"
            )

        # --- (၃) ONE USER ONE BOT LIMIT CHECK ---
        existing_clone = await get_clone_by_user(user_id)
        
        if existing_clone:
            bot_username = existing_clone.get("bot_username", "Unknown")
            bot_token_existing = existing_clone.get("bot_token", "")
            return await message.reply_text(
                f"𝗡𝗼𝘁𝗶𝗰 𝗙𝗼𝗿 𝗨𝘀𝗲𝗿𝘀\n\n"
                f"𝙔𝙤𝙪 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙝𝙖𝙫𝙚 𝙖 𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩.\n"
                f"𝗕𝗼𝘁 : @{bot_username}\n\n"
                f"𝙄𝙛 𝙮𝙤𝙪 𝙬𝙖𝙣𝙩 𝙩𝙤 𝙘𝙧𝙚𝙖𝙩𝙚 𝙖 𝙣𝙚𝙬 𝙤𝙣𝙚, 𝙙𝙚𝙡𝙚𝙩𝙚 𝙩𝙝𝙚 𝙚𝙭𝙞𝙨𝙩𝙞𝙣𝙜 𝘽𝙤𝙩 𝙛𝙞𝙧𝙨𝙩.\n"
                f"><code>/delclone {bot_token_existing}</code>"
            )

        if len(message.command) < 2:
            return await message.reply_text(
                "<b>D͟e͟v͟e͟l͟o͟p͟e͟r͟ : @iwillgoforwardsalone</b>\n\n/clone [Bot Token]\n\nGᴇᴛ ʙᴏᴛ ᴛᴏᴋᴇɴ ꜰʀᴏᴍ @BotFather"
            )
        
        bot_token = message.text.split(None, 1)[1]
        
        if not re.match(r'^\d+:[a-zA-Z0-9_-]+$', bot_token):
            return await message.reply_text("❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗕𝗼𝘁 𝗧𝗼𝗸𝗲𝗻.")

        msg = await message.reply_text("𝘾𝙧𝙚𝙖𝙩𝙞𝙣𝙜 𝙢𝙪𝙨𝙞𝙘 𝙗𝙤𝙩.𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩...")

        try:
            ai = Client(
                name=bot_token,
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=bot_token,
                plugins=dict(root="maythusharmusic.plugins.clone_plugins"),
            )
            
            await ai.start()
            bot_info = await ai.get_me()
            username = bot_info.username
            bot_mention = f"[{bot_info.first_name}](tg://user?id={bot_info.id})"
            
            await save_clone(bot_token, user_id, username)
            CLONES.add(bot_token)
            
            # Clone ပြီးသွားရင် Permission ကို ပြန်ဖြုတ်မယ် (One-time permission)
            # အကယ်၍ အမြဲပေးထားချင်ရင် ဒီလိုင်းကို ဖြုတ်လိုက်ပါ
            if user_id != OWNER_ID:
                await disallow_user(user_id)

            details = f"""
•✅𝗖𝗹𝗼𝗻𝗲 𝗕𝗼𝘁 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗰𝗿𝗲𝗮𝘁𝗲𝗱.

• 𝘽𝙤𝙩 𝙉𝙖𝙢𝙚 : {bot_mention}
• 𝙐𝙨𝙚𝙣𝙖𝙢𝙚 : @{username}
• 𝙇𝙞𝙨𝙩𝙚𝙣 𝙩𝙤 𝙢𝙪𝙨𝙞𝙘,𝙖𝙙𝙙 𝙮𝙤𝙪𝙧 𝙘𝙡𝙤𝙣𝙚 𝙗𝙤𝙩 𝙩𝙤 𝙩𝙝𝙚 𝙜𝙧𝙤𝙪𝙥 𝙖𝙣𝙙 𝙜𝙞𝙫𝙚 𝙞𝙩 𝙖𝙙𝙢𝙞𝙣 𝙨𝙩𝙖𝙩𝙪𝙨.
"""
            await msg.edit_text(details)
            
        except AccessTokenInvalid:
            await msg.edit_text("❌ ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ.")
        except Exception as e:
            await msg.edit_text(f"❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}")
        
    except Exception as e:
        await message.reply_text(f"❌ Unexpected error: {e}")

# ... (Rest of the file: delclone, checkbot, delallclones, restart_clones, clone_mode_switch remains the same) ...

@app.on_message(filters.command("delclone") & filters.private)
async def delete_clone_bot(client, message: Message):
    # ... (Same as before) ...
    try:
        from maythusharmusic.utils.database import delete_clone, get_clone_by_user
        
        token = None
        if len(message.command) >= 2:
            token = message.text.split(None, 1)[1]
        else:
            user_clone = await get_clone_by_user(message.from_user.id)
            if user_clone:
                token = user_clone.get("bot_token")
            else:
                return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀ ᴄʟᴏɴᴇ ʙᴏᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ.")

        if token:
            await delete_clone(token)
            if token in CLONES:
                CLONES.remove(token)
            await message.reply_text("✅ ᴄʟᴏɴᴇ ʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴜɴɪɴꜱᴛᴀʟʟᴇᴅ.")
        else:
            await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ ᴏʀ ɴᴏ ᴄʟᴏɴᴇ ʙᴏᴛ ꜰᴏᴜɴᴅ.")
        
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ : {e}")

@app.on_message(filters.command("checkbot") & filters.user(OWNER_ID))
async def total_clones_stats(client, message: Message):
    # ... (Same as before) ...
    try:
        from maythusharmusic.utils.database import get_clones
        clones = await get_clones()
        
        total = len(clones)
        text = f"📊 <b>𝗖𝗹𝗼𝗻𝗲 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀</b>\n\n"
        text += f"🤖 <b>𝗧𝗼𝘁𝗮𝗹 𝗖𝗹𝗼𝗻𝗲𝘀 : </b> {total}\n\n"
        
        if total > 0:
            text += "<b>𝗕𝗼𝘁 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲𝘀 : </b>\n"
            for count, clone in enumerate(clones, 1):
                username = clone.get("bot_username", "Unknown")
                text += f"{count}. @{username}\n"
        
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@app.on_message(filters.command("delallclones") & filters.user(OWNER_ID))
async def delete_all_clones_func(client, message: Message):
    # ... (Same as before) ...
    try:
        from maythusharmusic.utils.database import remove_all_clones, get_clones
        
        if len(message.command) < 2 or message.text.split()[1] != "confirm":
            return await message.reply_text(
                "𝗪𝗮𝗿𝗻𝗶𝗻𝗴\n"
                "𝗔𝗿𝗲 𝘆𝗼𝘂 𝘀𝘂𝗿𝗲 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝗱𝗲𝗹𝗲𝘁𝗲 𝗮𝗹𝗹 𝗖𝗹𝗼𝗻𝗲 𝗕𝗼𝘁𝘀.\n"
                "𝙄𝙛 𝙮𝙤𝙪 𝙖𝙧𝙚 𝙨𝙪𝙧𝙚, 𝙩𝙮𝙥𝙚 𝙩𝙝𝙚 𝙛𝙤𝙡𝙡𝙤𝙬𝙞𝙣𝙜 :\n"
                "<code>/delallclones confirm</code>"
            )
            
        msg = await message.reply_text("♻️ <b>𝘼𝙡𝙡 𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩𝙨 𝙖𝙧𝙚 𝙗𝙚𝙞𝙣𝙜 𝙙𝙚𝙡𝙚𝙩𝙚𝙙...</b>")
        
        await remove_all_clones()
        CLONES.clear()
        
        await msg.edit_text("✅ <b>𝘼𝙡𝙡 𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩𝙨 𝙝𝙖𝙫𝙚 𝙗𝙚𝙚𝙣 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙙𝙚𝙡𝙚𝙩𝙚𝙙 𝙛𝙧𝙤𝙢 𝙩𝙝𝙚 𝘿𝙖𝙩𝙖𝙗𝙖𝙨𝙚.</b>\n\n𝙍𝙚𝙨𝙩𝙖𝙧𝙩 𝙩𝙝𝙚 𝙗𝙤𝙩 𝙛𝙤𝙧 𝙩𝙝𝙚 𝙚𝙛𝙛𝙚𝙘𝙩 𝙩𝙤 𝙩𝙖𝙠𝙚 𝙚𝙛𝙛𝙚𝙘𝙩. (/reboot)")
        
    except Exception as e:
        await message.reply_text(f"Error: {e}")

async def restart_clones():
    # ... (Same as before) ...
    try:
        from maythusharmusic.utils.database import get_clones
        clones = await get_clones()
        
        if not clones:
            return
        
        print(f"Total Clones Found: {len(clones)}")
        
        for clone in clones:
            token = clone["bot_token"]
            try:
                ai = Client(
                    name=token,
                    api_id=API_ID,
                    api_hash=API_HASH,
                    bot_token=token,
                    plugins=dict(root="maythusharmusic.plugins.clone_plugins"),
                )
                await ai.start()
                print(f"𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗖𝗹𝗼𝗻𝗲 : @{clone['bot_username']}")
                CLONES.add(token)
            except Exception as e:
                print(f"Failed to start clone {token}: {e}")
    except ImportError:
        print("Database module loading error inside restart_clones")
    except Exception as e:
        print(f"Error in restart_clones: {e}")

@app.on_message(filters.command("clonebot") & filters.user(OWNER_ID))
async def clone_mode_switch(client, message: Message):
    # ... (Same as before) ...
    try:
        from maythusharmusic.utils.database import set_clones_active, is_clones_active
        
        if len(message.command) != 2:
            status = await is_clones_active()
            txt = "✅ <b>Enabled</b>" if status else "❌ <b>Disabled</b>"
            return await message.reply_text(f"<b>Current Clone System Status:</b> {txt}\n\n<b>Usage:</b> <code>/clonebot [on|off]</code>")
            
        state = message.text.split(None, 1)[1].strip().lower()
        
        if state == "on" or state == "enable":
            await set_clones_active(True)
            await message.reply_text("✅ <b>𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩 𝙎𝙮𝙨𝙩𝙚𝙢 𝙝𝙖𝙨 𝙗𝙚𝙚𝙗 𝙖𝙘𝙩𝙞𝙫𝙖𝙩𝙚𝙙.</b>\n𝘼𝙡𝙡 𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩𝙨 𝙬𝙞𝙡𝙡 𝙧𝙚𝙨𝙪𝙢𝙚 𝙣𝙤𝙧𝙢𝙖𝙡 𝙤𝙥𝙚𝙧𝙖𝙩𝙞𝙤𝙣.")
            
        elif state == "off" or state == "disable":
            await set_clones_active(False)
            await message.reply_text("❌ <b>𝙏𝙝𝙚 𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩 𝙎𝙮𝙨𝙩𝙚𝙢 𝙝𝙖𝙨 𝙗𝙚𝙚𝙣 𝙙𝙞𝙨𝙖𝙗𝙡𝙚𝙙.</b>\n𝘼𝙡𝙡 𝘾𝙡𝙤𝙣𝙚 𝘽𝙤𝙩𝙨 𝙬𝙞𝙡𝙡 𝙨𝙝𝙤𝙬 '𝙐𝙣𝙙𝙚𝙧 𝙈𝙖𝙞𝙣𝙩𝙚𝙣𝙖𝙣𝙘𝙚'.")
            
        else:
            await message.reply_text("<b>Usage:</b> <code>/clonebot [on|off]</code>")
            
    except Exception as e:
        await message.reply_text(f"Error: {e}")
