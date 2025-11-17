from pyrogram import Client
from uvloop import install
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN

install()

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

Bot = Client(
    "MegaCheckerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"},
    workers=50
)

Bot.start()
print("Echo Client started.")

Bot.me = Bot.get_me()
print(f"Echo Bot Started: {Bot.me.username}")
