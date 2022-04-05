#!/usr/bin/env python

"""
Events used in SpaceShooter
"""

import enum
import copy
from spaceshooter.sutils import cycle


@enum.unique
class GameEvent(enum.IntEnum):
    """
    Overall game events
    """
    NONE = 0
    DROP = 1
    DROPS = 2
    MISSILES = 3
    MISSILES_EVEN = 4
    MISSILES_ODD = 5
    MEDKIT = 6
    TNT = 7
    FREEZE = 8
    LIGHTBALL = 9
    SHIELD = 10
    GUN_MISSILE = 11

    @staticmethod
    def __from_factory_level_1(num=0):
        """
        Create events for Level1
        :param num: Number of iterations
        :return: List of events
        """
        num = 3 if num < 1 else num
        scenario = [GameEvent.NONE,
                    GameEvent.DROP,
                    GameEvent.MISSILES_ODD,
                    GameEvent.NONE,
                    GameEvent.LIGHTBALL,
                    GameEvent.NONE,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.NONE,
                    GameEvent.FREEZE,
                    GameEvent.NONE,
                    GameEvent.SHIELD,
                    GameEvent.GUN_MISSILE,
                    GameEvent.MEDKIT,
                    GameEvent.NONE,
                    GameEvent.TNT,
                    GameEvent.MISSILES,
                    GameEvent.DROP,
                    GameEvent.LIGHTBALL,
                    GameEvent.NONE,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.NONE,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES_ODD,
                    GameEvent.DROP,
                    GameEvent.TNT,
                    GameEvent.NONE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.NONE]
        # Deep copy of scenario due to later cycling
        # (need to serve the same state for all games)
        sc_copy = copy.deepcopy(scenario)
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def __from_factory_level_2(num=0):
        """
        Create events for Level2
        :param num: Number of iterations
        :return: List of events
        """
        num = 3 if num < 1 else num
        scenario = [GameEvent.DROP,
                    GameEvent.NONE,
                    GameEvent.MISSILES,
                    GameEvent.NONE,
                    GameEvent.DROP,
                    GameEvent.TNT,
                    GameEvent.GUN_MISSILE,
                    GameEvent.NONE,
                    GameEvent.DROP,
                    GameEvent.LIGHTBALL,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.DROP,
                    GameEvent.SHIELD,
                    GameEvent.NONE,
                    GameEvent.MEDKIT,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROPS,
                    GameEvent.NONE,
                    GameEvent.MISSILES,
                    GameEvent.NONE,
                    GameEvent.DROP,
                    GameEvent.FREEZE,
                    GameEvent.MISSILES_ODD,
                    GameEvent.MEDKIT,
                    GameEvent.DROPS,
                    GameEvent.NONE,
                    GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.NONE,
                    GameEvent.LIGHTBALL,
                    GameEvent.GUN_MISSILE,
                    GameEvent.MEDKIT,
                    GameEvent.NONE,
                    GameEvent.DROP,
                    GameEvent.SHIELD,
                    GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.NONE,
                    GameEvent.LIGHTBALL]
        # Deep copy of scenario due to later cycling
        # (need to serve the same state for all games)
        sc_copy = copy.deepcopy(scenario)
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def __from_factory_level_3(num=0):
        """
        Create events for Level 3
        :param num: Number of iterations
        :return: List of events
        """
        num = 3 if num < 1 else num
        scenario = [GameEvent.MISSILES_ODD,
                    GameEvent.DROPS,
                    GameEvent.NONE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROPS,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.TNT,
                    GameEvent.DROPS,
                    GameEvent.MISSILES,
                    GameEvent.FREEZE,
                    GameEvent.DROP,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROPS,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES,
                    GameEvent.LIGHTBALL,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.SHIELD,
                    GameEvent.DROPS,
                    GameEvent.MISSILES,
                    GameEvent.TNT,
                    GameEvent.DROP,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROP,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES,
                    GameEvent.SHIELD,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.TNT,
                    GameEvent.DROP,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.DROPS,
                    GameEvent.LIGHTBALL,
                    GameEvent.MISSILES,
                    GameEvent.DROPS]
        # Deep copy of scenario due to later cycling
        # (need to serve the same state for all games)
        sc_copy = copy.deepcopy(scenario)
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def __from_factory_level_4(num=0):
        """
        Create events list for Level 4
        :param num: Number of iterations
        :return: List of events
        """
        num = 3 if num < 1 else num
        scenario = [GameEvent.MISSILES_EVEN,
                    GameEvent.DROP,
                    GameEvent.MISSILES_ODD,
                    GameEvent.LIGHTBALL,
                    GameEvent.GUN_MISSILE,
                    GameEvent.TNT,
                    GameEvent.MISSILES,
                    GameEvent.DROP,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES_ODD,
                    GameEvent.FREEZE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.SHIELD,
                    GameEvent.MISSILES,
                    GameEvent.DROP,
                    GameEvent.GUN_MISSILE,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.DROP,
                    GameEvent.MISSILES_ODD,
                    GameEvent.LIGHTBALL,
                    GameEvent.GUN_MISSILE,
                    GameEvent.TNT,
                    GameEvent.MISSILES,
                    GameEvent.FREEZE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.SHIELD,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.TNT,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROPS,
                    GameEvent.MISSILES_ODD,
                    GameEvent.DROP,
                    GameEvent.GUN_MISSILE,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES,
                    GameEvent.TNT,
                    GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.LIGHTBALL]
        # Deep copy of scenario due to later cycling
        # (need to serve the same state for all games)
        sc_copy = copy.deepcopy(scenario)
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def __from_factory_level_5(num=0):
        """
        Create events for Level 5
        :param num: Number of iterations
        :return: List of events
        """
        num = 3 if num < 1 else num
        scenario = [GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.LIGHTBALL,
                    GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.SHIELD,
                    GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.MISSILES,
                    GameEvent.MISSILES,
                    GameEvent.LIGHTBALL,
                    GameEvent.GUN_MISSILE,
                    GameEvent.MEDKIT,
                    GameEvent.MISSILES,
                    GameEvent.MISSILES,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROPS,
                    GameEvent.MISSILES,
                    GameEvent.MISSILES,
                    GameEvent.TNT,
                    GameEvent.GUN_MISSILE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.FREEZE,
                    GameEvent.MISSILES,
                    GameEvent.MISSILES,
                    GameEvent.MEDKIT,
                    GameEvent.GUN_MISSILE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.DROPS,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.MISSILES_ODD,
                    GameEvent.DROPS,
                    GameEvent.GUN_MISSILE,
                    GameEvent.GUN_MISSILE,
                    GameEvent.TNT,
                    GameEvent.MISSILES,
                    GameEvent.LIGHTBALL,
                    GameEvent.GUN_MISSILE,
                    GameEvent.SHIELD,
                    GameEvent.MISSILES_EVEN,
                    GameEvent.MISSILES_ODD,
                    GameEvent.MEDKIT]
        # Deep copy of scenario due to later cycling
        # (need to serve the same state for all games)
        sc_copy = copy.deepcopy(scenario)
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def from_factory(level: int, num=0):
        """
        Create events list
        :param level: Level number
        :param num: Number of iterations
        :return: List of events
        """
        factories = [
            GameEvent.__from_factory_level_1,
            GameEvent.__from_factory_level_2,
            GameEvent.__from_factory_level_3,
            GameEvent.__from_factory_level_4,
            GameEvent.__from_factory_level_5]
        level = 0 if level < 0 else level
        level = 4 if level > 4 else level
        return factories[level](num)


