from FZBypass import Config, Bypass
from pyrogram import filters

@Bypass.on_message(filters.command(['start']))
async def start_msg(client, message):
    await message.reply_text('I am Working')