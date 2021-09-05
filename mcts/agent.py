import abc
import random
from typing import Any
from mcts import environment
from mcts import mcts


class Agent:
    """An entity that picks an action among possible states."""

    @abc.abstractmethod
    def act(self, state: environment.State) -> Any:
        raise NotImplementedError()


class RandomAgent(Agent):
    """An agent that picks an action at random."""

    def act(self, state: environment.State) -> Any:
        return random.choice(state.actions())


class HumanAgent(Agent):
    """An agent that allows a human to play through the console input."""

    def act(self, state: environment.State) -> Any:
        print(state)
        return eval(input('Enter your move: '))


class MCTSAgent(Agent):
    """Agent wrapping MCTS."""
    def __init__(self, evaluation_fn):
        self.search = mcts.MCTS(evaluation_fn=evaluation_fn)

    def act(self, state: environment.State) -> Any:
        return self.search.search(state)
