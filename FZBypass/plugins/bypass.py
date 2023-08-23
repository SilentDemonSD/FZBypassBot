from time import time
from re import match
from asyncio import create_task, gather
from pyrogram.filters import command, private, user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
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

    link, tlinks, no = '', [], 0
    atasks = []
    for enty in entities:
        if enty.type == MessageEntityType.URL:
            link = txt[enty.offset:(enty.offset+enty.length)]
        elif enty.type == MessageEntityType.TEXT_LINK:
            link = enty.url
            
        if link:
            no += 1
            tlinks.append(link)
            atasks.append(create_task(direct_link_checker(link)))
            link = ''

    completed_tasks = await gather(*atasks, return_exceptions=True)
    
    parse_data = []
    for result, link in zip(completed_tasks, tlinks):
        if isinstance(result, Exception):
            bp_link = f"<b>Bypass Error:</b> {result}"
        elif is_share_link(link):
            bp_link = result
        else:
            bp_link = f"<b>Bypass Link:</b> {result}"
        
        if is_share_link(link):
            parse_data.append(bp_link + "\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n")
        else:
            parse_data.append(f'┎ <b>Source Link:</b> {link}\n┃\n┖ {bp_link}\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n')
            
    end = time()

    parse_data[-1] = parse_data[-1] + f"🔗 <i><b>Total Links : {no}</b>\n🧭 <b>Took Only <code>{convert_time(end - start)}</code></b></i> !\n#cc : {message.from_user.mention} ( #ID{message.from_user.id} )"
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


@Bypass.on_inline_query()
async def inline_query(client, query):
    answers = [] 
    string = query.query.lower()
    if bool(match(r"^\!bp https?\:\/\/S+", string)):
        await asleep(2)
        link = string.strip('!bp ')
        try:
            bp_link = await direct_link_checker(link)
            if not is_share_link(link):
                bp_link = f"<b>Bypass Link:</b> {bp_link}"
            answers.append(InlineQueryResultArticle(
                title="✅️ <b>Bypassed Link !</b>",
                input_message_content=InputTextMessageContent(
                    f'┎ <b>Source Link:</b> {link}\n┃\n┖ {bp_link}\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n'
                ),
                description="Bypass Any Link Anywhere : !bp [Link]",
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('Bypass Again', switch_inline_query_current_chat="!bp ")]
                ])
            ))
        except Exception as e:
            bp_link = f"<b>Bypass Error:</b> {e}"
            answers.append(InlineQueryResultArticle(
                title="❌️ <b>Bypass Link Error !</b>",
                input_message_content=InputTextMessageContent(
                    f'┎ <b>Source Link:</b> {link}\n┃\n┖ {bp_link}\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n'
                ),
                description="Try any Other Link : !bp [Link]",
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('Bypass Again', switch_inline_query_current_chat="!bp ")]
                ])
            ))    
        
    else:
        answers.append(InlineQueryResultArticle(
                title="Inline Bypass Usage",
                input_message_content=InputTextMessageContent(
                    "Inline Bypass via this Bot !"
                ),
                description="Bypass Format : !bp [Link]",
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Dev", url="https://t.me/SilentDemonSD"),
                        InlineKeyboardButton('Bypass Now', switch_inline_query_current_chat="!bp ")]
                ])
            ))
    await query.answer(
        results=answers,
        cache_time=0
    )
