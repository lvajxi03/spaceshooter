#!/usr/bin/env python

import enum
import random
import os
import math

from stypes import (
    UserInput,
    Key,
    Options,
    MissileType,
    MovableType,
    FireballDirection,
    Board,
    Mode,
    SetupMode
)
from primi import (
    Rect,
    Tnt,
    Drop,
    Missile,
    Medkit,
    IceBox,
    Enemy,
    LightBall,
    Boss,
    Player,
    Movable,
    Explosion,
    Bomb,
    FireMissile,
    Shield,
    Star
)
from sconfig import ShooterConfig
from sutils import cycle
from sdefs import *


@enum.unique
class GameEvent(enum.IntEnum):
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
    def from_factory_level_1(num=0):
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
        sc_copy = [x for x in scenario]
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def from_factory_level_2(num=0):
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
        sc_copy = [x for x in scenario]
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def from_factory_level_3(num=0):
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
        sc_copy = [x for x in scenario]
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def from_factory_level_4(num=0):
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
        sc_copy = [x for x in scenario]
        counter = 0
        gen = cycle(sc_copy)
        events = []
        while counter < num:
            event = next(gen)
            events.append(event)
            counter += 1
        return events

    @staticmethod
    def from_factory_level_5(num=0):
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
        sc_copy = [x for x in scenario]
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
        factories = [
            GameEvent.from_factory_level_1,
            GameEvent.from_factory_level_2,
            GameEvent.from_factory_level_3,
            GameEvent.from_factory_level_4,
            GameEvent.from_factory_level_5]
        level = 0 if level < 0 else level
        level = 4 if level > 4 else level
        return factories[level](num)


@enum.unique
class EnemyEvent(enum.IntEnum):
    NONE = 0
    CIRCLE = 1
    SQUARE = 2
    FRONTBACK = 3
    UPDOWN = 4
    SINE = 5
    WAVE = 6
    BOSS = 7

    @staticmethod
    def from_factory_level_1(num=0):
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        ad_copy = [x for x in addons]
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
    def from_factory_level_2(num=0):
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        ad_copy = [x for x in addons]
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
    def from_factory_level_3(num=0):
        enemies = []
        addons = [EnemyEvent.CIRCLE,
                  EnemyEvent.SQUARE,
                  EnemyEvent.FRONTBACK,
                  EnemyEvent.UPDOWN,
                  EnemyEvent.SINE,
                  EnemyEvent.WAVE]
        ad_copy = [x for x in addons]
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
    def from_factory_level_4(num=0):
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
        ad_copy = [x for x in addons]
        gen = cycle(ad_copy)
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def from_factory_level_5(num=0):
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
        ad_copy = [x for x in addons]
        gen = cycle(ad_copy)
        while counter < num:
            enemy = next(gen)
            enemies.append(enemy)
            counter += 1
        return enemies

    @staticmethod
    def from_factory(level: int, num=0):
        factories = [
            EnemyEvent.from_factory_level_1,
            EnemyEvent.from_factory_level_2,
            EnemyEvent.from_factory_level_3,
            EnemyEvent.from_factory_level_4,
            EnemyEvent.from_factory_level_5]
        level = 0 if level < 0 else level
        level = 4 if level > 4 else level
        return factories[level](num)


