#!/usr/bin/env python

"""
Game managers
"""


import math
import random
from spaceshooter.stypes import MovableType, MissileType
from spaceshooter.primi import Tnt, Drop, Missile, Medkit,\
    IceBox, Enemy, LightBall, Boss, Shield
from spaceshooter.sdefs import MAX_EVENTS_FACTOR, ARENA_WIDTH,\
    ARENA_HEIGHT, STAGE_HEIGHT, MAX_LEVEL
from spaceshooter.sevents import GameEvent, EnemyEvent
from spaceshooter.sutils import cycle


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
            GameEvent.DROP: self.__create_drop,
            GameEvent.DROPS: self.__create_drops,
            GameEvent.MISSILES: self.__create_missiles,
            GameEvent.MISSILES_ODD: self.__create_missiles_odd,
            GameEvent.MISSILES_EVEN: self.__create_missiles_even,
            GameEvent.MEDKIT: self.__create_medkit,
            GameEvent.FREEZE: self.__create_freeze,
            GameEvent.LIGHTBALL: self.__create_lightball,
            GameEvent.SHIELD: self.__create_shield,
            GameEvent.TNT: self.__create_tnt,
            GameEvent.GUN_MISSILE: self.__create_gun_missiles
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

    def __create_tnt(self):
        """
        Create a single, random TNT box
        """

        self.parent.tnts.append(
            Tnt(
                ARENA_WIDTH,
                random.randint(150, 3 * ARENA_HEIGHT // 4),
                self.shooter.images['indicators']['tnt']))

    def __create_drop(self):
        """
        Create a single, random drop
        """
        self.parent.drops.append(
            Drop(
                random.randint(ARENA_WIDTH // 3, ARENA_WIDTH),
                0,
                self.shooter.images['indicators']['drop']))

    def __create_drops(self):
        """
        Create two random drops
        """
        self.parent.drops.append(
            Drop(
                random.randint(ARENA_WIDTH // 3, 2 * ARENA_WIDTH // 3),
                0,
                self.shooter.images['indicators']['drop']))
        self.parent.drops.append(
            Drop(
                random.randint(2 * ARENA_WIDTH // 3, ARENA_WIDTH),
                0,
                self.shooter.images['indicators']['drop']))

    def __create_gun_missiles(self):
        """
        Create gun missiles for every visible gun, (if not in frozen mode)
        :return: None
        """
        if self.parent.frozen_timer == 0:
            for movable in self.parent.movables:
                if movable.is_valid() and movable.etype == MovableType.DZIALO:
                    image = self.shooter.images['missiles'][MissileType.TO_NW]
                    self.parent.missiles.append(
                        Missile(movable.x - image.width(),
                                movable.y - image.height(),
                                MissileType.TO_NW,
                                image))

    def __create_missiles(self):
        """
        Create missiles for all enemies
        :return: None
        """
        if len(self.parent.enemymanager.enemies) > 0 and self.parent.frozen_timer == 0:
            image = self.shooter.images['missiles'][MissileType.TO]
            w = image.width()
            h = image.height()
            for enemy in self.parent.enemymanager.enemies:
                self.parent.missiles.append(
                    Missile(enemy.x - w,
                            enemy.y - h // 2,
                            MissileType.TO,
                            image))

    def __create_missiles_even(self):
        """
        Create missiles for even enemies
        :return: None
        """
        if len(self.parent.enemymanager.enemies) > 0 and self.parent.frozen_timer == 0:
            image = self.shooter.images['missiles'][MissileType.TO]
            w = image.width()
            h = image.height()
            for enemy in self.parent.enemymanager.enemies:
                if not enemy.odd:
                    self.parent.missiles.append(
                        Missile(enemy.x - w,
                                enemy.y - h // 2,
                                MissileType.TO,
                                image))

    def __create_missiles_odd(self):
        """
        Create missiles for odd enemies
        :return: None
        """
        if len(self.parent.enemymanager.enemies) > 0 and self.parent.frozen_timer == 0:
            image = self.shooter.images['missiles'][MissileType.TO]
            w = image.width()
            h = image.height()
            for enemy in self.parent.enemymanager.enemies:
                if enemy.odd:
                    self.parent.missiles.append(
                        Missile(enemy.x - w,
                                enemy.y - h // 2,
                                MissileType.TO,
                                image))

    def __create_medkit(self):
        """
        Create new medkit and append to list of all medkits
        :return: None
        """
        self.parent.medkits.append(
            Medkit(ARENA_WIDTH,
                   random.randint(250, 3 * ARENA_HEIGHT // 4),
                   self.shooter.images['indicators']['medkit']))

    def __create_freeze(self):
        """
        Create new icebox and append to list of all iceboxes
        :return: None
        """
        self.parent.iceboxes.append(
            IceBox(ARENA_WIDTH,
                   random.randint(150, 3 * ARENA_HEIGHT // 4),
                   self.shooter.images['indicators']['frozen-box']))

    def __create_lightball(self):
        """
        Create random LightBall object
        :return: None
        """
        self.parent.lightballs.append(
            LightBall(ARENA_WIDTH,
                      random.randint(150, 3 * ARENA_HEIGHT // 4),
                      self.shooter.images['indicators']['light-ball']))

    def __create_shield(self):
        """
        Create random Shield object
        :return: None
        """
        self.parent.shields.append(
            Shield(ARENA_WIDTH,
                   random.randint(150, 3 * ARENA_HEIGHT // 4),
                   self.shooter.images['indicators']['shield']))

    def run(self):
        """
        Process event queue
        :return: None
        """
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
        """
        Create manager instance
        :param parent: Manager parent handle (game)
        :param shooter: Shooter handle
        """
        self.enemies = []
        self.parent = parent
        self.shooter = shooter
        self.boss = None
        self.images = self.shooter.images['enemies']
        self.imagen = cycle(self.images)
        self.etype = EnemyEvent.NONE
        self.level = 0
        self.eventq = []
        self.creates = {
            EnemyEvent.CIRCLE: self.__create_circle,
            EnemyEvent.SQUARE: self.__create_square,
            EnemyEvent.FRONTBACK: self.__create_frontback,
            EnemyEvent.UPDOWN: self.__create_updown,
            EnemyEvent.SINE: self.__create_sine,
            EnemyEvent.WAVE: self.__create_wave
        }
        self.moves = {
            EnemyEvent.CIRCLE: self.__move_circle,
            EnemyEvent.SQUARE: self.__move_square,
            EnemyEvent.FRONTBACK: self.__move_frontback,
            EnemyEvent.UPDOWN: self.__move_updown,
            EnemyEvent.SINE: self.__move_sine,
            EnemyEvent.WAVE: self.__move_wave
        }

    def set_level(self, level: int):
        """
        Set level and recalculate queue
        :param level: Level number
        :return: None
        """
        self.level = level
        iterations = 12 + self.level + self.parent.options_pos
        self.eventq = EnemyEvent.from_factory(level, iterations)

    def pop(self) -> EnemyEvent:
        """
        Pop an event to process
        :return: EnemyEvent
        """
        return self.eventq.pop(0)

    def clear(self):
        """
        Clear all enemies and the boss
        :return: None
        """
        self.enemies = []
        self.boss = None

    def __create_frontback(self):
        """
        Create enemies set with a front-back scheme
        :return: None
        """
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            a_x = 400 if odd else 0
            enemy = Enemy(
                ARENA_WIDTH - 650 + a_x,
                150 + i * 80 - (0 if odd else 60),
                odd,
                image,
                speedx=-10,
                speedy=2)
            self.enemies.append(enemy)

    def __create_circle(self):
        """
        Create enemies set with a circle scheme
        :return: None
        """
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

    def __create_square(self):
        """
        Create enemies set with a square scheme
        :return: None
        """
        image = next(self.imagen)
        for i in range(8):
            odd = (i % 2) == 0
            a_x = 250 if odd else 0
            enemy = Enemy(
                ARENA_WIDTH - 550 + a_x,
                150 + i * 80,
                odd,
                image,
                speedx=-8,
                speedy=8)
            self.enemies.append(enemy)

    def __create_updown(self):
        """
        Create enemies set with an up-down scheme
        :return: None
        """
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

    def __create_sine(self):
        """
        Create enemies set with a sine scheme
        :return: None
        """
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

    def __create_wave(self):
        """
        Create enemies set with a wave scheme
        :return: None
        """
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

    def __create_boss(self):
        """
        Create the boss
        :return: None
        """
        self.boss = Boss((2 * ARENA_WIDTH) // 3,
                         random.randint(5, STAGE_HEIGHT - 100),
                         self.shooter.images['boss'])

    def create_boss_missiles(self):
        """
        Create boss missiles (3: TO, SWW, NWW)
        :return: None
        """
        fixed_height = 32
        for etype in [MissileType.TO, MissileType.TO_SWW, MissileType.TO_NWW]:
            image = self.shooter.images['missiles'][etype]
            self.parent.missiles.append(
                Missile(
                    self.boss.x - image.width(),
                    self.boss.y + fixed_height - image.height() // 2,
                    etype,
                    image))

    def __move_circle(self):
        """
        Move enemies according to circle scheme
        :return: None
        """
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

    def __move_square(self):
        """
        Move enemies according to square scheme
        :return: None
        """
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

    def __move_frontback(self):
        """
        Move enemies according to front-back scheme
        :return: None
        """
        for enemy in self.enemies:
            enemy.x += enemy.speedx * enemy.dx
            enemy.y += enemy.speedy * enemy.dy
            if enemy.moved in (0, 30):
                enemy.dy = -enemy.dy
            elif enemy.moved in (15, 45):
                enemy.dx = -enemy.dx
            enemy.moved += 1
            enemy.moved %= 60
            enemy.x -= 2
            if enemy.x + enemy.w < 0:
                enemy.valid = False
        self.enemies = [x for x in self.enemies if x.is_valid()]

    def __move_updown(self):
        """
        Move enemies according to up-down scheme
        :return: None
        """
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

    def __move_sine(self):
        """
        Move enemies according to sine scheme
        :return: None
        """
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

    def __move_wave(self):
        """
        Move enemies according to wave scheme
        :return: None
        """
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
        """
        Process enemy queue
        :return: None
        """
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
                    self.__create_boss()
                else:
                    if self.boss.is_alive():
                        self.create_boss_missiles()
                    else:
                        return False
        return True

    def paint(self, painter):
        """
        Common painter aggregator
        :param painter: Painter to draw by
        :return: None
        """
        for enemy in self.enemies:
            enemy.paint(painter)
        if self.boss:
            self.boss.paint(painter)
