from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.values.messages import Text, Title


@dataclass
class Message:
    text: Text
    uid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Message):
            return NotImplemented
        return self.uid == other.uid

@dataclass
class Chat:
    title: Title
    uid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chat):
            return NotImplemented
        return self.uid == other.uid
    
    def app_message(self, message: Message):
        self.messages.add(message)

