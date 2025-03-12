from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=True)
class TextTooLongExceptions(ApplicationException):
    text: str

    @property
    def message(self):
        return f'To long text messages {self.text[:255]}...'