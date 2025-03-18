from dataclasses import dataclass
from typing import Generic

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler




@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_uid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QR, QT]):
    chats_repository: BaseChatsRepository
    messages_reposiroty: BaseMessagesRepository #TODO: забрать отдтельно    

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_uid(uid=query.chat_uid)

        if not chat:
            raise ChatNotFoundException(chat_uid=query.chat_uid)
        
        return chat