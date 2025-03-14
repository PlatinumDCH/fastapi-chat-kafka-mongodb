import pytest
from datetime import datetime

from domain.events.messages import NewMessageReceiveEvent
from domain.values.messages import Text, Title
from domain.exceptions.messages import TitleTooLongException
from domain.entities.messages import Chat, Message



def test_create_message_success_short_text(get_low_sentence):
    text = Text(get_low_sentence)
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_success_long_text(get_hight_sentenct):
    text = Text(get_hight_sentenct)
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success_short_title(get_short_title):
    title = Title(get_short_title)
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_fail_long_title(get_long_title):
    with pytest.raises(TitleTooLongException):
        Title(get_long_title)
    

def test_add_chat_to_message(get_short_title, get_low_sentence):
    text = Text(get_low_sentence)
    message = Message(text=text)

    title = Title(get_short_title)
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages


def test_new_messag_event(get_low_sentence, get_short_title):
    text = Text(get_low_sentence)
    message = Message(text=text)

    title = Title(get_short_title)
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()


    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceiveEvent), new_event
    assert new_event.message_uid == message.uid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_uid == chat.uid
