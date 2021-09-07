import pytest
from mcts.environments import connect_four


@pytest.fixture
def env():
    return connect_four.ConnectFour(board_width=7, board_height=6)


def play_moves(state, player_1_moves, player_2_moves):
    for move_1, move_2 in zip(player_1_moves, player_2_moves):
        state = state.step(move_1)
        assert not state.is_final
        state = state.step(move_2)
        assert not state.is_final
    return state


def test_vertical_win(env):
    state = env.initialize()
    state = play_moves(state, [1, 1, 1], [2, 2, 2])
    state = state.step(1)
    print(state)
    assert state.is_final


def test_horizontal_win(env):
    state = env.initialize()
    state = play_moves(state, [1, 2, 3], [5, 5, 5])
    state = state.step(4)
    print(state)
    assert state.is_final


def test_north_diagonal_win(env):
    state = env.initialize()
    state = play_moves(state, [1, 2, 3, 3, 3], [2, 4, 4, 4, 5])
    state = state.step(4)
    print(state)
    assert state.is_final


def test_south_diagonal_win(env):
    state = env.initialize()
    state = play_moves(state, [4, 3, 2, 2, 2], [3, 1, 1, 1, 5])
    state = state.step(1)
    print(state)
    assert state.is_final
