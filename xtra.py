import logging
from pyrogram import enums
from asyncio import gather, sleep
from pyrogram.errors import FloodWait, MessageNotModified, MessageEmpty
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def delete_message(*args):
    msgs = [msg.delete() for msg in args if msg]
    results = await gather(*msgs, return_exceptions=True)
    for msg, result in zip(args, results, strict=False):
        if isinstance(result, Exception):
            logging.error(f"Failed to delete message {msg}: {result}", exc_info=True)

async def edit_message(message, text, buttons=None, markdown=False):
    parse_mode = enums.ParseMode.MARKDOWN if markdown else enums.ParseMode.HTML
    try:
        await message.edit(
            text=text,
            disable_web_page_preview=True,
            reply_markup=buttons,
            parse_mode=parse_mode,
        )
    except FloodWait as f:
        await sleep(f.value * 1.2)
        return await edit_message(message, text, buttons, markdown)
    except (MessageNotModified, MessageEmpty):
        pass
    except Exception as e:
        logging.error(str(e))
        raise

async def send_message(
    message,
    text,
    buttons=None,
    photo=None,
    markdown=False,
    block=True,
):
    parse_mode = enums.ParseMode.MARKDOWN if markdown else enums.ParseMode.HTML
    try:
        if isinstance(message, int):
            from .. import app
            return await app.send_message(
                chat_id=message,
                text=text,
                disable_web_page_preview=True,
                disable_notification=True,
                reply_markup=buttons,
                parse_mode=parse_mode,
            )
        if photo:
            return await message.reply_photo(
                photo=photo,
                reply_to_message_id=message.id,
                caption=text,
                reply_markup=buttons,
                disable_notification=True,
                parse_mode=parse_mode,
            )
        return await message.reply(
            text=text,
            quote=True,
            disable_web_page_preview=True,
            disable_notification=True,
            reply_markup=buttons,
            parse_mode=parse_mode,
        )
    except FloodWait as f:
        logging.warning(str(f))
        if not block:
            return message
        await sleep(f.value * 1.2)
        return await send_message(message, text, buttons, photo, markdown)
    except Exception as e:
        logging.error(str(e))
        raise

class ButtonMaker:
    def __init__(self):
        self._button = []
        self._header_button = []
        self._footer_button = []

    def data_button(self, key, data, position=None):
        btn = InlineKeyboardButton(text=key, callback_data=data)
        if not position:
            self._button.append(btn)
        elif position == "header":
            self._header_button.append(btn)
        elif position == "footer":
            self._footer_button.append(btn)

    def url_button(self, key, url, position=None):  # ✅ New method
        btn = InlineKeyboardButton(text=key, url=url)
        if not position:
            self._button.append(btn)
        elif position == "header":
            self._header_button.append(btn)
        elif position == "footer":
            self._footer_button.append(btn)

    def new_row(self):
        self._button.append(None)

    def build_menu(self, b_cols=2, h_cols=8, f_cols=8):
        menu = []
        row = []
        for btn in self._button:
            if btn is None:
                if row:
                    menu.append(row)
                row = []
            else:
                row.append(btn)
                if len(row) == b_cols:
                    menu.append(row)
                    row = []
        if row:
            menu.append(row)
        if self._header_button:
            h_cnt = len(self._header_button)
            if h_cnt > h_cols:
                header_buttons = [self._header_button[i:i + h_cols] for i in range(0, len(self._header_button), h_cols)]
                menu = header_buttons + menu
            else:
                menu.insert(0, self._header_button)
        if self._footer_button:
            f_cnt = len(self._footer_button)
            if f_cnt > f_cols:
                [menu.append(self._footer_button[i:i + f_cols]) for i in range(0, len(self._footer_button), f_cols)]
            else:
                menu.append(self._footer_button)
        return InlineKeyboardMarkup(menu)
