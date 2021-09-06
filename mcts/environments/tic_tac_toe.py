import random
from typing import Optional, Tuple
from mcts import environment


class TicTacToeState(environment.State):
    """A state in the game of tic-tac-toe."""

    HEADER = 'player 1: X\nplayer 2: O'
    SEPARATOR = '\n-------\n'
    VISUALIZATION = {
        None: ' ',
        1: 'X',
        2: 'O',
    }

    def __init__(self, player_turn: int, board: Tuple[Tuple[int]], winner: Optional[int] = None):
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
        empties = [
            (row, col)
            for row in range(3)
            for col in range(3)
            if self.board[row][col] is None
        ]
        return empties

    def step(self, action: Tuple[int, int]) -> 'TicTacToeState':
        """Return a new state resulting of applying the given action."""
        new = TicTacToeState(
            player_turn=self.player_turn,
            board=self.board,
            winner=self.winner,
        )
        new._step(action)
        return new

    def _step(self, action: Tuple[int, int]) -> None:
        """Apply the given action in place."""
        row, col = action
        rows = list(self.board)
        cells = list(rows[row])
        cells[col] = self.player_turn
        cells = tuple(cells)
        rows[row] = cells
        self.board = tuple(rows)
        if self.check_victory(last_move=action):
            self.winner = self.player_turn
        self.player_turn = self.player_turn % 2 + 1

    def check_victory(self, last_move: Tuple[int, int]) -> bool:
        """Check whether this is a winning position, given the last move."""
        player = self.player_turn
        row, col = last_move
        column_win = all(self.board[i][col] == player for i in range(3))
        row_win = all(self.board[row][i] == player for i in range(3))
        first_diag_win = all(self.board[i][i] == player for i in range(3))
        second_diag_win = all(self.board[i][2 - i] == player for i in range(3))
        return any([column_win, row_win, first_diag_win, second_diag_win])

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.board)
        return self._hash

    def __eq__(self, other):
        return self.board == other.board

    def __str__(self):
        """String representation of this board."""
        player_turn = 'player %s\'s turn' % self.player_turn
        board = (
        """
        |%s|%s|%s|
        |%s|%s|%s|
        |%s|%s|%s|
        """ % tuple(self.VISUALIZATION[val]
                    for row in self.board[::-1]
                    for val in row))
        # for row_idx in range(self.board_height - 1, -1, -1):
        #     row = [self.get_slot(col_idx, row_idx) for col_idx, column in enumerate(self.board)]
        #     board += ''.join([self.VISUALIZATION[val] for val in row]) + '\n'
        return self.SEPARATOR.join([self.HEADER, player_turn, board])


class TicTacToe(environment.Environment):
    """Tic Tac Toe game."""

    def initialize(self):
        return TicTacToeState(
            player_turn=random.randint(1, 2),
            board=((None, None, None),
                   (None, None, None),
                   (None, None, None)),
            winner=None,
        )
