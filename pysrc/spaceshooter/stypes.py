#!/usr/bin/env python

"""
Common types and definitions
"""

import enum
import copy
from spaceshooter.sutils import cycle


@enum.unique
class Key(enum.IntEnum):
    """
    Key abstraction class
    """
    NONE = 0
    KEY_F1 = 1
    KEY_ENTER = 2
    KEY_ESCAPE = 3
    KEY_LEFT = 4
    KEY_RIGHT = 5
    KEY_TOP = 6
    KEY_BOTTOM = 7
    KEY_BACKSPACE = 8
    KEY_SPACE = 9
    KEY_A = 10
    KEY_B = 11
    KEY_C = 12
    KEY_D = 13
    KEY_E = 14
    KEY_F = 15
    KEY_G = 16
    KEY_H = 17
    KEY_I = 18
    KEY_J = 19
    KEY_K = 20
    KEY_L = 21
    KEY_M = 22
    KEY_N = 23
    KEY_O = 24
    KEY_P = 25
    KEY_Q = 26
    KEY_R = 27
    KEY_S = 28
    KEY_T = 29
    KEY_U = 30
    KEY_V = 31
    KEY_W = 32
    KEY_X = 33
    KEY_Y = 34
    KEY_Z = 35
    KEY_0 = 36
    KEY_1 = 37
    KEY_2 = 38
    KEY_3 = 39
    KEY_4 = 40
    KEY_5 = 41
    KEY_6 = 42
    KEY_7 = 43
    KEY_8 = 44
    KEY_9 = 45
    KEY_UNDERSCORE = 46
    KEY_DASH = 47

    def is_move(self):
        """
        Check if key can be configured in setup
        :return: True if key can be configured in setup, false otherwise
        """
        return self.value >= Key.KEY_LEFT

    def __str__(self):
        cname = {
            Key.NONE: '⃠',
            Key.KEY_LEFT: '←',
            Key.KEY_RIGHT: '→',
            Key.KEY_TOP: '↑',
            Key.KEY_BOTTOM: '↓',
            Key.KEY_ENTER: 'Enter',
            Key.KEY_ESCAPE: 'Esc',
            Key.KEY_BACKSPACE: 'Bksp',
            Key.KEY_SPACE: '˽',
            Key.KEY_A: 'A',
            Key.KEY_B: 'B',
            Key.KEY_C: 'C',
            Key.KEY_D: 'D',
            Key.KEY_E: 'E',
            Key.KEY_F: 'F',
            Key.KEY_G: 'G',
            Key.KEY_H: 'H',
            Key.KEY_I: 'I',
            Key.KEY_J: 'J',
            Key.KEY_K: 'K',
            Key.KEY_L: 'L',
            Key.KEY_M: 'M',
            Key.KEY_N: 'N',
            Key.KEY_O: 'O',
            Key.KEY_P: 'P',
            Key.KEY_Q: 'Q',
            Key.KEY_R: 'R',
            Key.KEY_S: 'S',
            Key.KEY_T: 'T',
            Key.KEY_U: 'U',
            Key.KEY_V: 'V',
            Key.KEY_W: 'W',
            Key.KEY_X: 'X',
            Key.KEY_Y: 'Y',
            Key.KEY_Z: 'Z',
            Key.KEY_0: '0',
            Key.KEY_1: '1',
            Key.KEY_2: '2',
            Key.KEY_3: '3',
            Key.KEY_4: '4',
            Key.KEY_5: '5',
            Key.KEY_6: '6',
            Key.KEY_7: '7',
            Key.KEY_8: '8',
            Key.KEY_9: '9',
            Key.KEY_UNDERSCORE: '_',
            Key.KEY_DASH: '-',
            Key.KEY_F1: 'F1'
        }
        return cname[self]


@enum.unique
class MouseButton(enum.IntEnum):
    """
    Mouse button abstraction enum
    """
    NONE = 0
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5


class MouseEvent:
    """
    Mouse event abstraction class
    """
    x = -1
    y = -1
    button = MouseButton.NONE

    def __init__(self, x: int, y: int, button: MouseButton):
        """
        Create MouseEvent instance
        :param x: X coordinate of mouse event
        :param y: Y coordinate of mouse event
        :param button: Button used in the event
        """
        self.x = x
        self.y = y
        self.button = button

    def get_x(self):
        """
        Get X coordinate
        :return: X coordinate
        """
        return self.x

    def get_y(self):
        """
        Get Y coordinate
        :return: Y coordinate
        """
        return self.y


@enum.unique
class Board(enum.IntEnum):
    """
    Board representation
    """
    NONE = -1
    WELCOME = 0
    MENU = 1
    GAME = 2
    OPTIONS = 3
    HISCORES = 4
    SETUP = 5
    HELP = 6
    ABOUT = 7
    QUIT = 8
    NEWSCORE = 9
    PLAYER = 10


@enum.unique
class UserInput(enum.IntEnum):
    """
    User input abstraction enum
    """
    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    FIRE = 5
    BOMB = 6
    TNT = 7
    ESC = 8
    ENTER = 9
    BACKSPACE = 10
    TEXT = 11


@enum.unique
class FireballDirection(enum.IntEnum):
    """
    Fireball direction
    """
    UP = 0
    STRAIGHT = 1
    DOWN = 2


@enum.unique
class Mode(enum.IntEnum):
    """
    Game mode enum
    """
    NONE = 0
    INIT = 1
    PREPARE = 2
    PLAY = 3
    PAUSED = 4
    KILLED = 5
    GAMEOVER = 6
    CONGRATS = 7


