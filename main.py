import GameModels as game
import Heuristics as heur
import logging
import copy as cp
import numpy as np
from datetime import datetime
import time


def main():

    logging.basicConfig(level='INFO')
    level = input("Insert level (odd number): ")

    # the play will be saved in this file
    file_name = "_plays/othello_{}.txt".format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    out = open(file_name, "w")

    heuristic = heur.OthelloHeuristic()
    othello = game.OthelloGame(heuristic)

    # k start first
    turn = 'k'

    logging.info("starting player: {}, initial board:\n {}\n\n".format(turn, np.array(cp.copy(game.initial_board))))

    ix = othello.state

    start = time.time()

    while True:

        states = othello.neighbors(turn, ix)
        mx = -9999
        # store previous board
        previous = ix

        # cycle through the neighbors
        for s in states:
            # if the state is the previous one make it less valuable (so you will not get stuck)
            if s == previous:
                h = -1000
            else:
                # compute the heuristic value of the state s
                h = heuristic.Hl(othello, s, level, turn)

            logging.info("possible move for player {}; state = \n {} \n heuristic = {}\n".format(turn, s.representation.board, h))
            if h > mx:
                mx = h
                ix = s

        # at the end ix will contain the best state of the neighbor, log the state and write it in the out file
        logging.info("MOVE: player {} = \n {}\n\n".format(turn, ix.representation.board))
        out.write("MOVE: player {} = \n {}\n\n".format(turn, ix.representation.board))

        # check whether the state is final
        winner = ix.is_final()

        # if there is a winner print it and quit
        if winner is not None:
            elapsed_time = time.time()-start
            logging.info("The winner is player: {}".format(winner))
            logging.info("Elapsed time: {}".format(elapsed_time))

            out.write("The winner is player: {}\n".format(winner))
            out.write("Elapsed time: {}".format(elapsed_time))
            out.close()
            break

        turn = heur.OthelloHeuristic.get_enemy_color(turn)


if __name__ == "__main__":
    main()