@enum.unique
class EnemyEvent(enum.IntEnum):
    """
    Overall enemy events
    """
    NONE = 0
    CIRCLE = 1
    SQUARE = 2
    FRONTBACK = 3
    UPDOWN = 4
    SINE = 5
    WAVE = 6
    BOSS = 7

    @staticmethod
    def __from_factory_level_1(num=0):
        """
        Crete enemies list for Level 1
        :param num: Number of iterations
        :return: List of enemies
        """
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        ad_copy = copy.deepcopy(addons)
        gen = cycle(ad_copy)
        num = 3 if num < 1 else num
        counter = 0
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def __from_factory_level_2(num=0):
        """
        Create enemies list for Level 2
        :param num: Number of iterations
        :return: List of enemies
        """
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        ad_copy = copy.deepcopy(addons)
        gen = cycle(ad_copy)
        # num = 30 if num < 1 else num
        num = 3 if num < 1 else num
        counter = 0
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def __from_factory_level_3(num=0):
        """
        Create enemies list for Level 3
        :param num: Number of iterations
        :return: List of enemies
        """
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        ad_copy = copy.deepcopy(addons)
        gen = cycle(ad_copy)
        # num = 30 if num < 1 else num
        num = 3 if num < 1 else num
        counter = 0
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def __from_factory_level_4(num=0):
        """
        Create enemies list for Level 4
        :param num: Number of iterations
        :return: List of enemies
        """
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        # num = 30 if num < 1 else num
        num = 3 if num < 1 else num
        counter = 0
        ad_copy = copy.deepcopy(addons)
        gen = cycle(ad_copy)
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def __from_factory_level_5(num=0):
        """
        Create enemies list for Level 5
        :param num: Number of iterations
        :return: List of enemies
        """
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        # num = 30 if num < 1 else num
        num = 3 if num < 1 else num
        counter = 0
        ad_copy = copy.deepcopy(addons)
        gen = cycle(ad_copy)
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def from_factory(level: int, num=0):
        """
        Create enemies list
        :param level: Level number
        :param num: Number of iterations
        :return: List of enemies
        """
        factories = [
            EnemyEvent.__from_factory_level_1,
            EnemyEvent.__from_factory_level_2,
            EnemyEvent.__from_factory_level_3,
            EnemyEvent.__from_factory_level_4,
            EnemyEvent.__from_factory_level_5]
        level = 0 if level < 0 else level
        level = 4 if level > 4 else level
        return factories[level](num)
