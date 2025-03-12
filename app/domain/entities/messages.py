from dataclasses import dataclass

from domain.values.messages import Text

@dataclass
class Message:
    uid: str
    test: Text