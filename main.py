from bot import Bot
from pyrogram import idle

try:
    idle()
except Exception as e:
    print(f"Error deploying: {e}")
    Bot.stop()
