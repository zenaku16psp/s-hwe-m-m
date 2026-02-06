import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from maythusharmusic import LOGGER, app, userbot, YouTube
from maythusharmusic.core.call import pisces
from maythusharmusic.misc import sudo
from maythusharmusic.plugins import ALL_MODULES
from maythusharmusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# --- Clone Bot Function ကို Import လုပ်ခြင်း ---
#from maythusharmusic.plugins.bot.clone import restart_clones 
#from maythusharmusic.core.cleanmode import clean_mode_task
# -------------------------------------------

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("maythusharmusic.plugins" + all_module)
    LOGGER("maythusharmusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await pisces.start()
    
    # --- Clone Bot များကို စတင်ခြင်း ---
    #LOGGER("maythusharmusic").info("Clone Bot များကို စတင်နေပါသည်...")
    #try:
        #await restart_clones()
        #LOGGER("maythusharmusic").info("Clone Bots များ အောင်မြင်စွာ စတင်ပြီးပါပြီ။")
    #except Exception as e:
        #LOGGER("maythusharmusic").error(f"Clone Bots စတင်ရာတွင် အမှားရှိသည်: {e}")
    # -------------------------------

    try:
        await pisces.stream_call("https://files.catbox.moe/y2cu6k.mp4")
    except NoActiveGroupCall:
        LOGGER("maythusharmusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await pisces.decorators()
    LOGGER("maythusharmusic").info(
        "ᴅʀᴏᴘ ʏᴏᴜʀ ɢɪʀʟꜰʀɪᴇɴᴅ'ꜱ ɴᴜᴍʙᴇʀ ᴀᴛ @sasukevipmusicbotsupport..."
    )
    LOGGER("maythusharmusic").info(
        "ᴅʀᴏᴘ ʏᴏᴜʀ ɢɪʀʟꜰʀɪᴇɴᴅ'ꜱ ɴᴜᴍʙᴇʀ ᴀᴛ @sasukevipmusicbotsupport ᴊᴏɪɴ @sasukevipmusicbot , @sasukevipmusicbotsupport ꜰᴏʀ ᴀɴʏ ɪꜱꜱᴜᴇꜱ"
    )
  #  LOGGER("maythusharmusic").info("Clean Mode စနစ်ကို စတင်နေပါသည်...")
#    asyncio.create_task(clean_mode_task())
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("maythusharmusic").info("Stopping Sasuke Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
