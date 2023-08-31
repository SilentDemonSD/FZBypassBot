from pyrogram.filters import create
from re import search
from requests import get as rget
from urllib.parse import urlparse, parse_qs
from FZBypass import Config

async def auth_topic(_, __, message):
    for chat in Config.AUTH_CHATS:
        if ':' in chat:
            chat_id, topic_id = chat.split(':')
            if (int(chat_id) == message.chat.id 
                and (is_forum := message.reply_to_message)
                and ((is_forum.text is None and int(topic_id) == is_forum.id)
                or (is_forum.text is not None and int(topic_id) == is_forum.reply_to_message_id))):
                return True
        elif int(chat) == message.chat.id:
            return True
    return False

chat_and_topics = create(auth_topic)

def get_gdriveid(link):
    if "folders" in link or "file" in link:
        res = search(r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)", link)
        return res.group(3)
    parsed = urlparse(link)
    return parse_qs(parsed.query)['id'][0]

def get_dl(link):
    try:
        return rget(f"{Config.DIRECT_INDEX}/generate.aspx?id={get_gdriveid(link)}").json()["link"]
    except:
        return f"{Config.DIRECT_INDEX}/direct.aspx?id={get_gdriveid(link)}"

def convert_time(seconds):
    mseconds = seconds * 1000
    periods = [('d', 86400000), ('h', 3600000), ('m', 60000), ('s', 1000), ('ms', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if mseconds >= period_seconds:
            period_value, mseconds = divmod(mseconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    if result == '':
        return '0ms'
    return result