@enum.unique
class SetupMode(enum.IntEnum):
    """
    Setup mode enum
    """
    DISPLAY = 0
    ENTER = 1


@enum.unique
class Options(enum.IntEnum):
    """
    Available game options
    """
    EASY = 0
    NORMAL = 1
    HARD = 2
    UNLIMITED = 3


@enum.unique
class MissileType(enum.IntEnum):
    """
    Various missile types
    """
    FROM = 0
    TO = 1
    FROM_NE = 2
    FROM_SE = 3
    TO_NW = 4
    TO_SW = 5
    TO_NWW = 6
    TO_SWW = 7


@enum.unique
class MovableType(enum.IntEnum):
    """
    Available movable types
    """
    DZIALO = 0
    DOM1 = 1
    DOM2 = 2
    DOM3 = 3
    FABRYKA1 = 4
    FABRYKA2 = 5
    FABRYKA3 = 6
    WIEZOWIEC1 = 7
    WIEZOWIEC2 = 8
    WIEZOWIEC3 = 9

    @staticmethod
    def get_from_factory_level_1():
        """
        Movable factory for level 1
        :return: None
        """
        scenario = [MovableType.DOM1,
                    MovableType.FABRYKA1,
                    MovableType.WIEZOWIEC1,
                    MovableType.DOM2,
                    MovableType.FABRYKA2,
                    MovableType.DZIALO,
                    MovableType.WIEZOWIEC2,
                    MovableType.DOM3,
                    MovableType.FABRYKA3,
                    MovableType.WIEZOWIEC3,
                    MovableType.DZIALO]
        sc_copy = copy.deepcopy(scenario)
        generator = cycle(sc_copy)
        return generator

    @staticmethod
    def get_from_factory_level_2():
        """
        Movable factory for level 2
        :return: None
        """
        scenario = [MovableType.DOM1,
                    MovableType.FABRYKA1,
                    MovableType.WIEZOWIEC1,
                    MovableType.DZIALO,
                    MovableType.DOM2,
                    MovableType.FABRYKA2,
                    MovableType.WIEZOWIEC3,
                    MovableType.DZIALO,
                    MovableType.DOM3,
                    MovableType.WIEZOWIEC3,
                    MovableType.FABRYKA3,
                    MovableType.DZIALO]
        sc_copy = copy.deepcopy(scenario)
        generator = cycle(sc_copy)
        return generator

    @staticmethod
    def get_from_factory_level_3():
        """
        Movable factory for level 3
        :return: None
        """
        scenario = [MovableType.DOM1,
                    MovableType.FABRYKA1,
                    MovableType.WIEZOWIEC1,
                    MovableType.DZIALO,
                    MovableType.DZIALO,
                    MovableType.DOM2,
                    MovableType.FABRYKA2,
                    MovableType.WIEZOWIEC2,
                    MovableType.DZIALO,
                    MovableType.DZIALO,
                    MovableType.DOM3,
                    MovableType.FABRYKA3,
                    MovableType.WIEZOWIEC3,
                    MovableType.DZIALO,
                    MovableType.DZIALO]
        sc_copy = copy.deepcopy(scenario)
        generator = cycle(sc_copy)
        return generator

    @staticmethod
    def get_from_factory_level_4():
        """
        Movable factory for level 4
        :return: None
        """
        scenario = [MovableType.DOM1,
                    MovableType.WIEZOWIEC1,
                    MovableType.DZIALO,
                    MovableType.FABRYKA1,
                    MovableType.DOM2,
                    MovableType.DZIALO,
                    MovableType.WIEZOWIEC2,
                    MovableType.FABRYKA2,
                    MovableType.DZIALO,
                    MovableType.DOM3,
                    MovableType.FABRYKA3,
                    MovableType.DZIALO,
                    MovableType.WIEZOWIEC3,
                    MovableType.DOM2,
                    MovableType.DZIALO]
        sc_copy = copy.deepcopy(scenario)
        generator = cycle(sc_copy)
        return generator

    @staticmethod
    def get_from_factory_level_5():
        """
        Movable factory for level 5
        :return:
        """
        scenario = [MovableType.DOM1,
                    MovableType.WIEZOWIEC1,
                    MovableType.DZIALO,
                    MovableType.DZIALO,
                    MovableType.FABRYKA1,
                    MovableType.DOM2,
                    MovableType.DZIALO,
                    MovableType.DZIALO,
                    MovableType.WIEZOWIEC2,
                    MovableType.FABRYKA2,
                    MovableType.DZIALO,
                    MovableType.DZIALO,
                    MovableType.DOM3,
                    MovableType.FABRYKA3,
                    MovableType.DZIALO,
                    MovableType.DZIALO,
                    MovableType.WIEZOWIEC3,
                    MovableType.DOM2,
                    MovableType.DZIALO,
                    MovableType.DZIALO]
        sc_copy = copy.deepcopy(scenario)
        generator = cycle(sc_copy)
        return generator

    @staticmethod
    def get_from_factory(level: int):
        """
        Create movables for specific level
        :param level: game level
        :return: movables list
        """
        factories = [
            MovableType.get_from_factory_level_1,
            MovableType.get_from_factory_level_2,
            MovableType.get_from_factory_level_3,
            MovableType.get_from_factory_level_4,
            MovableType.get_from_factory_level_5]
        level = 4 if level > 4 else level
        level = 0 if level < 0 else level
        return factories[level]()
