import random
import time
import numpy as np


class MCTS:
    """Monte Carlo Tree Search."""

    def __init__(self, evaluation_fn, exploration_constant=0, timeout_ms=10):
        """Initialize the search with a given evaluation and timeout."""
        self.counters = {}
        self.evals = {}
        self.evaluation_fn = evaluation_fn
        self.exploration_constant = exploration_constant
        self.timeout_ms = timeout_ms

    def search(self, state):
        """Perform the search."""
        start_time = time.monotonic()
        while (time.monotonic() - start_time) * 1000 < self.timeout_ms:
            chain = self.select(state)
            final_state = self.rollout(chain[-1])
            evaluation = self.evaluation_fn(final_state)
            self.update(chain, evaluation)

        actions = state.actions()
        possible_states = [state.step(a) for a in actions]
        estimated_values = [self.estimate(s) for s in possible_states]
        # Pick greedily
        return actions[np.argmax(estimated_values)]

    def select(self, state):
        """Select a state to rollout from."""
        chain = [state]
        current_state = state
        while (current_state in self.counters
               and not current_state.is_final):
            # Selection - ucb argmax
            current_state = self.ucb(current_state)
            chain.append(current_state)
        return chain

    def rollout(self, state):
        """Play from a state to completion."""
        current_state = state
        while not current_state.is_final:
            actions = current_state.actions()
            # Light rollout - uniform distribution
            action = random.choice(actions)
            current_state = current_state.step(action)
        return current_state

    def update(self, states, evaluation):
        """Update state estimations."""
        for s in states:
            self.counters[s] = self.counters.get(s, 0) + 1
            self.evals[s] = self.evals.get(s, 0) + evaluation

    def estimate(self, state):
        """Compute a state estimation."""
        if state in self.counters:
            return self.evals[state] / self.counters[state]
        return float('-inf')

    def ucb(self, state):
        """Upper confidence bound child selection."""
        actions = state.actions()
        possible_states = [state.step(a) for a in actions]
        estimated_values = [self.estimate(s) for s in possible_states]
        exploration_values = [self.exploration_constant * self.exploration(state, s)
                              for s in possible_states]
        combined_values = [v + e for v, e in zip(estimated_values, exploration_values)]
        return possible_states[np.argmax(combined_values)]

    def exploration(self, parent_state, state):
        """Exploration value for ucb."""
        if state not in self.counters or parent_state not in self.counters:
            return float('inf')
        return np.sqrt(
            2 * np.log(self.counters[parent_state]) /
            self.counters[state]
        )
