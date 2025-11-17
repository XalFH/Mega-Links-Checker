import re
from pyrogram import Client, filters
from mc import check_cmd, LINK_REGEX

@Client.on_message(filters.text | filters.caption)
async def auto_check_mega(client, message):
    if not re.search(LINK_REGEX, message.text or message.caption or ""):
        return
    await check_cmd(client, message)
