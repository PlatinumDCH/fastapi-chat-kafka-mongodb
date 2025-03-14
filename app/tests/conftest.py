from pytest import fixture
import faker

from punq import Container

from infra.repositories.messages import BaseChatRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()

@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)

@fixture
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


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