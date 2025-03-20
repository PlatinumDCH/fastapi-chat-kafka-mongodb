from punq import Container

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageShema,
    ChatDetailSchema,
    GetMessageQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from application.api.messages.filters import GetMessagesFilters
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.messages import GetChatDetailQuery, GetMessagesQuery


router = APIRouter(tags=['Chat'])



@router.post(
        '/', 
        # response_model=CreateChatResponseSchema,
        status_code=status.HTTP_201_CREATED,
        description='Enpoint create new chat, if chat.title exists - return 400Error',
        responses={
            status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
            status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
        }
    )
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container)
    ) -> CreateChatResponseSchema:
    """ Create mew chat"""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat)

@router.post(
    '/{chat_uid}/messages',
    status_code=status.HTTP_201_CREATED,
    description='endpoint added new message in chat with ObjectID',
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageShema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_message_handler(
    chat_uid: str,
    schema: CreateMessageShema,
    contaier: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """ Added new message to chat"""
    mediator: Mediator = contaier.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(CreateMessageCommand(text=schema.text, chat_uid=chat_uid))
    except ApplicationException as exceptions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exceptions.message})

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    '/{chat_uid}/',
    status_code=status.HTTP_200_OK,
    description='Get info about chat and all messages in him',
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_chat_with_messages_handler(
    chat_uid: str,
    container: Container = Depends(init_container),
) -> ChatDetailSchema:
    """ Get ChatObject """
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_uid=chat_uid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message}
        )
    
    return ChatDetailSchema.from_entity(chat)

@router.get(
    '/{chat_uid}/messages',
    status_code=status.HTTP_200_OK,
    description='All send messages in chat',
    responses={
        status.HTTP_200_OK: {'model': GetMessageQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_messagrs_handler(
    chat_uid: str,
    filters: GetMessagesFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetMessageQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_uid=chat_uid, filters=filters.to_infra())
        )
        
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message}
        )
    
    return GetMessageQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages]
    )