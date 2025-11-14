import re
from pyrogram import Client, filters
from mc import check_cmd, LINK_REGEX

API_ID = 
API_HASH = ""
BOT_TOKEN = ""

app = Client("mega_checker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.text | filters.caption)
async def auto_check_mega(client, message):
    if not re.search(LINK_REGEX, message.text or message.caption or ""):
        return
    await check_cmd(client, message)

print("bot runnning")
app.run()
