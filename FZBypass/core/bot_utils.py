from pyrogram.filters import create
from pyrogram.enums import MessageEntityType
from re import search, match
from requests import get as rget
from urllib.parse import urlparse, parse_qs
from FZBypass import Config

async def auth_topic(_, __, message):
    for chat in Config.AUTH_CHATS:
        if ':' in chat:
            chat_id, topic_id = chat.split(':')
            if (int(chat_id) == message.chat.id and message.is_topic_message
                and message.topics and message.topics.id == int(topic_id)):
                return True
        elif int(chat) == message.chat.id:
            return True
    return False

AuthChatsTopics = create(auth_topic)

async def auto_bypass(_, c, message):
    if Config.AUTO_BYPASS and message.entities and not match(r'^\/(bash|shell)($| )', message.text) and any(enty.type in [MessageEntityType.TEXT_LINK, MessageEntityType.URL] for enty in message.entities):
        return True
    elif not Config.AUTO_BYPASS and (txt := message.text) and match(fr'^\/(bypass|bp)(@{(await c.get_me()).username})?($| )', txt) and not match(r'^\/(bash|shell)($| )', txt):
        return True
    return False

BypassFilter = create(auto_bypass)

def get_gdriveid(link):
    if "folders" in link or "file" in link:
        res = search(r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)", link)
        return res.group(3)
    parsed = urlparse(link)
    return parse_qs(parsed.query)['id'][0]

def get_dl(link, direct_mode=False):
    if direct_mode and not Config.DIRECT_INDEX:
        return "No Direct Index Added !"
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
