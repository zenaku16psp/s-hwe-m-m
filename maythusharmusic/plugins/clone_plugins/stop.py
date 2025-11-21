from pyrogram import Client, filters
from pyrogram.types import Message

from maythusharmusic import app
from maythusharmusic.core.call import pisces
from maythusharmusic.utils.database import set_loop
from maythusharmusic.utils.decorators import AdminRightsCheck
from maythusharmusic.utils.inline import close_markup
from config import BANNED_USERS


@Client.on_message(
    filters.command(["end", "stop", "cend", "cstop"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await pisces.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
