import random
from typing import Optional, Tuple
from mcts import environment


class ConnectFourState(environment.State):
    """A state in Connect four."""

    HEADER = 'player 1: X\nplayer 2: O'
    SEPARATOR = '\n-------\n'
    VISUALIZATION = {
        None: '.',
        1: 'X',
        2: 'O',
    }

    def __init__(self, player_turn: int, board: Tuple[Tuple[int]], board_height: int, winner: Optional[int] = None):
        """Initialize a Connect Four board state."""
        self.player_turn = player_turn
        self.board = board
        self.board_height = board_height
        self.winner = winner
        self._hash = None

    def actions(self):
        """Valid actions are any column where there's an empty slot."""
        if self.winner:
            return []
        # Zeros are empty slots
        open_indices = [
            col_idx for col_idx, col in enumerate(self.board)
            if len(col) < self.board_height - 1
        ]
        return open_indices

    def step(self, action: int) -> 'ConnectFourState':
        """Return a new state resulting of applying the given action."""
        new = ConnectFourState(
            player_turn=self.player_turn,
            board=self.board,
            board_height=self.board_height,
            winner=self.winner,
        )
        new._step(action)
        return new

    def _step(self, action: int) -> None:
        """Apply the given action in place."""
        column = action
        self._place_chip(column, self.player_turn)
        if self.check_victory(last_move=column):
            self.winner = self.player_turn
        self.player_turn = self.player_turn % 2 + 1

    def _place_chip(self, column: int, player: int) -> None:
        columns = list(self.board)
        columns[column] += (self.player_turn,)
        self.board = tuple(columns)

    def get_slot(self, column, row):
        if 0 <= column < len(self.board):
            if 0 <= row < len(self.board[column]):
                return self.board[column][row]
        return None

    def check_victory(self, last_move: int) -> bool:
        """Check whether this is a winning position, given the last move."""
        board = self.board
        c = last_move
        r = len(board[c]) - 1
        player = self.get_slot(c, r)

        # Vertical
        vertical_counter = 1
        for i in range(1, 4):
            current = self.get_slot(c, r - i)
            if current == player:
                vertical_counter += 1
            else:
                break
        if vertical_counter >= 4:
            return True

        # Horizontal
        horizontal_counter = 1
        for i in range(1, 4):
            current = self.get_slot(c + i, r)
            if current == player:
                horizontal_counter += 1
            else:
                break
        for i in range(1, 4):
            current = self.get_slot(c - i, r)
            if current == player:
                horizontal_counter += 1
            else:
                break
        if horizontal_counter >= 4:
            return True

        south_diagonal_counter = 1
        for i in range(1, 4):
            current = self.get_slot(c + i, r + i)
            if current == player:
                south_diagonal_counter += 1
            else:
                break
        for i in range(1, 4):
            current = self.get_slot(c - i, r - i)
            if current == player:
                south_diagonal_counter += 1
            else:
                break
        if south_diagonal_counter >= 4:
            return True

        north_diagonal_counter = 1
        for i in range(1, 4):
            current = self.get_slot(c + i, r - i)
            if current == player:
                north_diagonal_counter += 1
            else:
                break
        for i in range(1, 4):
            current = self.get_slot(c - i, r + i)
            if current == player:
                north_diagonal_counter += 1
            else:
                break
        if north_diagonal_counter >= 4:
            return True
        return False

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.board)
        return self._hash

    def __eq__(self, other):
        return self.board == other.board

    def __str__(self):
        """String representation of this board."""
        player_turn = 'player %s\'s turn' % self.player_turn
        board = ''
        for row_idx in range(self.board_height - 1, -1, -1):
            row = [self.get_slot(col_idx, row_idx) for col_idx, column in enumerate(self.board)]
            board += ''.join([self.VISUALIZATION[val] for val in row]) + '\n'
        return self.SEPARATOR.join([self.HEADER, player_turn, board])


class ConnectFour(environment.Environment):
    """Connect four game."""

    def __init__(self, board_width: int, board_height: int):
        self.board_width = board_width
        self.board_height = board_height

    def initialize(self):
        return ConnectFourState(
            player_turn=random.randint(1, 2),
            board=tuple([(),] * self.board_width),
            board_height=self.board_height,
            winner=None,
        )
