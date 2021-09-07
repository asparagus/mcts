import pytest
from mcts.environments import tic_tac_toe


@pytest.fixture
def env():
    return tic_tac_toe.TicTacToe()


def play_moves(state, player_1_moves, player_2_moves):
    for move_1, move_2 in zip(player_1_moves, player_2_moves):
        state = state.step(move_1)
        assert not state.is_final
        state = state.step(move_2)
        assert not state.is_final
    return state


def test_vertical_win(env):
    state = env.initialize()
    state = play_moves(state, [(0, 0), (1, 0)], [(2, 2), (1, 2)])
    state = state.step((2, 0))
    print(state)
    assert state.is_final


def test_horizontal_win(env):
    state = env.initialize()
    state = play_moves(state, [(0, 0), (0, 1)], [(2, 2), (1, 2)])
    state = state.step((0, 2))
    print(state)
    assert state.is_final



def test_north_diagonal_win(env):
    state = env.initialize()
    state = play_moves(state, [(0, 0), (1, 1)], [(0, 2), (1, 2)])
    state = state.step((2, 2))
    print(state)
    assert state.is_final


def test_south_diagonal_win(env):
    state = env.initialize()
    state = play_moves(state, [(2, 0), (1, 1)], [(2, 2), (2, 1)])
    state = state.step((0, 2))
    print(state)
    assert state.is_final
