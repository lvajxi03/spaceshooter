#!/usr/bin/env python

"""
Test game module
"""


from game import Game
from unittest.mock import Mock


def test_game_1():
    m = Mock()
    m.images = {}
    g = Game(m)
    g.change_board(Board.GAME)
    assert g.mode == Mode.INIT
    assert g.board == Board.GAME