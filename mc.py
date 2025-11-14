import re
import uuid
import asyncio
import aiohttp
from pyrogram.types import Message, CallbackQuery
from xtra import ButtonMaker, send_message, edit_message

LOG_CHANNEL = [-1002405234042]
AUTH_CHATS = [-1002423975548]

CHECK_FORMAT = (
    "<blockquote><b>Name: {name}</b></blockquote>\n"
    "ᴛʏᴘᴇ : {type_}\n"
    "ᴛᴏᴛᴀʟ ғɪʟᴇs : {files}\n"
    "ᴛᴏᴛᴀʟ sᴜʙғᴏʟᴅᴇʀs : {folders}\n"
    "sɪᴢᴇ : {size}\n"
    'Lɪɴᴋ : <a href="{link}">Cʟɪᴄᴋ Hᴇʀᴇ</a>'
)
LINK_REGEX = r'https:\/\/mega\.nz\/(?:file|folder)\/[\w-]+(?:#[\w-]+)?'
API_URL = "https://mega-checker-api.onrender.com/api"

def parse_mega_json(data, link):
    name = data.get("name", "-")
    type_ = data.get("type", "-")
    files = data.get("files", "-")
    folders = data.get("folders", "-")
    size = data.get("sizeFormatted", "-")
    return CHECK_FORMAT.format(name=name, type_=type_, files=files, folders=folders, size=size, link=link)

async def send_log(client, user, links, results):
    if not LOG_CHANNEL:
        return
    log_channel_id = LOG_CHANNEL[0]
    user_display = f"@{user.username}" if getattr(user, "username", None) else f"{user.first_name} (<code>{user.id}</code>)"
    log_text = (
        f"<b>Check Task Log</b>\n"
        f"User: {user_display}\n"
        f"Checked {len(links)} MEGA link(s):\n"
        + "\n".join([f"<code>{link}</code>" for link in links]) +
        "\n\n<b>Results:</b>\n"
        + ("\n".join(results) if results else "No valid MEGA info found.")
    )
    try:
        await client.send_message(chat_id=log_channel_id, text=log_text, disable_web_page_preview=True)
    except Exception:
        pass

async def check_cmd(client, message: Message):
    if message.chat.id not in AUTH_CHATS:
        return
    text = message.text or message.caption or ""
    links = list({x.strip() for x in re.findall(LINK_REGEX, text) if x.strip()})
    if not links:
        return
    wait_msg = await send_message(message, f"Checking {len(links)} MEGA link{'s' if len(links) > 1 else ''}...", block=True)
    tasks = [check_single_link(link) for link in links]
    results = await asyncio.gather(*tasks)
    valid_results = [res for res in results if res]
    await send_log(client, message.from_user, links, valid_results)
    if not valid_results:
        return await edit_message(wait_msg, "No valid MEGA info found.", markdown=False)
    text_output = "\n".join(valid_results)
    user_display = f"@{message.from_user.username}" if getattr(message.from_user, "username", None) else f"{message.from_user.first_name} (<code>{message.from_user.id}</code>)"
    text_output += f"\n\n<b>By : {user_display}</b>"
    bm = ButtonMaker()
    if len(valid_results) == 1:
        match = re.search(LINK_REGEX, valid_results[0])
        if match:
            bm.url_button("Open in MEGA", match.group(0))
        await edit_message(wait_msg, text_output, buttons=bm.build_menu(1), markdown=False)
    else:
        await edit_message(wait_msg, text_output, markdown=False)

async def check_single_link(link):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, json={"url": link}) as resp:
                data = await resp.json()
        except Exception:
            return None
    if "error" in data:
        return None
    return parse_mega_json(data, link)
