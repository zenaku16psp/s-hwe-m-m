from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from maythusharmusic import app
from maythusharmusic.utils.database import is_clones_active

CLONE_START_IMAGE_URL = "https://files.catbox.moe/2uahrk.jpg"

# Quote ပုံစံပေါ်ဖို့အတွက် စာကြောင်းရှေ့မှာ > ကိုထည့်ပေးထားပါတယ်
START_TEXT = """
> • ʜᴇʏ ʙᴀʙʏ : {} 👋
> • ɪ ᴀᴍ {}, ʜᴇʀᴇ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴡɪᴛʜ ᴀ ꜱᴍᴏᴏᴛʜ ᴍᴜꜱɪᴄ ꜱᴛʀᴇᴀᴍɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ 🦋.

> • ғᴇᴀᴛᴜʀᴇs
> • ʜǫ ᴀᴜᴅɪᴏ : 320ᴋʙᴘs sᴛʀᴇᴀᴍɪɴɢ
> • sᴛʀᴇᴀᴍ sᴜᴘᴘᴏʀᴛ : ᴀᴜᴅɪᴏ-ᴠɪᴅᴇᴏ
> • 24-7 ᴜᴘᴛɪᴍᴇ : ᴇɴᴛᴇʀᴘʀɪsᴇ ʀᴇʟɪᴀʙɪʟɪᴛʏ
> • ᴘʟᴀʏ ᴄᴏᴍᴍᴇɴᴛꜱ : ᴘʟᴀʏ, ᴠᴘʟᴀʏ 
> • ʙᴇsᴇᴅ ᴏɴ : ʏᴏᴜᴛᴜʙᴇ ᴀᴘɪ

> • ᴜsᴇ /clone ᴄᴏᴍᴍᴀɴᴅ
> • ɢᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ɪɴ sᴇᴄᴏɴᴅs •
> •ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ 🦋.
"""

@Client.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    # Clone system status check
    if not await is_clones_active():
        return await message.reply_text(">**ꜱᴏʀʀʏ, ᴄʟᴏɴᴇ ʙᴏᴛ ꜱʏꜱᴛᴇᴍ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ᴏꜰꜰ ꜰᴏʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.**")
    
    # Bot username ကိုရယူခြင်း
    app_username = (await client.get_me()).username
    bot_info = await client.get_me()
    bot_mention = f"[{bot_info.first_name}](tg://user?id={bot_info.id})"
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ",
                    url=f"https://t.me/{app_username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users+add_admins"
                )
            ],
            [
                InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/iwillgoforwardsalone"),
                InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/sasukemusicsupportchat"),
            ],
            [
                InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url="https://t.me/everythingreset"),
            ],
        ]
    )
    
    # START_IMAGE_URL ရှိမရှိစစ်ဆေးခြင်း
    if CLONE_START_IMAGE_URL:
        await message.reply_photo(
            photo=CLONE_START_IMAGE_URL,
            caption=START_TEXT.format(message.from_user.mention, bot_mention),
            reply_markup=keyboard,
        )
    else:
        await message.reply_text(
            START_TEXT.format(message.from_user.mention, bot_mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )


@Client.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    # Clone system status check for groups
    if not await is_clones_active():
        return await message.reply_text("⚠️ <b>Sorry, Clone Bot System is currently OFF for maintenance.</b>")
    
    # Group start message
    await message.reply_text(
        "**ʜᴇʟʟᴏ,ɪ ᴀᴍ ʀᴇᴀᴅʏ ᴛᴏ ᴘʟᴀʏ ᴍᴜꜱɪᴄ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.**\n"
        "**ᴜꜱᴇ /ᴘʟᴀʏ ᴛᴏ ꜱᴛᴀʀᴛ ꜱᴛʀᴇᴀᴍɪɴɢ ᴍᴜꜱɪᴄ**",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", 
                                   url=f"https://t.me/{(await client.get_me()).username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users+add_admins")
            ]
        ])
    )


@Client.on_message(filters.command("clone") & filters.private)
async def clone_command(client: Client, message: Message):
    """Clone bot ဖန်တီးရန် command"""
    
    # Clone system status check
    if not await is_clones_active():
        return await message.reply_text("⚠️ <b>Sorry, Clone Bot System is currently OFF for maintenance.</b>")
    
    clone_text = """
> 𝗖𝗹𝗼𝗻𝗲 𝗕𝗼𝘁 𝗦𝘆𝘀𝘁𝗲𝗺**

> •ɢᴏ ᴛᴏ @sasukevipmusicbot ᴛᴏ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴍᴜꜱɪᴄ ʙᴏᴛ.
> •ʏᴏᴜ ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ᴀ ᴄʟᴏɴᴇ ʙᴏᴛ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.
    """
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "ᴄʀᴇᴀᴛᴇ ᴄʟᴏɴᴇ ʙᴏᴛ", 
                url="https://t.me/sasukevipmusicbot"
            )
        ],
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_main")
        ]
    ])
    
    await message.reply_text(
        clone_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


# Callback query handler for back button
@app.on_callback_query(filters.regex("back_to_main"))
async def back_to_main(client, callback_query):
    """Main menu သို့ ပြန်သွားရန် callback handler"""
    await callback_query.answer()
    
    app_username = (await client.get_me()).username
    bot_info = await client.get_me()
    bot_mention = f"[{bot_info.first_name}](tg://user?id={bot_info.id})"
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                    url=f"https://t.me/{app_username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users+ban_users"
                )
            ],
            [
                InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/iwillgoforwardsalone"),
                InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/sasukemusicsupportchat"),
            ],
            [
                InlineKeyboardButton("ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url="https://t.me/everythingreset"),
            ],
        ]
    )
    
    if CLONE_START_IMAGE_URL:
        await callback_query.message.edit_media(
            media=InputMediaPhoto(CLONE_START_IMAGE_URL),
            caption=START_TEXT.format(callback_query.from_user.mention, bot_mention),
            reply_markup=keyboard,
        )
    else:
        await callback_query.message.edit_text(
            START_TEXT.format(callback_query.from_user.mention, bot_mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