class EventManager:
    """
    Manage game events in efficient way
    """

    def __init__(self, parent, shooter):
        """
        Create EventManager object
        :param parent: Game parent handler
        :param shooter: Shooter handler
        """
        self.eventq = []
        self.parent = parent
        self.shooter = shooter
        self.level = 0
        self.creates = {
            GameEvent.DROP: self.create_drop,
            GameEvent.DROPS: self.create_drops,
            GameEvent.MISSILES: self.create_missiles,
            GameEvent.MISSILES_ODD: self.create_missiles_odd,
            GameEvent.MISSILES_EVEN: self.create_missiles_even,
            GameEvent.MEDKIT: self.create_medkit,
            GameEvent.FREEZE: self.create_freeze,
            GameEvent.LIGHTBALL: self.create_lightball,
            GameEvent.SHIELD: self.create_shield,
            GameEvent.TNT: self.create_tnt,
            GameEvent.GUN_MISSILE: self.create_gun_missiles
        }

    def set_level(self, level: int):
        """
        Set level to populate events
        :param level: Game level number
        """
        self.level = level
        iterations = 12 + self.level + self.parent.options_pos
        self.eventq = GameEvent.from_factory(level, iterations * MAX_EVENTS_FACTOR)

    def pop(self) -> GameEvent:
        """
        Get first event from queue
        :return: GameEvent object
        """
        return self.eventq.pop(0)

    def create_tnt(self):
        """
        Create a single, random TNT box
        """
        t = Tnt(
            ARENA_WIDTH,
            random.randint(150, 3 * ARENA_HEIGHT // 4),
            self.shooter.images['indicators']['tnt'])
        self.parent.tnts.append(t)

    def create_drop(self):
        """
        Create a single, random drop
        """
        d = Drop(random.randint(
            ARENA_WIDTH // 3, ARENA_WIDTH),
            0,
            self.shooter.images['indicators']['drop'])
        self.parent.drops.append(d)

    def create_drops(self):
        """
        Create two random drops
        """
        d = Drop(random.randint(
            ARENA_WIDTH // 3, 2 * ARENA_WIDTH // 3),
            0,
            self.shooter.images['indicators']['drop'])
        self.parent.drops.append(d)
        d = Drop(random.randint(
            2 * ARENA_WIDTH // 3, ARENA_WIDTH),
            0,
            self.shooter.images['indicators']['drop'])
        self.parent.drops.append(d)

    def create_gun_missiles(self):
        """
        Create gun missiles for every visible gun, (if not in frozen mode)
        :return: None
        """
        if self.parent.frozen_timer == 0:
            for movable in self.parent.movables:
                if movable.is_valid() and movable.etype == MovableType.DZIALO:
                    image = self.shooter.images['missiles'][MissileType.TO_NW]
                    m = Missile(movable.x - image.width(),
                                movable.y - image.height(),
                                MissileType.TO_NW,
                                image)
                    self.parent.missiles.append(m)

    def create_missiles(self):
        if len(self.parent.enemymanager.enemies) > 0 and self.parent.frozen_timer == 0:
            image = self.shooter.images['missiles'][MissileType.TO]
            w = image.width()
            h = image.height()
            for e in self.parent.enemymanager.enemies:
                m = Missile(e.x - w,
                            e.y - h // 2,
                            MissileType.TO,
                            image)
                self.parent.missiles.append(m)

    def create_missiles_even(self):
        if len(self.parent.enemymanager.enemies) > 0 and self.parent.frozen_timer == 0:
            image = self.shooter.images['missiles'][MissileType.TO]
            w = image.width()
            h = image.height()
            for e in self.parent.enemymanager.enemies:
                if not e.odd:
                    m = Missile(e.x - w,
                                e.y - h // 2,
                                MissileType.TO,
                                image)
                    self.parent.missiles.append(m)

    def create_missiles_odd(self):
        if len(self.parent.enemymanager.enemies) > 0 and self.parent.frozen_timer == 0:
            image = self.shooter.images['missiles'][MissileType.TO]
            w = image.width()
            h = image.height()
            for e in self.parent.enemymanager.enemies:
                if e.odd:
                    m = Missile(e.x - w,
                                e.y - h // 2,
                                MissileType.TO,
                                image)
                    self.parent.missiles.append(m)

    def create_medkit(self):
        m = Medkit(ARENA_WIDTH,
                   random.randint(250, 3 * ARENA_HEIGHT // 4),
                   self.shooter.images['indicators']['medkit'])
        self.parent.medkits.append(m)

    def create_freeze(self):
        f = IceBox(ARENA_WIDTH,
                   random.randint(150, 3 * ARENA_HEIGHT // 4),
                   self.shooter.images['indicators']['frozen-box'])
        self.parent.iceboxes.append(f)

    def create_lightball(self):
        """
        Create random LightBall object
        """
        lb = LightBall(ARENA_WIDTH,
                       random.randint(150, 3 * ARENA_HEIGHT // 4),
                       self.shooter.images['indicators']['light-ball'])
        self.parent.lightballs.append(lb)

    def create_shield(self):
        """
        Create random Shield object
        """
        s = Shield(ARENA_WIDTH,
                   random.randint(150, 3 * ARENA_HEIGHT // 4),
                   self.shooter.images['indicators']['shield'])
        self.parent.shields.append(s)

    def run(self):
        if len(self.eventq) > 0:
            event = self.pop()
            if event is not GameEvent.NONE:
                creator = self.creates[event]
                creator()


class EnemyManager:
    """
    Manage game enemies in efficient way
    """

    def __init__(self, parent, shooter):
        self.enemies = []
        self.parent = parent
        self.shooter = shooter
        self.boss = None
        self.images = [x for x in self.shooter.images['enemies']]
        self.imagen = cycle(self.images)
        self.etype = EnemyEvent.NONE
        self.level = 0
        self.eventq = []
        self.creates = {
            EnemyEvent.CIRCLE: self.create_circle,
            EnemyEvent.SQUARE: self.create_square,
            EnemyEvent.FRONTBACK: self.create_frontback,
            EnemyEvent.UPDOWN: self.create_updown,
            EnemyEvent.SINE: self.create_sine,
            EnemyEvent.WAVE: self.create_wave
        }
        self.moves = {
            EnemyEvent.CIRCLE: self.move_circle,
            EnemyEvent.SQUARE: self.move_square,
            EnemyEvent.FRONTBACK: self.move_frontback,
            EnemyEvent.UPDOWN: self.move_updown,
            EnemyEvent.SINE: self.move_sine,
            EnemyEvent.WAVE: self.move_wave
        }

    def set_level(self, level: int):
        self.level = level
        iterations = 12 + self.level + self.parent.options_pos
        self.eventq = EnemyEvent.from_factory(level, iterations)

    def push(self, event: EnemyEvent):
        self.eventq.append(event)

    def pop(self) -> EnemyEvent:
        return self.eventq.pop(0)

    def clear(self):
        self.enemies = []
        self.boss = None

    def create_frontback(self):
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            ax = 400 if odd else 0
            enemy = Enemy(
                ARENA_WIDTH - 650 + ax,
                150 + i * 80 - (0 if odd else 60),
                odd,
                image,
                speedx=-10,
                speedy=2)
            self.enemies.append(enemy)

    def create_circle(self):
        image = next(self.imagen)
        radius = (ARENA_HEIGHT * 2 / 3 - 100) / 2
        spotx = int(ARENA_WIDTH / 2 + radius)
        spoty = int(100 + radius)
        for i in range(8):
            odd = (i % 2) == 0
            enemy = Enemy(
                spotx,
                spoty,
                odd,
                image,
                angle=i * 45,
                radius=radius,
                speedx=-5)
            self.enemies.append(enemy)
        self.move()

    def create_square(self):
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            ax = 250 if odd else 0
            enemy = Enemy(
                ARENA_WIDTH - 550 + ax,
                150 + i * 80,
                odd,
                image,
                speedx=-8,
                speedy=8)
            self.enemies.append(enemy)

    def create_updown(self):
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            enemy = Enemy(
                int(ARENA_WIDTH * 0.45) + 130 * i,
                int(ARENA_HEIGHT * 0.1) if odd else int(ARENA_HEIGHT * 0.6),
                odd,
                image,
                speedx=-3,
                speedy=13 if odd else -13)
            self.enemies.append(enemy)

    def create_sine(self):
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            dx = 250 if odd else 0
            enemy = Enemy(
                int(ARENA_WIDTH * 0.9) - dx,
                (i + 2) * 80,
                odd,
                image,
                speedx=-5,
                speedy=10)
            self.enemies.append(enemy)

    def create_wave(self):
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            enemy = Enemy(
                int(0.8 * ARENA_WIDTH) if odd else int(0.9 * ARENA_WIDTH),
                250 + 70 * i,
                odd,
                image,
                speedx=-8,
                speedy=15)
            self.enemies.append(enemy)

    def create_boss(self):
        self.boss = Boss((2 * ARENA_WIDTH) // 3,
                         random.randint(5, STAGE_HEIGHT - 100),
                         self.shooter.images['boss'])

    def create_boss_missiles(self):
        fixed_height = 32
        for t in [MissileType.TO, MissileType.TO_SWW, MissileType.TO_NWW]:
            self.parent.missiles.append(
                Missile(
                    self.boss.x - i.width(),
                    self.boss.y + fixed_height - i.height() // 2,
                    t,
                    self.shooter.images['missiles'][t]))

    def move_circle(self):
        for enemy in self.enemies:
            enemy.angle += 2
            enemy.angle %= 360
            radians = math.pi * enemy.angle / 180.0
            dx = enemy.radius * math.cos(radians)
            dy = enemy.radius * math.sin(radians)
            enemy.x = enemy.spot_x + int(dx) + enemy.speedx
            enemy.y = enemy.spot_y + int(dy)
            enemy.spot_x += enemy.speedx
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def move_square(self):
        for enemy in self.enemies:
            enemy.x += enemy.speedx * enemy.dx
            enemy.y += enemy.speedy * enemy.dy
            if enemy.moved == 0:
                enemy.dy = 0
                enemy.dx = 1 if enemy.odd else -1
            elif enemy.moved == 40:
                enemy.dy = 0
                enemy.dx = -1 if enemy.odd else 1
            elif enemy.moved == 20:
                enemy.dx = 0
                enemy.dy = 1 if enemy.odd else -1
            elif enemy.moved == 60:
                enemy.dx = 0
                enemy.dy = -1 if enemy.odd else 1
            enemy.moved += 1
            enemy.moved %= 80
            enemy.x -= 2
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def move_frontback(self):
        for enemy in self.enemies:
            enemy.x += enemy.speedx * enemy.dx
            enemy.y += enemy.speedy * enemy.dy
            if enemy.moved == 0 or enemy.moved == 30:
                enemy.dy = -enemy.dy
            elif enemy.moved == 15 or enemy.moved == 45:
                enemy.dx = -enemy.dx
            enemy.moved += 1
            enemy.moved %= 60
            enemy.x -= 2
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def move_updown(self):
        for enemy in self.enemies:
            enemy.y += enemy.speedy
            enemy.x += enemy.speedx
            if enemy.y < int(ARENA_HEIGHT * 0.1):
                enemy.speedy = -enemy.speedy
            elif enemy.y > int(ARENA_HEIGHT * 0.7):
                enemy.speedy = -enemy.speedy
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def move_sine(self):
        for enemy in self.enemies:
            radians = math.pi * enemy.x / 180.0
            if enemy.odd:
                enemy.dy = int(100 * math.sin(radians))
                enemy.y = enemy.spot_y - enemy.dy
            else:
                enemy.dy = int(100 * math.cos(radians))
                enemy.y = enemy.spot_y + enemy.dy
            enemy.x += enemy.speedx
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def move_wave(self):
        for enemy in self.enemies:
            enemy.x += enemy.speedx
            sektor = enemy.x // 150
            if sektor % 2 == 0:
                if enemy.odd:
                    enemy.y += enemy.speedy
                else:
                    enemy.y -= enemy.speedy
            else:
                if enemy.odd:
                    enemy.y -= enemy.speedy
                else:
                    enemy.y += enemy.speedy
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def populate(self, event):
        """
        Populate enemies list according to next EnemyEvent in queue
        :param event: EnemyEvent from the event queue
        """
        self.etype = event
        if self.etype is not EnemyEvent.NONE:
            creator = self.creates[event]
            creator()

    def move(self):
        """
        Move available enemies according to current scenario
        """
        if self.boss:
            self.boss.move()
        elif self.etype is not EnemyEvent.NONE:
            mover = self.moves[self.etype]
            mover()

    def run(self):
        if len(self.enemies) == 0 and self.level < MAX_LEVEL:
            if len(self.eventq) > 0:
                # There is still something to pick
                event = self.pop()
                self.populate(event)
            else:
                return False
        elif len(self.enemies) == 0 and self.level == MAX_LEVEL:
            if len(self.eventq) > 0:
                # There is still something to pick
                event = self.pop()
                self.populate(event)
            else:
                if not self.boss:
                    self.parent.missiles = []
                    self.parent.lightballs = []
                    self.parent.tnts = []
                    self.parent.shield_timer = 0
                    self.parent.lighball_timer = 0
                    self.parent.frozen_timer = 0
                    self.create_boss()
                else:
                    if self.boss.is_alive():
                        self.create_boss_missiles()
                    else:
                        return False
        return True

    def paint(self, painter):
        for enemy in self.enemies:
            enemy.paint(painter)
        if self.boss:
            self.boss.paint(painter)


class Game:
    def __init__(self, shooter):
        self.config = ShooterConfig(
            filename=os.path.expanduser("~/.spaceshooterrc"))
        self.config.read()
        self.counter = {
            'welcome': 1
        }
        self.menu_boards = [
            Board.GAME,
            Board.OPTIONS,
            Board.HISCORES,
            Board.SETUP,
            Board.HELP,
            Board.ABOUT,
            Board.QUIT,
        ]
        self.shooter = shooter
        self.arena = None
        self.mode = Mode.NONE
        # Setup-related
        self.setupmode = SetupMode.DISPLAY
        self.temp_setup = {}
        self.setup_counter = 0
        self.temp_position = 0
        self.setup_keys = [
            UserInput.LEFT,
            UserInput.RIGHT,
            UserInput.TOP,
            UserInput.BOTTOM,
            UserInput.FIRE,
            UserInput.BOMB,
            UserInput.TNT
        ]
        # Board-related
        self.board = Board.NONE
        self.next_board = Board.NONE
        self.game_counter = 0
        self.menupos2board = [
            Board.PLAYER,
            Board.OPTIONS,
            Board.HISCORES,
            Board.SETUP,
            Board.HELP,
            Board.ABOUT,
            Board.QUIT
        ]
        self.optionspos2option = [
            Options.EASY,
            Options.NORMAL,
            Options.HARD,
            Options.UNLIMITED
        ]
        self.mousepress_events = {
            Board.WELCOME: self.mousepress_welcome,
            Board.MENU: self.mousepress_menu,
            Board.PLAYER: self.mousepress_player,
            Board.GAME: self.mousepress_game,
            Board.OPTIONS: self.mousepress_options,
            Board.HISCORES: self.mousepress_hiscores,
            Board.SETUP: self.mousepress_setup,
            Board.HELP: self.mousepress_help,
            Board.ABOUT: self.mousepress_about,
            Board.QUIT: self.mousepress_quit,
            Board.NEWSCORE: self.mousepress_newscore
        }
        self.keypress_events = {
            Board.WELCOME: self.keypress_welcome,
            Board.PLAYER: self.keypress_player,
            Board.MENU: self.keypress_menu,
            Board.GAME: self.keypress_game,
            Board.OPTIONS: self.keypress_options,
            Board.HISCORES: self.keypress_hiscores,
            Board.SETUP: self.keypress_setup,
            Board.HELP: self.keypress_help,
            Board.ABOUT: self.keypress_about,
            Board.QUIT: self.keypress_quit,
            Board.NEWSCORE: self.keypress_newscore,
        }
        self.keyrelease_events = {
            Board.WELCOME: self.keyrelease_welcome,
            Board.PLAYER: self.keyrelease_player,
            Board.MENU: self.keyrelease_menu,
            Board.GAME: self.keyrelease_game,
            Board.OPTIONS: self.keyrelease_options,
            Board.HISCORES: self.keyrelease_hiscores,
            Board.SETUP: self.keyrelease_setup,
            Board.HELP: self.keyrelease_help,
            Board.ABOUT: self.keyrelease_about,
            Board.QUIT: self.keyrelease_quit,
            Board.NEWSCORE: self.keyrelease_newscore
        }
        self.keyreleasegame_events = {
            Mode.INIT: self.keyrelease_init,
            Mode.PLAY: self.keyrelease_play,
            Mode.PAUSED: self.keyrelease_paused,
            Mode.KILLED: self.keyrelease_killed,
            Mode.PREPARE: self.keyrelease_prepare,
            Mode.GAMEOVER: self.keyrelease_gameover,
            Mode.CONGRATS: self.keyrelease_congrats
        }
        self.board_initializers = {
            Board.WELCOME: self.init_welcome,
            Board.PLAYER: self.init_player,
            Board.MENU: self.init_menu,
            Board.GAME: self.init_game,
            Board.OPTIONS: self.init_options,
            Board.HISCORES: self.init_hiscores,
            Board.SETUP: self.init_setup,
            Board.HELP: self.init_help,
            Board.ABOUT: self.init_about,
            Board.QUIT: self.init_quit,
            Board.NEWSCORE: self.init_newscore
        }
        self.mode_initializers = {
            Mode.INIT: self.init_init,  # Yes.
            Mode.PREPARE: self.init_prepare,
            Mode.PLAY: self.init_play,
            Mode.PAUSED: self.init_paused,
            Mode.KILLED: self.init_killed,
            Mode.GAMEOVER: self.init_gameover,
            Mode.CONGRATS: self.init_congrats
        }
        self.setupmode_initializers = {
            SetupMode.DISPLAY: self.init_display,
            SetupMode.ENTER: self.init_enter
        }
        self.useractions = {}
        keys = self.config.db['keys']
        for key in keys:
            self.useractions[keys[key]] = key
        # Board-related
        self.menu_pos = 0
        # Options related
        self.options_pos = 1
        # Game settings:
        self.nick = ""
        # Game objects:
        self.iceboxes = []
        self.bombs = []
        self.lightballs = []
        self.medkits = []
        self.missiles = []
        self.firemissiles = []
        self.boss = None
        self.tnts = []
        self.tnt = 0
        self.shields = []
        self.meteorites = []
        self.drops = []
        self.explosions = []
        # Game-related:
        self.player_index = 0
        self.points = 750
        self.level = -1
        self.lives = 3
        self.indicators = 10
        self.stars = Star.from_factory(
            star_ids,
            self.shooter.images['star'])
        self.shield_timer = 0
        self.frozen_timer = 0
        self.lightball_timer = 0
        self.movable_factory = None
        self.movables = []
        self.get_ready_counter = 0
        self.get_ready = 3
        self.menu_rectangles = []
        self.options_rectangles = []
        self.lang_rectangles = []
        r = Rect(ARENA_WIDTH - 160, ARENA_HEIGHT - 60, 80, 60)
        self.lang_rectangles.append(r)
        r = Rect(ARENA_WIDTH - 80, ARENA_HEIGHT - 60, 80, 60)
        self.lang_rectangles.append(r)
        self.player_rectangles = []
        r = Rect(ARENA_WIDTH / 4 - self.shooter.images['icons']['prev'].width() / 2,
                 600 - self.shooter.images['icons']['prev'].height() / 2,
                 self.shooter.images['icons']['prev'].width(),
                 self.shooter.images['icons']['prev'].height())
        self.player_rectangles.append(r)
        r = Rect(ARENA_WIDTH / 2 - self.shooter.images['big_players'][self.player_index].width() / 2,
                 600 - self.shooter.images['big_players'][self.player_index].height() / 2,
                 self.shooter.images['big_players'][self.player_index].width(),
                 self.shooter.images['big_players'][self.player_index].height())
        self.player_rectangles.append(r)
        r = Rect(3 * ARENA_WIDTH / 4 - self.shooter.images['icons']['next'].width() / 2,
                 600 - self.shooter.images['icons']['next'].height() / 2,
                 self.shooter.images['icons']['next'].width(),
                 self.shooter.images['icons']['next'].height())
        self.player_rectangles.append(r)
        self.eventmanager = EventManager(self, self.shooter)
        self.enemymanager = EnemyManager(self, self.shooter)
        # Newscore
        self.newscore_counter = 0
        # Player related
        self.player = None
        self.player_xmove_counter = 0
        self.player_ymove_counter = 0
        # Bombs related
        self.bomb_lock = False
        # Missiles related
        self.missile_lock = False
        # Smoke related
        self.smoke_counter = 0

    def has_key_setup(self, key):
        return True if key in self.temp_setup else False

    def hiscores_append(self, name, points):
        self.config.add_hiscore(name, points)

    def is_hiscore(self, points):
        if len(self.config['hiscores']) < 10:
            return True
        if self.config['hiscores'][9][1] < points:
            return True
        return False

    def mousepress_welcome(self, event):
        pass

    def mousepress_player(self, event):
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.player_rectangles[0].contains(event.x, event.y):
            if self.player_index > 0:
                self.player_index -= 1
            return
        if self.player_rectangles[2].contains(event.x, event.y):
            if self.player_index < 3:  # TODO: const
                self.player_index += 1
            return
        if self.player_rectangles[1].contains(event.x, event.y):
            self.change_board(Board.GAME)

    def mousepress_menu(self, event):
        pos = 0
        for r in self.menu_rectangles:
            if r.contains(event.x, event.y):
                self.change_board(self.menupos2board[pos])
                return
            pos += 1
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()

    def mousepress_game(self, event):
        if self.mode in [Mode.GAMEOVER, Mode.CONGRATS]:
            if self.lang_rectangles[0].contains(event.x, event.y):
                self.config['lang'] = 'pl'
                self.update_menu_rectangles()
                self.update_options_rectangles()
                return
            if self.lang_rectangles[1].contains(event.x, event.y):
                self.config['lang'] = 'en'
                self.update_menu_rectangles()
                self.update_options_rectangles()

    def mousepress_options(self, event):
        pos = 0
        for r in self.options_rectangles:
            if r.contains(event.x, event.y):
                self.config['lastmode'] = self.optionspos2option[pos]
                self.change_board(Board.MENU)
                return
            pos += 1
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()

    def mousepress_hiscores(self, event):
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()
        else:
            self.change_board(Board.MENU)

    def mousepress_setup(self, event):
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()

    def mousepress_help(self, event):
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()
        else:
            self.change_board(Board.MENU)

    def mousepress_about(self, event):
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()
        else:
            self.change_board(Board.MENU)

    def mousepress_quit(self, event):
        pass

    def mousepress_newscore(self, event):
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.update_menu_rectangles()
            self.update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.update_menu_rectangles()
            self.update_options_rectangles()

    def mouse_pressed(self, event):
        self.mousepress_events[self.board](event)

    def update_menu_rectangles(self):
        self.menu_rectangles = []
        fm = self.arena.metrics['menu']
        c = 3
        for label in self.shooter.labels['menu'][self.config['lang']]:
            r = Rect(400, c * 100 - fm.height(), fm.horizontalAdvance(label), fm.height())
            self.menu_rectangles.append(r)
            c += 1

    def update_options_rectangles(self):
        self.options_rectangles = []
        fm = self.arena.metrics['options']
        c = 3
        for label in self.shooter.labels['options'][self.config['lang']]:
            r = Rect(400, c * 100 - fm.height(), fm.horizontalAdvance(label), fm.height())
            self.options_rectangles.append(r)
            c += 1

    def change_board(self, board, nextb=Board.NONE):
        self.next_board = nextb
        if board != self.board:
            self.board = board
            initializer = self.board_initializers[board]
            initializer()

    def change_mode(self, mode):
        if mode != self.mode:
            self.mode = mode
            initializer = self.mode_initializers[mode]
            initializer()

    def change_setup(self, setup):
        if self.setupmode != setup:
            self.setupmode = setup
            initializer = self.setupmode_initializers[setup]
            initializer()

    def init_player(self):
        pass

    def init_welcome(self):
        self.shooter.timers['welcome-event'].start(TIMEOUT_WELCOME)
        self.shooter.timers['paint-event'].start(TIMEOUT_PAINT)

    def __stop_timers(self):
        """
        Stop all game-related timers
        """
        for event in ["game-counter-event",
                      "movable-update-event",
                      "get-ready-event",
                      "game-update-event",
                      "setup-enter-event",
                      "enemies-event",
                      "game-events",
                      "game-shield-event",
                      "game-freeze-event",
                      "game-light-event",
                      "smoke-timer"
                      ]:
            self.shooter.timers[event].stop()

    def init_menu(self):
        self.player = None
        self.update_menu_rectangles()
        self.__stop_timers()
        self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
        self.shooter.timers['setup-enter-event'].stop()
        self.shooter.timers['player-move-event'].stop()

    def init_congrats(self):
        self.__stop_timers()
        self.shooter.timers['player-move-event'].stop()

    def init_game(self):
        self.change_mode(Mode.INIT)

    def init_options(self):
        self.options_pos = int(self.config['lastmode'])
        self.update_options_rectangles()

    def init_hiscores(self):
        self.shooter.timers['newscore-event'].stop()

    def init_setup(self):
        self.init_display()

    def init_about(self):
        pass

    def init_quit(self):
        self.config.save()
        self.arena.parent.close()

    def init_newscore(self):
        self.shooter.timers['newscore-event'].start(TIMEOUT_NEWSCORE)

    def init_display(self):
        pass

    def init_enter(self):
        self.temp_setup = [
            self.config.get_key(UserInput.LEFT),
            self.config.get_key(UserInput.RIGHT),
            self.config.get_key(UserInput.TOP),
            self.config.get_key(UserInput.BOTTOM),
            self.config.get_key(UserInput.FIRE),
            self.config.get_key(UserInput.BOMB),
            self.config.get_key(UserInput.TNT),
        ]
        self.temp_position = 0
        self.shooter.timers['setup-enter-event'].start(TIMEOUT_SETUP_ENTER)
        self.setup_counter = 0

    def init_init(self):
        self.points = 0
        self.level = -1
        self.lives = 3
        self.indicators = 10
        self.tnt = 3
        self.eventmanager = EventManager(self, self.shooter)
        self.enemymanager = EnemyManager(self, self.shooter)
        self.change_mode(Mode.PREPARE)
        self.shooter.timers['smoke-timer'].start(TIMEOUT_SMOKE)

    def init_prepare(self):
        if self.level < MAX_LEVEL:
            self.level += 1
        self.enemymanager.clear()
        self.enemymanager.set_level(self.level)
        self.eventmanager.set_level(self.level)
        self.medkits = []
        self.missiles = []
        self.firemissiles = []
        self.tnts = []
        self.shields = []
        self.shield_timer = 0
        self.frozen_timer = 0
        self.lightball_timer = 0
        self.lightballs = []
        self.drops = []
        self.iceboxes = []
        self.movable_factory = MovableType.get_from_factory(self.level)
        movs = []
        for i in range(0, 16):
            movs.append(next(self.movable_factory))
        self.movables = Movable.from_factory(movs,
                                             ARENA_WIDTH,
                                             self.shooter.images['movables'])
        if not self.player:
            self.player = Player(200, 400,
                                 self.shooter.images['players'][self.player_index])
        self.shooter.timers['player-move-event'].start(TIMEOUT_PLAYER_MOVE)
        self.shooter.timers['get-ready-event'].start(TIMEOUT_GET_READY)

    def init_play(self):
        self.game_counter = 0
        option = self.options_pos % 3
        timeout_ge = TIMEOUT_GAME_EVENTS - 100 * (option + self.level)
        timeout_ee = TIMEOUT_ENEMIES_EVENTS - 100 * (option + self.level)
        self.shooter.timers['game-update-event'].start(TIMEOUT_GAME_UPDATE)
        self.shooter.timers['game-counter-event'].start(TIMEOUT_GAME_COUNTER)
        self.shooter.timers['game-events'].start(timeout_ge)
        self.shooter.timers['enemies-event'].start(timeout_ee)
        self.shooter.timers['smoke-timer'].start(TIMEOUT_SMOKE)

    def init_paused(self):
        self.shooter.timers['game-update-event'].stop()
        self.shooter.timers['game-counter-event'].stop()
        self.shooter.timers['game-events'].stop()
        self.shooter.timers['enemies-event'].stop()
        self.shooter.timers['smoke-timer'].stop()

    def init_killed(self):
        """
        Perform all the actions needed when killed
        :return: None
        """
        self.__stop_timers()
        # No enemies while killed and waiting for RET key:
        self.enemymanager.clear()
        # Clear any event objects on the board:
        self.missiles = []
        self.tnts = []
        self.firemissiles = []
        self.medkits = []
        self.shields = []
        self.drops = []
        self.lightballs = []
        # Clear any other timers:
        self.lightball_timer = 0
        self.shield_timer = 0
        self.frozen_timer = 0

    def init_help(self):
        """
        Initial actions done when help (no actions)
        :return: None
        """
        pass

    def init_gameover(self):
        """
        Initial actions done when game over
        :return: None
        """
        self.__stop_timers()
        self.shooter.timers['player-move-event'].stop()

    def keyrelease_player(self, key, _):
        if key == Key.KEY_Q or key == Key.KEY_ESCAPE:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.change_board(Board.GAME)
        elif key == Key.KEY_LEFT:
            if self.player_index > 0:
                self.player_index -= 1
        elif key == Key.KEY_RIGHT:
            if self.player_index < 3:  # TODO: const
                self.player_index += 1

    def keyrelease_congrats(self, key, _):
        if key in [Key.KEY_ESCAPE, Key.KEY_Q]:
            if self.is_hiscore(self.points):
                self.change_board(Board.NEWSCORE)
            else:
                self.change_board(Board.HISCORES)

    def keyrelease_welcome(self, _k, _t):
        self.change_board(Board.MENU)

    def keyrelease_menu(self, key, _):
        if key == Key.KEY_Q:
            self.change_board(Board.QUIT)
        elif key == Key.KEY_TOP:
            if self.menu_pos > 0:
                self.menu_pos -= 1
        elif key == Key.KEY_BOTTOM:
            if self.menu_pos < len(self.shooter.labels['menu']['en']) - 1:
                self.menu_pos += 1
        elif key == Key.KEY_ENTER:
            self.change_board(self.menupos2board[self.menu_pos])

    def keyrelease_game(self, key, _):
        handler = self.keyreleasegame_events[self.mode]
        handler(key, None)

    def keyrelease_options(self, key, _):
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_TOP:
            if self.options_pos > 0:
                self.options_pos -= 1
        elif key == Key.KEY_BOTTOM:
            if self.options_pos < len(self.shooter.labels['options']['en']) - 1:
                self.options_pos += 1
        elif key == Key.KEY_ENTER:
            self.config['lastmode'] = self.optionspos2option[self.options_pos]
            self.change_board(Board.MENU)

    def keyrelease_hiscores(self, key, _):
        """
        Handle heyrelease when in HiScores board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(Board.MENU)

    def keyrelease_prepare(self, key, _):
        """
        Handle keyrelease when in Prepare board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)

    def keyrelease_setup(self, key, _):
        if key:
            if self.setupmode == SetupMode.DISPLAY:
                if key in [Key.KEY_Q, Key.KEY_ESCAPE]:
                    self.change_board(Board.MENU)
                elif key == Key.KEY_F1:
                    self.change_setup(SetupMode.ENTER)
            elif self.setupmode == SetupMode.ENTER:
                if key == Key.KEY_ENTER:
                    self.config.set_key(UserInput.LEFT, self.temp_setup[0])
                    self.config.set_key(UserInput.RIGHT, self.temp_setup[1])
                    self.config.set_key(UserInput.TOP, self.temp_setup[2])
                    self.config.set_key(UserInput.BOTTOM, self.temp_setup[3])
                    self.config.set_key(UserInput.FIRE, self.temp_setup[4])
                    self.config.set_key(UserInput.BOMB, self.temp_setup[5])
                    self.config.set_key(UserInput.TNT, self.temp_setup[6])
                    self.config.save()
                    self.useractions = {}
                    keys = self.config.db['keys']
                    for key in keys:
                        self.useractions[keys[key]] = key
                    self.change_setup(SetupMode.DISPLAY)
                elif key == Key.KEY_ESCAPE:
                    # Nie przepisywać klawszy
                    self.change_setup(SetupMode.DISPLAY)
                elif key.is_move():
                    if not self.has_key_setup(key):
                        if self.temp_position <= 6:
                            self.temp_setup[self.temp_position] = key
                            self.temp_position += 1
                            if self.temp_position > 6:
                                self.temp_position = 6

    def keyrelease_about(self, key, _):
        """
        Key handler for ABOUT board.
        :param key: key to handle
        :param _: unused
        :return: None
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(Board.MENU)

    def keyrelease_quit(self, _k, _t):
        """
        Key handler for QUIT board
        :param _k: unused
        :param _t: unused
        :return: None
        """
        self.arena.parent.close()

    def keyrelease_newscore(self, key, _t):
        if key:
            if key == Key.KEY_ESCAPE:
                self.change_board(Board.HISCORES)
            elif key == Key.KEY_BACKSPACE:
                if len(self.nick) > 0:
                    self.nick = self.nick[:-1]
            elif key > Key.KEY_SPACE:
                if len(self.nick) < MAX_NICK_LEN:
                    self.nick += str(key)
                else:
                    n = list(self.nick)
                    n[MAX_NICK_LEN - 1] = str(key)
                    self.nick = "".join(n)
            elif key == Key.KEY_ENTER:
                if len(self.nick) > 0:
                    self.config.add_hiscore(self.nick, self.points)
                self.change_board(Board.HISCORES)

    def keyrelease_init(self, key, _):
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)

    def keyrelease_play(self, key, _):
        if key == Key.KEY_Q:
            self.__stop_timers()
            self.change_board(Board.MENU)
        elif key == Key.KEY_ESCAPE:
            self.shooter.timers['movable-update-event'].stop()
            self.shooter.timers['stars-update-event'].stop()
            self.change_mode(Mode.PAUSED)
        elif key in self.useractions:
            action = self.useractions[key]
            if action == UserInput.TOP:
                if self.player.y > 20:
                    self.player_ymove_counter = PLAYER_YMOVE_REPEAT
            elif action == UserInput.BOTTOM:
                if self.player.y < ARENA_HEIGHT - BOTTOM_BAR - self.player.height - 20:
                    self.player_ymove_counter = -PLAYER_YMOVE_REPEAT
            elif action == UserInput.RIGHT:
                if self.player.x < ARENA_WIDTH - self.player.width - 20:
                    self.player_xmove_counter = -PLAYER_XMOVE_REPEAT
            elif action == UserInput.LEFT:
                if self.player.x > 20:
                    self.player_xmove_counter = PLAYER_XMOVE_REPEAT
            elif action == UserInput.FIRE:
                if self.lightball_timer > 0:
                    self.create_firemissile(
                        self.player.x + self.player.w,
                        self.player.y + self.player.h // 2)
                else:
                    self.create_missile(
                        self.player.x + self.player.w,
                        self.player.y + self.player.h // 2,
                        MissileType.FROM)
            elif action == UserInput.BOMB:
                self.create_bomb(
                    self.player.x + self.player.w // 4,
                    self.player.y + self.player.h)
            elif action == UserInput.TNT:
                self.explode_tnt()

    def keyrelease_paused(self, key, _):
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
            self.change_mode(Mode.PLAY)

    def keyrelease_killed(self, key, _):
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.process_killed()
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
            self.change_mode(Mode.PLAY)

    def keyrelease_help(self, key, _):
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(Board.MENU)

    def keyrelease_gameover(self, key, _text):
        """
        Key release handler for Mode.GAMEOVER
        :param key: Released key
        :param _text: Entered text (not used)
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(
                Board.NEWSCORE if self.config.is_hiscore(
                    self.points) else Board.HISCORES)

    def process_killed(self):
        if self.lives > 0:
            self.indicators = 10
        self.__stop_timers()
        self.enemymanager.clear()
        self.missiles = []
        self.medkits = []
        self.shields = []
        self.tnts = []
        self.lightballs = []
        self.drops = []
        self.iceboxes = []
        self.explosions = []

    def game_paint_event(self):
        self.arena.paint()

    def keypress_player(self, key, _):
        pass

    def keypress_welcome(self, key, _):
        pass

    def keypress_menu(self, key, _):
        pass

    def keypress_game(self, key, _):
        pass

    def keypress_options(self, key, _):
        pass

    def keypress_hiscores(self, key, _):
        pass

    def keypress_setup(self, key, _):
        pass

    def keypress_about(self, key, _):
        pass

    def keypress_quit(self, key, _):
        pass

    def keypress_newscore(self, key, _):
        pass

    def keypress_init(self, key, _):
        pass

    def keypress_play(self, key, _):
        pass

    def keypress_paused(self, key, _):
        pass

    def keypress_killed(self, key, _):
        pass

    def keypress_help(self, key, _):
        pass

    def keypress_gameover(self, key, _):
        pass

    def stars_update_event(self):
        for star in self.stars:
            star.move()

    def welcome_event(self):
        if self.counter['welcome'] > 0:
            self.counter['welcome'] -= 1
        else:
            self.shooter.timers['welcome-event'].stop()
            self.change_board(Board.MENU)

    def game_counter_event(self):
        self.game_counter += 1

    def game_freeze_event(self):
        pass

    def add_movable(self):
        """
        Append new movable from generator
        :return: None
        """
        last = self.movables[-1]
        x = last.x + last.image.width()  # no spacing, as requested
        new_type = next(self.movable_factory)
        new_movable = Movable(x,
                              self.shooter.images['movables'][new_type],
                              new_type)
        self.movables.append(new_movable)

    def movable_update_event(self):
        for movable in self.movables:
            movable.move()
        if not self.movables[0].is_valid():
            self.movables.pop(0)
            self.add_movable()

    def get_ready_event(self):
        if self.get_ready > 0:
            self.get_ready -= 1
        else:
            self.shooter.timers['get-ready-event'].stop()
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.change_mode(Mode.PLAY)

    def keypressed(self, key, _):
        handler = self.keypress_events[self.board]
        handler(key, None)

    def keyreleased(self, key, _):
        self.keyrelease_events[self.board](key, None)

    def create_missile(self, x, y, etype):
        if not self.missile_lock:
            self.missile_lock = True
            self.shooter.timers['missile-timer'].start(TIMEOUT_MISSILE_LOCK)
            image = self.shooter.images['missiles'][etype]
            m = Missile(x, y, etype, image)
            self.missiles.append(m)

    def game_update_event(self):
        # Missiles
        for missile in self.missiles:
            missile.move()
        for firemissile in self.firemissiles:
            firemissile.move()
        # IceBoxes:
        for icebox in self.iceboxes:
            icebox.move()
        # Bombs
        for bomb in self.bombs:
            bomb.move()
        # Medkids
        for medkit in self.medkits:
            medkit.move()
        # LightBalls
        for lightball in self.lightballs:
            lightball.move()
        # TNTs
        for tnt in self.tnts:
            tnt.move()
        # Shields
        for shield in self.shields:
            shield.move()
        # Enemies
        if self.frozen_timer == 0:
            self.enemymanager.move()
        # Meteorites
        for meteorite in self.meteorites:
            meteorite.move()
        # Drops
        for drop in self.drops:
            drop.move()
        for explosion in self.explosions:
            explosion.move()
        self.explosions = [x for x in self.explosions if x.is_valid()]
        self.check_collision_shield()
        self.check_collision_medkit()
        self.check_collision_tnt()
        self.check_collision_missiles()
        self.check_collision_drops()
        self.check_collision_enemies()
        self.check_collision_lightball()
        self.check_collision_icebox()
        self.check_collision_bomb()
        self.check_collision_movables()

    def enemies_event(self):
        if not self.enemymanager.run():
            if self.level == MAX_LEVEL:
                # TODO
                # Boss is killed, do some animation here?
                if self.lives == 0:
                    self.change_mode(Mode.GAMEOVER)
                else:
                    self.change_mode(Mode.CONGRATS)
            else:
                self.change_mode(Mode.PREPARE)

    def events_event(self):
        self.eventmanager.run()

    def setup_enter_event(self):
        self.setup_counter += 1

    def check_collision_drops(self):
        """
        Check if any of the drop collided a player - only in normal and hard mode
        and perform an action:
        * if not shield/unlimited mode explode player
        * if not shield/unlimited mode decrease indicator points
        """
        if self.shield_timer == 0 and self.options_pos not in (Options.EASY, Options.UNLIMITED):
            for drop in self.drops:
                if drop.collides(self.player):
                    drop.valid = False
                    self.explode(
                        self.player.x + self.player.w // 2,
                        self.player.y + self.player.h // 2)
                    self.drops = [x for x in self.drops if x.is_valid()]
                    self.decrease_hp()

    def check_collision_missiles(self):
        for missile in self.missiles:
            if missile.etype == MissileType.FROM and missile.is_valid():
                for enemy in self.enemymanager.enemies:
                    if missile.collides(enemy):
                        enemy.valid = False
                        missile.valid = False
                        self.explode(enemy.x + enemy.w // 2,
                                     enemy.y + enemy.h // 2)
                        self.points += 1
                        self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
                        self.missiles = [x for x in self.missiles if x.is_valid()]
                for movable in self.movables:
                    if movable.is_valid() and movable.etype == MovableType.DZIALO and movable.collides(missile):
                        movable.valid = False
                        self.points += 1
                        self.explode(movable.x + movable.w // 2,
                                     movable.y + movable.h // 2)
                        self.movables = [x for x in self.movables if x.is_valid()]
                        self.add_movable()
                        self.missiles = [x for x in self.missiles if x.is_valid()]
            elif missile.etype in [MissileType.TO,
                                   MissileType.TO_NWW,
                                   MissileType.TO_SWW,
                                   MissileType.TO_NW] and missile.is_valid():
                if self.shield_timer == 0 and self.options_pos != Options.UNLIMITED:
                    if missile.collides(self.player):
                        missile.valid = False
                        self.explode(self.player.x + self.player.w // 2,
                                     self.player.y + self.player.h // 2)
                        self.missiles = [x for x in self.missiles if x.is_valid()]
                        self.decrease_hp()
        for fireball in self.firemissiles:
            for enemy in self.enemymanager.enemies:
                if enemy.is_valid() and fireball.collides(enemy):
                    enemy.valid = False
                    fireball.valid = False
                    self.points += 1
                    self.explode(enemy.x + enemy.w // 2,
                                 enemy.y + enemy.h // 2)
                    self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
                    self.firemissiles = [x for x in self.firemissiles if x.is_valid()]
            for movable in self.movables:
                if movable.is_valid() and movable.etype == MovableType.DZIALO and fireball.collides(movable):
                    movable.valid = False
                    self.points += 1
                    self.explode(movable.x + movable.w // 2,
                                 movable.y + movable.h // 2)
                    self.movables = [x for x in self.movables if x.is_valid()]
                    self.add_movable()
                    self.firemissiles = [x for x in self.firemissiles if x.is_valid()]
        if self.enemymanager.boss:
            for missile in self.missiles:
                if missile.etype == MissileType.FROM and missile.is_valid():
                    if self.enemymanager.boss.collides(missile):
                        self.enemymanager.boss.decrease_hp()

    def decrease_hp(self):
        """
        Decrease indicator points when collided by an object
        :return: None
        """
        if self.indicators > 0:
            self.indicators -= 1
        if self.indicators == 0:
            self.lives -= 1
            if self.lives <= 0:  # In case of two timers did the lives < 0
                self.change_mode(Mode.GAMEOVER)
            else:
                self.process_killed()
                self.change_mode(Mode.KILLED)

    def increase_hp(self):
        """
        Increase indicator points (when medkit caught)
        :return: None
        """
        if self.indicators < 10:
            self.indicators += 1

    def check_collision_enemies(self):
        """
        Check if player collides with any enemy, then do the action:
        * explode enemy,
        * increase game points,
        * if not unlimited mode/frozen/shield, decrease indicator points
        :return: None
        """
        for enemy in self.enemymanager.enemies:
            if enemy.collides(self.player):
                self.points += 1
                enemy.valid = False
                self.explode(enemy.x + enemy.w // 2,
                             enemy.y + enemy.h // 2)
                self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
                if self.shield_timer == 0 and self.frozen_timer == 0 and self.options_pos != Options.UNLIMITED:
                    self.decrease_hp()

    def check_collision_movables(self):
        """
        Check if player collided with a movable: only hardcore mode.
        Action:
        * increase game points
        * decrease HP
        * explode building
        :return: None
        """
        if self.options_pos == Options.HARD:
            for movable in self.movables:
                if movable.collides(self.player):
                    self.points += 1
                    movable.valid = False
                    self.explode(movable.x + movable.w // 2,
                                 movable.y + movable.h // 2)
                    self.movables = [x for x in self.movables if x.is_valid()]
                    self.decrease_hp()

    def explode(self, x, y):
        """
        Create new explosion and append to all explosions list
        :param x: X coordinate of explosion
        :param y: Y coordinate of explosion
        :return: None
        """
        self.explosions.append(
            Explosion(
                x, y, self.shooter.images['explosions']))

    def explode_tnt(self):
        if self.tnt > 0 and len(self.enemymanager.enemies) > 0:
            for i in range(0, 3):
                try:
                    enemy = self.enemymanager.enemies[i]
                    self.explode(enemy.x + enemy.w // 2,
                                 enemy.y + enemy.h // 2)
                    enemy.valid = False
                except IndexError:
                    pass
            self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
            self.tnt -= 1

    def check_collision_medkit(self):
        """
        Check collision with medkits -- collect health points
        """
        for medkit in self.medkits:
            if medkit.collides(self.player):
                medkit.valid = False
                self.increase_hp()
        self.medkits = [x for x in self.medkits if x.is_valid()]

    def check_collision_shield(self):
        """
        Check collision with shields -- collect a shield
        (remove all remaining shields if any)
        """
        for shield in self.shields:
            if shield.collides(self.player):
                self.shield_timer = SHIELD_TIMER
                self.shields = []
                self.shooter.timers['game-shield-event'].start(TIMEOUT_SHIELD)

    def check_collision_tnt(self):
        """
        Check collision with TNT -- collect a TNT
        """
        for tnt in self.tnts:
            if tnt.collides(self.player):
                self.tnt += 1
                tnt.valid = False
        self.tnts = [x for x in self.tnts if x.is_valid()]

    def check_collision_lightball(self):
        """
        Check collision with lightball -- enter LightBall mode
        (3 missiles in a single shot)
        """
        for lb in self.lightballs:
            if lb.collides(self.player):
                self.lightball_timer = 10
                lb.valid = False
                self.lightballs = []
                self.shooter.timers['game-light-event'].start(TIMEOUT_LIGHT)

    def check_collision_icebox(self):
        for icebox in self.iceboxes:
            if icebox.collides(self.player):
                icebox.valid = False
                self.frozen_timer = 10
                self.iceboxes = []
                self.missiles = []  # If frozen mode, no missiles shall be present.
                self.shooter.timers['game-freeze-event'].start(TIMEOUT_FREEZE)

    def check_collision_bomb(self):
        for bomb in self.bombs:
            for movable in self.movables:
                if movable.is_valid() and bomb.collides(movable):
                    self.explode(movable.x + movable.w // 2, movable.y + movable.h // 2)
                    bomb.valid = False
                    movable.valid = False
                    self.add_movable()
                    self.points += 1
            for enemy in self.enemymanager.enemies:
                if enemy.is_valid() and bomb.collides(enemy):
                    self.explode(enemy.x + enemy.w // 2, enemy.y + enemy.h // 2)
                    enemy.valid = False
                    bomb.valid = False
                    self.points += 1
        self.movables = [x for x in self.movables if x.is_valid()]
        self.bombs = [x for x in self.bombs if x.is_valid()]

    def create_bomb(self, x, y):
        """
        Create bomb at given location
        (and start bomb timer)
        :param x: X coordinate of the bomb
        :param y: Y coordinate of the bomb
        :return: None
        """
        if not self.bomb_lock:
            self.bomb_lock = True
            self.bombs.append(
                Bomb(x, y, self.shooter.images['indicators']['bomb']))
            self.shooter.timers['bomb-timer'].start(TIMEOUT_BOMB_LOCK)

    def shield_event(self):
        if self.shield_timer > 0:
            self.shield_timer -= 1
        else:
            self.shooter.timers['game-shield-event'].stop()

    def light_event(self):
        if self.lightball_timer > 0:
            self.lightball_timer -= 1
        else:
            self.shooter.timers['game-light-event'].stop()

    def freeze_event(self):
        """
        Handle freeze event
        (decrease timer or expire freeze)
        :return: None
        """
        if self.frozen_timer > 0:
            self.frozen_timer -= 1
        else:
            self.shooter.timers['game-freeze-event'].stop()

    def create_firemissile(self, x, y):
        """
        Create fire missile, which in fact contains 3 fireballs
        :param x: initial X position of firemissile
        :param y: initial Y position of firemissile
        :return: None
        """
        if not self.missile_lock:
            self.missile_lock = True
            self.shooter.timers['missile-timer'].start(TIMEOUT_MISSILE_LOCK)
            f = FireMissile(x,
                            y,
                            FireballDirection.UP,
                            self.shooter.images['indicators']['light-ball'])
            self.firemissiles.append(f)
            f = FireMissile(x,
                            y,
                            FireballDirection.STRAIGHT,
                            self.shooter.images['indicators']['light-ball'])
            self.firemissiles.append(f)
            f = FireMissile(x,
                            y,
                            FireballDirection.DOWN,
                            self.shooter.images['indicators']['light-ball'])
            self.firemissiles.append(f)

    def newscore_event(self):
        """
        Handle newscore event
        (cursor blinking)
        :return: None
        """
        self.newscore_counter = 0 if self.newscore_counter == 1 else 1

    def player_move_event(self):
        """
        Handle player event
        (smooth moving in every direction
        :return: None
        """
        if self.player:
            if self.player_ymove_counter > 0:
                self.player.go_up()
                self.player_ymove_counter -= 1
            elif self.player_ymove_counter < 0:
                self.player.go_down()
                self.player_ymove_counter += 1
            if self.player_xmove_counter > 0:
                self.player.go_left()
                self.player_xmove_counter -= 1
            elif self.player_xmove_counter < 0:
                self.player.go_right()
                self.player_xmove_counter += 1

    def bomb_timer(self):
        """
        Handle bomb timer
        (disallow creating too many bombs at once)
        :return:
        """
        self.bomb_lock = False

    def missile_timer(self):
        """
        Handle missile timer
        (disallow creating too many missiles at once)
        :return:
        """
        self.missile_lock = False

    def smoke_timer(self):
        """
        Handle smoke timer
        (rorate smoke frame)
        :return:
        """
        self.smoke_counter += 1
        self.smoke_counter %= 4
