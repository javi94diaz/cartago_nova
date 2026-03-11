from abc import ABC, abstractmethod

class Action(ABC):

    @abstractmethod
    def validate(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError