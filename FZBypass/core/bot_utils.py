from pyrogram.filters import create

async def auth_topic(_, message):
    for chat in Config.AUTH_CHATS:
        if ':' in chat:
            chat_id, topic_id = chat.split(':')
            if message.chat.id == chat_id and (is_forum := message.reply_to_message) and not hasattr(is_forum, text) and topic_id == is_forum.id:
            return True
        elif message.chat.id == chat:
            return True
    return False

chat_and_topics = create(auth_topic)