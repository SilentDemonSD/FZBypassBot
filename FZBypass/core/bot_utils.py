from pyrogram.filters import create
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

def convert_time(seconds):
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result
