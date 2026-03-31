from abc import ABC, abstractmethod

class Action(ABC):
    _next_id = 1

    def __init__(self):
        self.id = Action._next_id
        Action._next_id += 1

    def describe(self):
        return ""

    def __repr__(self):
        description = self.describe()
        return f"<{self.__class__.__name__}#{self.id} {description}>"

    @abstractmethod
    def validate(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError