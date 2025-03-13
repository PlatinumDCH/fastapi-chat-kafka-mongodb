from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from uuid import uuid4

from domain.events.base import BaseEvent



@dataclass
class BaseEntity(ABC):
    uid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    _events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True)
    
    def __hash__(self):
        return hash(self.uid)
    
    def __eq__(self, __value: 'BaseEntity'):
        return self.uid == __value.uid

    def register_events(self, event: BaseEvent)->None:
        self._events.append(event)

    def pull_events(self)->list[BaseEvent]:
        regidtered_events = copy(self._events)

        self._events.clear()
        return regidtered_events
    