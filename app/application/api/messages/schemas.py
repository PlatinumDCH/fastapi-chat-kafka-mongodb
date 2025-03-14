from pydantic import BaseModel

from domain.entities.messages import Chat


class CreateChatRequestSchema(BaseModel):
    title: str

class CreateChatResponseSchema(BaseModel):
    uid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatRequestSchema':
        return CreateChatResponseSchema(
            uid=chat.uid,
            title=chat.title.as_generic_type(),
        )