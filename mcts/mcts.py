import random
import numpy as np


class MCTS:

    def __init__(self, evaluation_fn, num_rollouts=10000):
        self.counters = {}
        self.evals = {}
        self.evaluation_fn = evaluation_fn
        self.num_rollouts = num_rollouts

    def search(self, state):
        actions = state.actions()
        for i in range(self.num_rollouts):
            action = random.choice(actions)
            next_state = state.step(action)
            states = self.rollout(next_state)
            evaluation = self.evaluation_fn(states[-1])
            self.update(states, evaluation)

        possible_states = [state.step(a) for a in actions]
        estimated_values = [self.estimate(s) for s in possible_states]
        argmax = np.argmax(estimated_values)
        return actions[argmax]

    def rollout(self, state):
        states = [state]
        while not states[-1].is_final:
            actions = states[-1].actions()
            action = random.choice(actions)
            states.append(states[-1].step(action))
        return states

    def update(self, states, evaluation):
        for s in states:
            self.counters[s] = self.counters.get(s, 0) + 1
            self.evals[s] = self.counters.get(s, 0) + evaluation

    def estimate(self, state):
        if state in self.counters:
            return self.evals[state] / self.counters[state]
        return float('-inf')
