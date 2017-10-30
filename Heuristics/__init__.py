import logging
corners = {(0, 0), (0, 1), (1, 0), (6, 0), (7, 0), (7, 1), (0, 6), (0, 7), (1, 7), (7, 6), (7, 7), (6, 7)}


class Heuristic:

    def __init__(self):
        pass

    def H(self, state, turn, game):
        return 1


class OthelloHeuristic(Heuristic):

    def H(self, state, turn, game):
        h1 = self.H1(state, turn)
        h2 = self.H2(state, turn, game)
        h3 = self.H3(state, turn)
        # avg = (h1*0.3 + h2*0.3 + h3*0.4) / 3
        avg = (h1 * 0.42 + h3 * 0.58) / 2
        logging.debug("H: avg = {}".format(avg))
        return avg

    # Coin Parity
    def H1(self, state, turn):
        my_discs, enemy_discs = self.count_discs(state, turn)
        return 100 * (enemy_discs - my_discs) / (enemy_discs + my_discs)

    # Mobility
    def H2(self, state, turn, game):
        my_moves = len(game.neighbors(turn, state))
        enemy_moves = len(game.neighbors(self.get_enemy_color(turn), state))
        if (my_moves + enemy_moves) != 0:
            mobility_heuristic_value = 100 * (enemy_moves - my_moves) / (enemy_moves + my_moves)
        else:
            mobility_heuristic_value = 0
        return mobility_heuristic_value

    # Corners Captured
    def H3(self, state, turn):
        my_corner_discs, enemy_corner_discs = self.count_corner_discs(state, turn)
        if (enemy_corner_discs + my_corner_discs) != 0:
            corner_heuristic_value = 100 * (enemy_corner_discs - my_corner_discs) / (enemy_corner_discs + my_corner_discs)
        else:
            corner_heuristic_value = 0
        return corner_heuristic_value

    def Hl(self, game, state, l, turn):
        logging.debug("Hl: recursive call, level = {}; turn = {}".format(l, turn))
        if l == 0:
            return self.H(state, turn, game)
        if turn == 'w':
            next_turn = 'k'
            return max([self.Hl(game, x, int(l) - 1, next_turn) for x in game.neighbors(turn, state)])
        else:
            next_turn = 'w'
            return min([self.Hl(game, x, int(l) - 1, next_turn) for x in game.neighbors(turn, state)])

    @staticmethod
    def count_discs(state, turn):
        count_my_discs= 0
        count_enemy_discs=0
        for i in range(8):
            for j in range(8):
                if state.representation.get_disc(i, j) == turn:
                    count_my_discs += 1
                elif state.representation.get_disc(i, j) == '-':
                    continue
                else:
                    count_enemy_discs += 1
        return count_my_discs, count_enemy_discs

    @staticmethod
    def get_enemy_color(my_color):
        if my_color == 'k':
            return 'w'
        else:
            return 'k'

    @staticmethod
    def count_corner_discs(state, turn):
        count_my_discs = 0
        count_enemy_discs = 0
        for item in corners:
            if state.representation.get_disc(item[0], item[1]) == turn:
                count_my_discs += 1
            elif state.representation.get_disc(item[0], item[1]) == "-":
                continue
            else:
                count_enemy_discs += 1
        return count_my_discs, count_enemy_discs



