import cProfile
from mcts.environments import connect_four
from mcts import agent
from mcts import environment
from mcts import mcts


class Tournament:
    def __init__(self, game, competitor_a, competitor_b):
        self.game = game
        self.competitor_a = competitor_a
        self.competitor_b = competitor_b

    def round(self):
        state = self.game.initialize()
        while not state.is_final:
            player = self.competitor_a if state.player_turn == 1 else self.competitor_b
            action = player.act(state)
            state = state.step(action)
        return int(state.winner == 1), int(state.winner == 2)

    def run(self, n):
        sum_results_a = 0.0
        sum_results_b = 0.0
        for i in range(n):
            win_a, win_b = self.round()
            print('%i: %s, %s' % (i, win_a, win_b))
            sum_results_a += win_a
            sum_results_b += win_b
        return sum_results_a / n, sum_results_b / n


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Script for running a competition between agents.')
    parser.add_argument(
        '--n', type=int, default=100, help='Number of iterations to run.')
    parser.add_argument('a', help='Competitor, one of "human", "random", "mcts"')
    parser.add_argument('b', help='Competitor, one of "human", "random", "mcts"')
    args = parser.parse_args()
    print(args)

    def player_evaluation_fn(player: int):
        def evaluation_fn(state: environment.State):
            if state.winner is None:
                return 0
            return 1 if state.winner == player else -1
        return evaluation_fn

    agents = {
        'human': lambda player: agent.HumanAgent(),
        'random': lambda player: agent.RandomAgent(),
        'mcts': lambda player: agent.MCTSAgent(player_evaluation_fn(player)),
    }
    result_sum = 0
    game = connect_four.ConnectFour(board_width=8, board_height=7)
    tournament = Tournament(
        game=game,
        competitor_a=agents[args.a](1),
        competitor_b=agents[args.b](2),
    )
    cProfile.runctx("tournament.run(args.n)", globals(), locals())
    # results_a, results_b = tournament.run(args.n)
    # print('Tournament results: %s / %s' % (results_a, results_b))
