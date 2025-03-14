from dataclasses import dataclass

from domain.exceptions.base import ApplicationException



@dataclass(eq=False)
class LogicExceptions(ApplicationException):
    @property
    def message(self):
        return f'Ann error occurred while processing request'