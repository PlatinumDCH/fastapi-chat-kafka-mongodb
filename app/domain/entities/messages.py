from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.events.messages import NewChatCreated, NewMessageReceiveEvent
from domain.values.messages import Text, Title



@dataclass(eq=False)
class Message(BaseEntity):
    text: Text

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_events(NewChatCreated(chat_uid=new_chat.uid, chat_title=new_chat.title.as_generic_type()))

        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_events(NewMessageReceiveEvent(
            message_text=message.text.as_generic_type(),
            chat_uid=self.uid,
            message_uid=message.uid
        ))
    


