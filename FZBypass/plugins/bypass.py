from time import time
from pyrogram.filters import command, private, user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import MessageEntityType

from FZBypass import Config, Bypass, BOT_START
from FZBypass.core.bypass_checker import direct_link_checker, is_share_link
from FZBypass.core.bot_utils import chat_and_topics, convert_time
from FZBypass.core.exceptions import DDLException


@Bypass.on_message(command('start'))
async def start_msg(client, message):
    await message.reply(f'''<b><i>FZ Bypass Bot!</i></b>
    
    <i>A Powerful Elegant Multi Threaded Bot written in Python... which can Bypass Various Shortener Links, Scrape links, and More ... </i>
    
    <i><b>Bot Started {convert_time(time() - BOT_START)} ago...</b></i>

🛃 <b>Use Me Here :</b> @CyberPunkGrp <i>(Bypass Topic)</i>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🎓 Dev', url='https://t.me/SilentDemonSD'), InlineKeyboardButton('🔍 Deploy Own', url="https://github.com/SilentDemonSD/FZBypassBot")]
            ])
    )


@Bypass.on_message(command(['bypass', 'bp']) & chat_and_topics)
async def bypass_check(client, message):
    uid = message.from_user.id
    if (reply_to := message.reply_to_message) and (reply_to.text is not None or reply_to.caption is not None):
        txt = reply_to.text or reply_to.caption
        entities = reply_to.entities or reply_to.caption_entities
    elif len(message.command) > 1:
        txt = message.text
        entities = message.entities
    else:
        return await message.reply('<i>No Link Provided!</i>')
    
    wait_msg = await message.reply("<i>Bypassing...</i>")
    start = time()

    parse_data = []
    link, no = '', 0
    for enty in entities:
        if enty.type == MessageEntityType.URL:
            link = txt[enty.offset:(enty.offset+enty.length)]
        elif enty.type == MessageEntityType.TEXT_LINK:
            link = enty.url
            
        if link:
            no += 1
            try:
                bp_link = await direct_link_checker(link)
            except Exception as e:
                bp_link = str(e)
            if is_share_link(link):
                parse_data.append(bp_link)
            else:
                parse_data.append(f'┎ <b>Link:</b> {link}\n┃\n┖ <b>Bypassed Link:</b> {bp_link}\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n')
            link = ''
            
    end = time()

    parse_data[-1] = parse_data[-1] + f"🔗 <b>Total Links:</b> <i>{no}</i> & <b>Took Only </b> <i>{convert_time(end - start)}</i>!"
    tg_txt = ""
    for tg_data in parse_data:
        tg_txt += tg_data
        if len(tg_txt) > 4000:
            await wait_msg.edit(tg_txt, disable_web_page_preview=True)
            wait_msg = await message.reply("<i>Fetching...</i>", reply_to_message_id=wait_msg.id)
    
    if tg_txt != "":
        await wait_msg.edit(tg_txt, disable_web_page_preview=True)


@Bypass.on_message(command('log') & user(Config.OWNER_ID))
async def send_logs(client, message):
    await message.reply_document('log.txt', quote=True)
