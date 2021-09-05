import abc
from typing import List


class State(abc.ABC):

    @property
    def is_final(self) -> bool:
        return not self.actions()

    @abc.abstractmethod
    def actions(self) -> List:
        raise NotImplementedError()

    @abc.abstractmethod
    def step(self, action) -> 'State':
        raise NotImplementedError()


class Environment(abc.ABC):

    @abc.abstractmethod
    def initialize(self) -> State:
        raise NotImplementedError()
