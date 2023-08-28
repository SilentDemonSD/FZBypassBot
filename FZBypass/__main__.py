from FZBypass import Bypass, LOGGER
from pyrogram import idle
from os import path as ospath

async def restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await Bypass.edit_message_text(chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>")
        except Exception as e:
            LOGGER.error(e)

Bypass.start()
LOGGER.info('FZ Bot Started!')
Bypass.loop.run_until_complete(restart())
idle()
Bypass.stop()