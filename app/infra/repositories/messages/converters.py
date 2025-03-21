from domain.entities.messages import Chat, Message


def convert_message_to_document(message: Message) -> dict:
    return {
        'uid': message.uid,
        'text': message.text.as_generic_type(),
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        'uid': chat.uid,
        'title': chat.title.as_generic_type(),
        'created_at': chat.created_at,
        'messages': [convert_message_to_document(message) for message in chat.messages],
    }