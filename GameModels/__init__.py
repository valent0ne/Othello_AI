import numpy as np
import copy as cp
import logging


initial_board = [
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', 'k', 'w', '-', '-', '-'],
                 ['-', '-', '-', 'w', 'k', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-'],
                 ['-', '-', '-', '-', '-', '-', '-', '-']
                ]

# Class that define a game
class Game:

    def __init__(self, initial_state=None, heuristic=None):
        self.state = initial_state
        self.heuristic = heuristic

    def neighbors(self, state, turn):
        out = set([])
        return out

    def get_state(self):
        return self.state

    def solution(self, state):
        return True

# Class that describes the Othello rapresentation
class OthelloRepresentation:

    # Init: Copy the initial board specify at the begin of this file
    def __init__(self):
        self.board = np.copy(initial_board)

    # Given a coordinate return what there's in that cell
    def get_disc(self, a, b):
        return self.board[a][b]

    # Given a coordinate and a color, change the disc in that position
    def set_disc(self, a, b, disc):
        self.board[a][b] = disc

    # Verify if a cell is empty (return True) or there's a sic(return False)
    def is_empty(self, a, b):
        return self.board[a][b] == '-'

    # Static method that calculate, given a certain color, the color belong to the enemy
    @staticmethod
    def get_enemy_color(my_color):
        if my_color == 'k':
            return 'w'
        else:
            return 'k'


# Class that describes the Othell0's state
class OthelloState:

    # Every state has saved a rapresentation of that state and a heuristic value associate to this state
    def __init__(self, h):
        self.heuristic = h
        self.representation = OthelloRepresentation()
        
    # Method that verify if two states are equal on the representation
    def __eq__(self, other):
        return str(self.representation.board) == str(other.representation.board)

    # Method that verify if two states are not equal on the representation
    def __ne__(self, other):
        return str(self.representation.board) != str(other.representation.board)

    def __hash__(self):
        return hash(str(self.representation.board))

    # Given a coordinate return what there's in that cell in the current state
    def get_disc(self, a, b):
        return self.representation.get_disc(a, b)

    # Given a coordinate modify what there's in that cell in the current state
    def set_disc(self, a, b, disc):
        self.representation.set_disc(a, b, disc)
        
    # Given a coordinate verify if there's or not a disc
    def is_empty(self, a, b):
        return self.representation.is_empty(a, b)

    # Method that verify if the current state is the final state or not
    def is_final(self):
        # counter of the black discs
        num_black_discs = 0
        # counter of the white discs
        num_white_discs = 0
        # Start the exploration from the beginning of the board and than explore all the board
        for i in range(8):
            for j in range(8):
                # if in the cell (i,j) there's '-'
                if self.representation.get_disc(i, j) == "-":
                    # return None -->it's not a final state
                    return None
                # if ther's a black disc
                elif self.representation.get_disc(i, j) == 'k':
                    # add 1 to counter of black discs
                    num_black_discs += 1
                # otherwise there's a white disc
                else:
                    # add 1 to counter of white discs 
                    num_white_discs += 1
        # if black discs are grather than white discs
        if num_black_discs > num_white_discs:
            # the winner is black
            return "k"
        # if white discs are grather than black discs
        elif num_black_discs < num_white_discs:
            # the winner is white
            return "w"
        # otherwise the number of black disac are equal to the number of white discs
        else:
            return "e"

    # Method that calculate, given a coordinate and a color, which discs are affected by the move that put a disc 
    # in the position (a,b)
    def get_w_discs_change(self, a, b, my_color):
        total_affected_discs = set([])
        if self.representation.is_empty(a, b):

            set_change_row = set([])
            set_change_col = set([])
            set_change_fdiag = set([])
            set_change_sdiag = set([])

            row_prev, row_next = self.get_nearest_discs_row(a, b, my_color)
            col_up, col_bottom = self.get_nearest_discs_col(a, b, my_color)
            fdiag_up, fdiag_bottom = self.get_nearest_discs_first_diag(a, b, my_color)
            sdiag_up, sdiag_bottom = self.get_nearest_discs_second_diag(a, b, my_color)

            if row_prev is not None:
                set_change_row |= self.get_affected_row(a, b, row_prev[1], my_color)
            if row_next is not None:
                set_change_row |= self.get_affected_row(a, b, row_next[1], my_color)
            if col_up is not None:
                set_change_col |= self.get_affected_col(a, b, col_up[0], my_color)
            if col_bottom is not None:
                set_change_col |= self.get_affected_col(a, b, col_bottom[0], my_color)
            if fdiag_up is not None:
                set_change_fdiag |= self.get_affected_first_diag(a, b, fdiag_up[0], fdiag_up[1], my_color)
            if fdiag_bottom is not None:
                set_change_fdiag |= self.get_affected_first_diag(a, b, fdiag_bottom[0], fdiag_bottom[1], my_color)
            if sdiag_up is not None:
                set_change_sdiag |= self.get_affected_second_diag(a, b, sdiag_up[0], sdiag_up[1], my_color)
            if sdiag_bottom is not None:
                set_change_sdiag |= self.get_affected_second_diag(a, b, sdiag_bottom[0], sdiag_bottom[1], my_color)

            total_affected_discs = set_change_row | set_change_col | set_change_fdiag | set_change_sdiag
            
        return total_affected_discs

    # Method that calculate which discs in the row x should change the color if the moves put a disc of my_color
    # in position (a,b)
    def get_affected_row(self, a, b, b1, my_color):
        out_previous = set([])
        out_next = set([])
        enemy_color = self.representation.get_enemy_color(my_color)
        if b1 > b:
            j = b
            while j < b1:
                j += 1
                if self.representation.get_disc(a, j) == enemy_color:
                    out_next.add((a, j))
                elif self.representation.get_disc(a, j) == '-':
                    out_next.clear()
                    break
        elif b1 < b:
            j = b
            while j > b1:
                j -= 1
                if self.representation.get_disc(a, j) == enemy_color:
                    out_previous.add((a, j))
                elif self.representation.get_disc(a, j) == '-':
                    out_previous.clear()
                    break
        return out_next | out_previous

    # Method that calculate which discs in the col y should change the color if the moves put a disc of my_color
    # in position (a,b)    
    def get_affected_col(self, a, b, a1, my_color):
        out_above = set([])
        out_under = set([])
        enemy_color = self.representation.get_enemy_color(my_color)
        if a1 > a:
            i = a
            while i < a1:
                i += 1
                if self.representation.get_disc(i, b) == enemy_color:
                    out_under.add((i, b))
                elif self.representation.get_disc(i, b) == '-':
                    out_under.clear()
                    break
        elif a1 < a:
            i = a
            while i > a1:
                i -= 1
                if self.representation.get_disc(i, b) == enemy_color:
                    out_above.add((i, b))
                elif self.representation.get_disc(i, b) == '-':
                    out_above.clear()
                    break
        return out_above | out_under

    # Method that calculate which discs in the first diagonal that begin in position (0,0) and finish in position
    # (7,7) should change the color if the moves put a disc of my_color in position (a,b)
    def get_affected_first_diag(self, a, b, a1, b1, my_color):
        out_previous = set([])
        out_next = set([])
        enemy_color = self.representation.get_enemy_color(my_color)
        if a > a1 and b > b1:
            i = a
            j = b
            while i > a1 and j > b1:
                i -= 1
                j -= 1
                if self.representation.get_disc(i, j) == enemy_color:
                    out_previous.add((i, j))
                elif self.representation.get_disc(i, j) == '-':
                    out_previous.clear()
                    break
        elif a < a1 and b < b1:
            i = a
            j = b
            while i < a1 and j < b1:
                i += 1
                j += 1
                if self.representation.get_disc(i, j) == enemy_color:
                    out_next.add((i, j))
                elif self.representation.get_disc(i, j) == '-':
                    out_next.clear()
                    break
        return out_next | out_previous


    # Method that calculate which discs in the second diagonal that begin in position (0,7) and finish in position
    # (7,0) should change the color if the moves put a disc of my_color in position (a,b)
    def get_affected_second_diag(self, a, b, a1, b1, my_color):
        out_previous = set([])
        out_next = set([])
        enemy_color = self.representation.get_enemy_color(my_color)
        if a > a1 and b < b1:
            i = a
            j = b
            while i > a1 and j < b1:
                i -= 1
                j += 1
                if self.representation.get_disc(i, j) == enemy_color:
                    out_previous.add((i, j))
                elif self.representation.get_disc(i, j) == '-':
                    out_previous.clear()
                    break
        elif a < a1 and b > b1:
            i = a
            j = b
            while i < a1 and j > b1:
                i += 1
                j -= 1
                if self.representation.get_disc(i, j) == enemy_color:
                    out_next.add((i, j))
                elif self.representation.get_disc(i, j) == '-':
                    out_next.clear()
                    break
        return out_next | out_previous

    # Return the disc of the same color of mine that is in nearest position in the row 
    def get_nearest_discs_row(self, a, b, color):
        next_d = None
        previous = None
        j = b
        while j > 0:
            j -= 1
            if self.representation.get_disc(a, j) == color:
                previous = (a, j)
                break
        j = b
        while j < 7:
            j += 1
            if self.representation.get_disc(a, j) == color:
                next_d = (a, j)
                break
        return previous, next_d

    # Return the disc of the same color of mine that is in nearest position in the col
    def get_nearest_discs_col(self, a, b, color):
        above = None
        under = None
        i = a
        while i > 0:
            i -= 1
            if self.representation.get_disc(i, b) == color:
                above = (i, b)
                break
        i = a
        while i < 7:
            i += 1
            if self.representation.get_disc(i, b) == color:
                under = (i, b)
                break
        return above, under

    # Return the disc of the same color of mine that is in nearest position in the first diagonal
    def get_nearest_discs_first_diag(self, a, b, color):
        previous = None
        next_d = None
        # checking 1st semi-diagonal (from a,b to top-left)
        i = a
        j = b
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if self.representation.get_disc(i, j) == color:
                previous = (i, j)
                break
        # checking 2nd semi-diagonal (from a,b to bottom-right)
        i = a
        j = b
        while i < 7 and j < 7:
            i += 1
            j += 1
            if self.representation.get_disc(i, j) == color:
                next_d = (i, j)
                break
        return previous, next_d

    # Return the disc of the same color of mine that is in nearest position in the second diagonal
    def get_nearest_discs_second_diag(self, a, b, color):
        previous = None
        next_d = None
        # checking 1st semi-diagonal (from a,b to top-right)
        i = a
        j = b
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if self.representation.get_disc(i, j) == color:
                next_d = (i, j)
                break
        # checking 2nd semi-diagonal (from a,b to bottom-left)
        i = a
        j = b
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if self.representation.get_disc(i, j) == color:
                previous = (i, j)
                break
        return previous, next_d


class OthelloGame(Game):

    def __init__(self, h):
        self.state = OthelloState(h)

    # this method put a disc in position (a,b) and change the color of the discs affected
    @staticmethod
    def make_move(state, a, b, my_color, coordinates):
        out = cp.deepcopy(state)
        # for every affected disc, change it to my color
        if len(coordinates) > 0:
            out.set_disc(a, b, my_color)
            for pos in coordinates:
                out.set_disc(pos[0], pos[1], my_color)
                logging.debug("make_move: changed color of disc in pos ({}, {}) to {}\n".format(pos[0], pos[1], my_color))
        return out

    # Method that calculate the neigborood of a certain state
    def neighbors(self, turn, ext_state=None):
        if ext_state is None:
            state = cp.deepcopy(self.state)
        else:
            state = cp.deepcopy(ext_state)
        logging.debug("neighbors: copied state =\n {}".format(state.representation.board))
        out = set([state])
        for i in range(8):
            for j in range(8):
                if state.representation.get_disc(i, j) == '-':
                    affected_discs = state.get_w_discs_change(i, j, turn)
                    if len(affected_discs) > 0:
                        logging.debug("neighbors: state = \n {}".format(state.representation.board))
                        new_state = self.make_move(state, i, j, turn, affected_discs)
                        logging.debug("neighbors: new_state =\n {}".format(new_state.representation.board))
                        out.add(new_state)
        logging.debug("neighbours: discovered {} neighbours".format(len(out)))
        return out
