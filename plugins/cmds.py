import re
from pyrogram import Client, filters
from xtra import check_cmd, LINK_REGEX

WELCOME = "Hello! Send me any MEGA link and I will check it."

@Client.on_message((filters.text | filters.caption) & ~filters.command(["start"]))
async def auto_check_mega(client, message):
    text = message.text or message.caption or ""
    if not re.search(LINK_REGEX, text):
        return
    await check_cmd(client, message)

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(WELCOME, quote=True)
