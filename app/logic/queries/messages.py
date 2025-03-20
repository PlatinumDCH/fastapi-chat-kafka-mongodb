from dataclasses import dataclass
from typing import Generic, Iterable

from domain.entities.messages import Chat, Message
from infra.repositories.filters.messsages import GetMessagesFilters
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler




@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_uid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_uid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler):
    chats_repository: BaseChatsRepository
    messages_reposiroty: BaseMessagesRepository #TODO: забрать отдтельно    

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_uid(uid=query.chat_uid)

        if not chat:
            raise ChatNotFoundException(chat_uid=query.chat_uid)
        
        return chat

@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.messages_repository.get_messages(
            chat_uid=query.chat_uid,
            filters=query.filters
        )