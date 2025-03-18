from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.values.messages import Title, Text
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException, ChatNotFoundException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chats_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)

        new_chat = Chat.create_chat(title=title)
        # TODO: считать ивенты 
        await self.chats_repository.add_chat(new_chat)

        return new_chat

@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_uid: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Chat]):
    message_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await  self.chats_repository.get_chat_by_uid(uid=command.chat_uid)

        if not chat:
            raise ChatNotFoundException(chat_uid=command.chat_uid)
    

        message = Message(text=Text(value=command.text))
        chat.add_message(message)
        await self.message_repository.add_message(chat_uid=command.chat_uid, message=message)

        return message