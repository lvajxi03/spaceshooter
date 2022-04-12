#!/usr/bin/env python

"""
Test game module
"""


from spaceshooter.game import Game
from spaceshooter.stypes import Board, Mode
from unittest.mock import Mock


def test_game_1():
    """
    Change board and check what happened
    :return: None
    """
    shooter_mock = Mock()
    shooter_mock.images = {'star': None}
    game = Game(shooter_mock)
    game.change_board(Board.GAME)
    assert game.mode == Mode.INIT
    assert game.board == Board.GAME
