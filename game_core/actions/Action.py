from abc import ABC, abstractmethod

class Action(ABC):

    @abstractmethod
    def validate(self, game):
        raise NotImplementedError

    @abstractmethod
    def execute(self, game):
        raise NotImplementedError