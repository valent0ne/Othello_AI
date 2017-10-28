import GameModels as game
import Heuristics as heur
import numpy as np
import logging


def main():
    logging_level = input("Insert logging level (DEBUG or INFO, default = INFO): ")
    if logging_level != "INFO" and logging_level != "DEBUG":
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level=logging_level)
    return "pippo"

if __name__ == "__main__":
    main()