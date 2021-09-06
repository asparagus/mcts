import random
import time
import numpy as np


class MCTS:
    """Monte Carlo Tree Search."""

    def __init__(self, evaluation_fn, timeout_ms=1000):
        self.counters = {}
        self.evals = {}
        self.evaluation_fn = evaluation_fn
        self.timeout_ms = timeout_ms

    def search(self, state):
        start_time = time.monotonic()
        steps = 0
        while (time.monotonic() - start_time) * 1000 < self.timeout_ms:
            chain = self.select(state)
            final_state = self.rollout(chain[-1])
            evaluation = self.evaluation_fn(final_state)
            self.update(chain, evaluation)
            steps += 1

        actions = state.actions()
        possible_states = [state.step(a) for a in actions]
        estimated_values = [self.estimate(s) for s in possible_states]
        argmax = np.argmax(estimated_values)
        return actions[argmax]

    def select(self, state):
        chain = [state]
        current_state = state
        while (current_state in self.counters
               and not current_state.is_final):
            actions = current_state.actions()
            action = random.choice(actions)
            current_state = current_state.step(action)
            chain.append(current_state)
        return chain

    def rollout(self, state):
        current_state = state
        while not current_state.is_final:
            actions = current_state.actions()
            action = random.choice(actions)
            current_state = current_state.step(action)
        return current_state

    def update(self, states, evaluation):
        for s in states:
            self.counters[s] = self.counters.get(s, 0) + 1
            self.evals[s] = self.evals.get(s, 0) + evaluation

    def estimate(self, state):
        if state in self.counters:
            return self.evals[state] / self.counters[state]
        return float('-inf')
