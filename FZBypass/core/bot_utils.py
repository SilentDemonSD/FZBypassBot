from pyrogram.filters import create
from FZBypass import Config

async def auth_topic(_, __, message):
    for chat in Config.AUTH_CHATS:
        if ':' in chat:
            chat_id, topic_id = chat.split(':')
            if (int(chat_id) == message.chat.id 
                and (is_forum := message.reply_to_message) 
                and not hasattr(is_forum, 'text') 
                and int(topic_id) == is_forum.id):
                return True
        elif int(chat) == message.chat.id:
            return True
    return False

chat_and_topics = create(auth_topic)