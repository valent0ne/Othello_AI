import GameModels as game
import Heuristics as heur
import logging


def main():
    logging_level = input("Insert logging level (DEBUG or INFO, default = INFO): ")
    if logging_level != "INFO" and logging_level != "DEBUG":
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level=logging_level)

    level = input("Insert level (min = 2, max = 15, default = 5): ")
    if level not in range(1, 16):
        level = 5
    heuristic = heur.OthelloHeuristic()
    othello = game.OthelloGame(heuristic)

    turn = 'k'

    logging.info("starting player: {}, initial board:\n {}".format(turn, game.initial_board))

    while True:

        states = othello.neighbors(turn)
        mx = -9999
        ix = 0

        for s in states:
            h = heuristic.Hl(othello, s, level, turn)
            if h > mx:
                mx = h
                ix = s

        logging.info("player {} move: \n {}".format(turn, ix.representation.board))
        exit(1)

        winner = ix.is_final()

        if winner is not None:
            logging.info("The winner is {}".format(winner))
            break

        turn = heur.OthelloHeurisdtic.get_enemy_color(turn)


if __name__ == "__main__":
    main()