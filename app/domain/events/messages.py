from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceiveEvent(BaseEvent):
    message_text: str
    message_uid: str
    chat_uid: str