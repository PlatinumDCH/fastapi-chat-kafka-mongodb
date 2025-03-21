from dataclasses import dataclass

from logic.exceptions.base import LogicExceptions



@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicExceptions):
    event_type: type

    @property
    def message(self):
        return f"Not found handlere for event :{self.event_type}"



@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicExceptions):
    command_type: type

    @property
    def message(self):
        return f"Not found handlere for command :{self.command_type}"
