from FZBypass import Config, Bypass
from pyrogram.filters import command, private, text
from FZBypass.core.bypass_ddl import canBypass
from FZBypass.core.bot_utils import chat_and_topics
from FZBypass.core.exceptions import DDLException

@Bypass.on_message(command(['start'] & ~private))
async def start_msg(client, message):
    await message.reply('<b>FZ Bypass Bot! Up & Running!</b>')
    
@Bypass.on_message(command(['bypass', 'bp']) & text & chat_and_topics)
async def bypass_check(client, message):
    uid = message.from_user.id
    arg = message.text.split('\n')[0].split()
    if reply_to := message.reply_to_message and hasattr(reply_to, "text"):
        link = reply_to.text
    elif len(arg) > 1:
        link = arg[1]
    else:
        link = ''
    if link == '':
        return await message.reply('<i>No Link Provided!</i>')
    try:
        by_link = await direct_link_checker(link)
    except DDLException as error:
        return await message.reply(error)
    except Exception as e:
        return await message.reply(str(e))

    if by_link:
        await message.reply(f"<b>Bypassed Link :</b> <code>{by_link}</code>")
    
