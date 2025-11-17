from bot import Bot
from pyrogram import idle

try:
    Bot.loop.run_until_complete(Bot.get_me())
    idle()
except Exception as e:
    print(f"Error deploying: {e}")
    Bot.stop()
