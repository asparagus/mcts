import copy
import random
from typing import Optional

import numpy as np

from mcts import environment


class ConnectFourState(environment.State):
    """A state in Connect four."""

    HEADER = 'player 1: X\nplayer 2: O'
    SEPARATOR = '\n-------\n'
    VISUALIZATION = {
        0: '.',
        1: 'X',
        2: 'O',
    }

    def __init__(self, player_turn: int, board: np.ndarray, winner: Optional[int] = None):
        """Initialize a Connect Four board state."""
        self.player_turn = player_turn
        self.board = board
        self.winner = winner
        self._hash = None

    def actions(self):
        """Valid actions are any column where there's an empty slot."""
        if self.winner:
            return []
        # Zeros are empty slots
        open_indices = np.flatnonzero(np.min(self.board, axis=1) == 0)
        return list(open_indices)

    def step(self, action: int) -> 'ConnectFourState':
        """Return a new state resulting of applying the given action."""
        new = copy.deepcopy(self)
        new._step(action)
        return new

    def _step(self, action: int) -> None:
        """Apply the given action in place."""
        col = action
        row = np.argmin(self.board[col])
        self.board[col, row] = self.player_turn 
        if self.check_victory(last_move=(col, row)):
            self.winner = self.player_turn
        self.player_turn = self.player_turn % 2 + 1

    def check_victory(self, last_move: (int, int)) -> bool:
        """Check whether this is a winning position, given the last move."""
        board = self.board
        c, r = last_move
        player = board[c, r]
        # Check vertical
        south_diagonal_counter = 0
        north_diagonal_counter = 0
        vertical_counter = 0
        horizontal_counter = 0
        for i in range(-3, 4):
            if 0 <= c + i < len(board):
                horizontal_counter = horizontal_counter + 1 if board[c + i, r] == player else 0
                if 0 <= r + i < len(board[0]):
                    south_diagonal_counter = south_diagonal_counter + 1 if board[c + i, r + i] == player else 0
                if 0 <= r - i < len(board[0]):
                    north_diagonal_counter = north_diagonal_counter + 1 if board[c + i, r - i] == player else 0
            if 0 <= r + i < len(board[0]):
                vertical_counter = vertical_counter + 1 if board[c, r + i] == player else 0
            if max(horizontal_counter, vertical_counter,
                   south_diagonal_counter, north_diagonal_counter) == 4:
                return True
        return False

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(str(self))
        return self._hash

    def __eq__(self, other):
        if self.player_turn != other.player_turn:
            return False
        if self.winner != other.winner:
            return False
        return np.array_equal(self.board, other.board)

    def __str__(self):
        """String representation of this board."""
        player_turn = 'player %s\'s turn' % self.player_turn
        board = ''
        for row_idx in range(self.board.shape[1] - 1, -1, -1):
            row = self.board[:, row_idx]
            board += ''.join([self.VISUALIZATION[val] for val in row]) + '\n'
        return self.SEPARATOR.join([self.HEADER, player_turn, board])


class ConnectFour(environment.Environment):
    """Connect four game."""

    def __init__(self, board_width: int, board_height: int):
        self.shape = (board_width, board_height)

    def initialize(self):
        return ConnectFourState(
            player_turn=random.randint(1, 2),
            board=np.zeros(shape=self.shape, dtype=np.float32),
            winner=None,
        )
