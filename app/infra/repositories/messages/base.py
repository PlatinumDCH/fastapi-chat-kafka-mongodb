from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import Chat, Message
from infra.repositories.filters.messsages import GetMessagesFilters


@dataclass
class BaseChatsRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def get_chat_by_uid(self, uid: str) -> Chat|None:
        ...
    
    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...



@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message) -> None:
        ...
    
    @abstractmethod
    async def get_messages(self, chat_uid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        ...