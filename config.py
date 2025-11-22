import re
import os
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Telegram Channel Cache (File Storage)
#CACHE_CHANNEL_ID = -1003329159824

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", None))
API_HASH = getenv("API_HASH", None)

#COOKIES_URL = [
 #           url for url in getenv("COOKIES_URL", "").split(" ")
#            if url and "batbin.me" in url
  #      ]

COOKIE_URL = "https://batbin.me/cutlets"

#API_URL = getenv("API_URL", "https://api.thequickearn.xyz")
#API_KEY = getenv("API_KEY", "30DxNexGenBotsfcfad8")
#VIDEO_API_URL = getenv("VIDEO_API_URL", 'https://api.video.thequickearn.xyz')

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", None)

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", None)
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)

CLONE_DB_URI = getenv("CLONE_DB_URI", "mongodb+srv://wanglinmongodb:wanglin@renegadeimmortal.o1qj9yf.mongodb.net/?retryWrites=true&w=majority")

CLONE_ENABLED = getenv("CLONE_ENABLED", "True").lower() == "true"

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 900))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", None))

# Get this value from @BRANDRD_ROBOT on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "1318826936"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/maythu-shar-music/maythusharmusic",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL_LINK = getenv("SUPPORT_CHANNEL_LINK", "@everythingreset")
SUPPORT_CHAT_LINK = getenv("SUPPORT_CHAT_LINK", "@sasukemusicsupportchat")

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/everythingreset")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/sasukemusicsupportchat")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# Auto Gcast/Broadcast Handler (True = broadcast on , False = broadcast off During Hosting, Dont Do anything here.)
AUTO_GCAST = os.getenv("AUTO_GCAST")

# Auto Broadcast Message That You Want Use In Auto Broadcast In All Groups.
AUTO_GCAST_MSG = getenv("AUTO_GCAST_MSG", "")

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "bcfe26b0ebc3428882a0b5fb3e872473")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "907c6a054c214005aeae1fd752273cc4")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "50"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Auto End Stream ကို ဖွင့်ရန် True ၊ ပိတ်ရန် False ထားပါ
AUTO_END_STREAM = getenv("AUTO_END_STREAM", "True").lower() == "true"

# Cleanmode time after which bot will delete its old messages from chats
CLEANMODE_DELETE_MINS = int(getenv("CLEANMODE_MINS", "20"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "2000"))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2097152000))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes

CLONE_SESSIONS = {
    "session1": getenv("STRING1", ""),
    "session2": getenv("STRING2", ""), 
    "session3": getenv("STRING3", ""),
    "session4": getenv("STRING4", ""),
    "session5": getenv("STRING5", "")
}

# Get your pyrogram v2 session from @BRANDEDSTRINGSESSION_BOT on Telegram
STRING1 = getenv("STRING_SESSION",  None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

LOG = 2
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/0s2ipo.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://files.catbox.moe/0s2ipo.jpg"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
STATS_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
JOIN_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/0s2ipo.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/0s2ipo.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/0s2ipo.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
