from pydantic import BaseModel
from datetime import datetime

from domain.entities.messages import Chat, Message



class CreateChatRequestSchema(BaseModel):
    title: str



class CreateChatResponseSchema(BaseModel):
    uid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(
            uid=chat.uid,
            title=chat.title.as_generic_type(),
        )


class MessageDetailSchema(BaseModel):
    uid: str
    text: str
    created_at: datetime

class ChatDetailSchema(BaseModel):
    uid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(
            uid=chat.uid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at
        )

class CreateMessageShema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    text: str
    uid: str

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(text=message.text.as_generic_type(), uid=message.uid)