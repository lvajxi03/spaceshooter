#!/usr/bin/env python

"""
Main launcher
"""

import sys
import random
import getopt
from spaceshooter.arena import SpaceShooter, Controller, Arena
from spaceshooter.game import Game
from spaceshooter.sdefs import ARENA_HEIGHT, ARENA_WIDTH
from spaceshooter.stypes import Board


def __usage__(msg=None):
    if msg:
        print(msg)
        print()
    print("Welcome to spaceshooter game!")
    print()
    print("Usage:")
    print(f"\t{sys.argv[0]} [options]")
    print()
    print("where options can be one or more of the following:")
    print()
    print("-f font-name -- use font-name for default font")
    print("-w -- use windowing mode instead of full screen")
    print("-h -- print this help message and terminate")
    print()
    print("That's all, folks!")


if __name__ == "__main__":
    FONT = None
    WINDOWING = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "wf:h", [])
        for o, a in opts:
            if o == "-f":
                if a.strip():
                    FONT = a
                else:
                    __usage__("No font name specified!")
                    sys.exit(1)
            elif o == "-w":
                WINDOWING = True
            else:
                __usage__(f"Unknown option: {o}")
                sys.exit(1)
    except getopt.GetoptError as ge:
        __usage__(str(ge))
        sys.exit(1)
    random.seed()
    shooter = SpaceShooter(sys.argv)
    shooter.game = Game(shooter)
    window = Controller(shooter)
    window.game = shooter.game
    shooter.window = window
    arena = Arena(window, font=FONT)
    arena.shooter = shooter
    shooter.game.arena = arena
    window.setCentralWidget(arena)
    if WINDOWING:
        window.setFixedSize(ARENA_WIDTH, ARENA_HEIGHT)
        window.show()

    else:
        window.showFullScreen()
    shooter.game.change_board(Board.WELCOME)
    sys.exit(shooter.exec())
