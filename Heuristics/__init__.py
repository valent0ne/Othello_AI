corners = {
           (0, 0),
           (0, 1),
           (1, 0),
           (6, 0),
           (7, 0),
           (7, 1),
           (0, 6),
           (0, 7),
           (1, 7),
           (7, 6),
           (7, 7),
           (6, 7)
           }

class Heuristic:

    def __init__(self):
        pass

    def H(self, state, turn, game):
        return 1


class OthelloHeuristic(Heuristic):

    # This method return the weighted average of the value obtained by the application of the three heuristic
    def Average_Of_Heuristics(self, state, turn, game):
        h1 = self.Coin_Parity(state, turn)
        # h2 = self.Mobility(state, turn, game)
        h3 = self.Corners_Captured(state, turn)
        # avg = (h1*0.3 + h2*0.2 + h3*0.5) / 3
        avg = (h1*0.4 + h3*0.6) / 2
        return avg

    # Coin Parity: this heuristic is based on the number of disc white and black are on the board
    def Coin_Parity(self, state, turn):
        my_discs, enemy_discs = self.count_discs(state, turn)
        return 100 * (enemy_discs - my_discs) / (enemy_discs + my_discs)

    # Mobility: this heuristic is based on the number of possible moves that the player can do
    def Mobility(self, state, turn, game):
        my_moves = len(game.neighbors(turn, state))
        enemy_moves = len(game.neighbors(self.get_enemy_color(turn), state))
        if (my_moves + enemy_moves) != 0:
            mobility_heuristic_value = 100 * (enemy_moves - my_moves) / (enemy_moves + my_moves)
        else:
            mobility_heuristic_value = 0
        return mobility_heuristic_value

    # Corners Captured: this heuristic is based on the occupation of the corners
    def Corners_Captured(self, state, turn):
        my_corner_discs, enemy_corner_discs = self.count_corner_discs(state, turn)
        if (enemy_corner_discs + my_corner_discs) != 0:
            corner_heuristic_value = 100 * (enemy_corner_discs - my_corner_discs) / (enemy_corner_discs + my_corner_discs)
        else:
            corner_heuristic_value = 0
        return corner_heuristic_value

    # This is the function minMax: it takes the game instance, a current state, the number of level to explore
    # and the current turn
    def MinMax(self, game, state, l, turn):
        # if the level is equal 0
        if l == 0:
            # return the weighted average of the three heuristic computed
            return self.H(state, turn, game)
        # if the level>0 and the current turn is of white player
        if turn == 'w':
            # then, next turn is of black player
            next_turn = 'k'
            # calculate recoursevely what is the max value that we sould obtain
            return max([self.MinMax(game, x, int(l) - 1, next_turn) for x in game.neighbors(turn, state)])
        # otherwise the current turn is of black player
        else:
            # next turn is of white player
            next_turn = 'w'
            # calculate recoursevely what is the min value that we sould obtain
            return min([self.MinMax(game, x, int(l) - 1, next_turn) for x in game.neighbors(turn, state)])

    # this is a static method that count the number of discs belong respectively to the current player
    # and the enemy player
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


    #this is  a static method that return the enemy's discs color
    @staticmethod
    def get_enemy_color(my_color):
        if my_color == 'k':
            return 'w'
        else:
            return 'k'

    # this is a stati method that calculate the number of the current player's and the enemy's discs in the corner
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



