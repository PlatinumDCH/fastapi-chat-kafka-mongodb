import pytest
import faker
from datetime import datetime

from domain.values.messages import Text, Title
from domain.exceptions.messages import TitleTooLongException
from domain.entities.messages import Chat, Message


SHORT_TEXT = 15
LONG_TEXT = 400

@pytest.fixture
def get_fake_engine():
    yield faker.Faker() 

@pytest.fixture
def get_low_sentence(get_fake_engine):
    return get_fake_engine.sentence()

@pytest.fixture
def get_hight_sentenct(get_fake_engine):
    return get_fake_engine.sentence(nb_words=LONG_TEXT)

@pytest.fixture
def get_short_title(get_fake_engine):
    return get_fake_engine.text(max_nb_chars=SHORT_TEXT)

@pytest.fixture
def get_long_title(get_fake_engine):
    return get_fake_engine.text(max_nb_chars=LONG_TEXT)


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
    
def test_add_chat_to_message(get_short_title):
    text = Text(get_low_sentence)
    message = Message(text=text)

    title = Title(get_short_title)
    chat = Chat(title=title)

    chat.app_message(message)

    assert message in chat.messages
