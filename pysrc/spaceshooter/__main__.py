#!/usr/bin/env python

"""
Main launcher
"""

import sys
import random
from spaceshooter.arena import SpaceShooter, Controller, Arena
from spaceshooter.game import Game, Board
from spaceshooter.sdefs import ARENA_HEIGHT, ARENA_WIDTH


if __name__ == "__main__":
    try:
        FIXED_SIZE = (sys.argv[1] == "-f")
    except IndexError:
        FIXED_SIZE = False
    random.seed()
    shooter = SpaceShooter(sys.argv)
    shooter.game = Game(shooter)
    window = Controller(shooter)
    window.game = shooter.game
    shooter.window = window
    arena = Arena(window)
    arena.shooter = shooter
    shooter.game.arena = arena
    window.setCentralWidget(arena)
    if FIXED_SIZE:
        window.showFullScreen()
    else:
        window.setFixedSize(ARENA_WIDTH, ARENA_HEIGHT)
        window.show()
    shooter.game.change_board(Board.WELCOME)
    sys.exit(shooter.exec())
