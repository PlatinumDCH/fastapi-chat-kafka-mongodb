from dataclasses import dataclass

from logic.exceptions.base import LogicExceptions



@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicExceptions):
    title: str

    @property
    def message(self):
        return f'A chat with this name arleady exists: {self.title}'