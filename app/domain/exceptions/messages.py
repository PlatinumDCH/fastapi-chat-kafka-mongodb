from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"To long text messages {self.text[:255]}..."


@dataclass(eq=False)
class EmptyTextException(ApplicationException):

    @property
    def message(self):
        return "Text cant be empty"