from pytest import fixture
import faker

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.init import init_mediator
from logic.mediator import Mediator


@fixture(scope='function')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()

@fixture(scope='function')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    
    return mediator

SHORT_TEXT = 15
LONG_TEXT = 400

@fixture
def get_fake_engine():
    yield faker.Faker() 

@fixture
def get_low_sentence(get_fake_engine):
    return get_fake_engine.sentence()

@fixture
def get_hight_sentenct(get_fake_engine):
    return get_fake_engine.sentence(nb_words=LONG_TEXT)

@fixture
def get_short_title(get_fake_engine):
    return get_fake_engine.text(max_nb_chars=SHORT_TEXT)

@fixture
def get_long_title(get_fake_engine):
    return get_fake_engine.text(max_nb_chars=LONG_TEXT)