#!/usr/bin/env python

"""
Primitive definitions
"""

import math
import random
from sdefs import *
from stypes import (
    MovableType,
    MissileType,
    FireballDirection
)


class Rect:
    """
    Generic rectangle class
    """
    def __init__(self, x, y, w, h):
        """
        Create rectangle
        :param x: top x coordinate
        :param y: top y coordinate
        :param w: width
        :param h: height
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, x, y):
        """
        Check if rectangle contains a point
        :param x: point x coordinate
        :param y: point y coordinate
        :return: None
        """
        if self.x <= x <= self.x + self.w:
            if self.y <= y <= self.y + self.h:
                return True
        return False

    def set_size(self, w, h):
        """
        Set new size
        :param w: new width
        :param h: new height
        :return: None
        """
        if w > 0:
            self.w = w
        if h > 0:
            self.h = h

    def move_to(self, x, y):
        """
        Move to a specific location
        :param x: specific location x
        :param y: specific location y
        :return: None
        """
        self.x = x
        self.y = y

    def move_by(self, dx, dy):
        """
        Move by a specific distance
        :param dx: distance length
        :param dy: distance height
        :return:
        """
        self.x += dx
        self.y += dy

    def move(self):
        """
        Abstract method
        :return: None
        """

    def collides(self, r):
        """
        Check if collides with another rectangle
        :param r: Rectangle to check
        :return: True if collides, false otherwise
        """
        if r is not None:
            if self.x >= r.x + r.w or self.x + self.w <= r.x:
                return False
            if self.y >= r.y + r.h or self.y + self.h <= r.y:
                return False
            return True
        return False


class ImageRect(Rect):
    """
    Rectangle with associated image
    """
    def __init__(self, x, y, image):
        """
        Create object
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param image: associated image
        """
        super().__init__(x, y, -1, -1)
        self.image = image
        if image is not None:
            self.set_size(image.width(), image.height())

    def paint(self, painter):
        """
        Paint object on a bitmap
        :param painter: bitmap to paint
        :return: None
        """
        painter.drawPixmap(self.x, self.y, self.image)


class Movable(ImageRect):
    """
    Object that moves together with terrain and stars
    (house, skyscraper, factory, gun, etc)
    """

    def __init__(self, x, image, etype: MovableType, speed=MOVABLE_SPEED):
        """
        Create an object
        :param x: bottom left x position
        :param image: associated image
        :param etype: type of a movable
        :param speed: object speed
        """
        super().__init__(x, -1, image)
        self.etype = etype
        self.image = image
        self.speed = speed
        self.valid = True
        if image is not None:
            # Movables are aligned to bottom pane
            self.set_size(image.width(), image.height())
            self.y = STAGE_HEIGHT - self.h

    def move(self):
        """
        Move object according to its policy
        :return: None
        """
        self.x -= self.speed
        if self.x + self.w < 0:
            self.valid = False

    def is_valid(self):
        """
        Check if object shall still exist
        :return: True if object shall exist, False otherwise
        """
        return self.valid

    @staticmethod
    def from_factory(movs: list, width, imagelist):
        """
        Create movable list from factory
        :param movs: movable scenario list
        :param width:
        :param imagelist:
        :return:
        """
        movables = []
        if len(movs) > 0:
            x, i = 0, 0
            while x < 2 * width:
                m = Movable(x, imagelist[movs[i]], movs[i], MOVABLE_SPEED)
                x += m.image.width()  # One next to each other, as requested, no space left
                i += 1
                if i > len(movs) - 1:
                    i = 0
                movables.append(m)
        return movables


class FlyingObject(ImageRect):
    """
    Generic object than can fly around the arena
    """
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.valid = True

    def is_valid(self):
        """
        Check if object is valid
        :return:
        """
        return self.valid

    def move_to(self, x, y):
        """
        Move object to specific location
        :param x: X coordinate of the new location
        :param y: Y coordinate of the new location
        :return: None
        """
        self.x = x
        self.y = y
        if self.x + self.w < 0:
            self.valid = False
        elif self.x > ARENA_WIDTH:
            self.valid = False
        elif self.y + self.h < 0:
            self.valid = False
        elif self.y > ARENA_HEIGHT:
            self.valid = False

    def move_by(self, dx, dy):
        """
        Move object by a specific distance
        :param dx: Distance width
        :param dy: Distance height
        :return: None
        """
        self.x += dx
        self.y += dy
        if self.x + self.w < 0:
            self.valid = False
        elif self.x > ARENA_WIDTH:
            self.valid = False
        elif self.y + self.h < 0:
            self.valid = False
        elif self.y > ARENA_HEIGHT:
            self.valid = False


class Player(FlyingObject):
    """
    Player object
    """
    offset = 20  # Shield offset in every direction

    def __init__(self, x, y, image):
        """
        Create Player instance
        :param x: X coordinate of top-left corner
        :param y: Y coordinate of top-left corner
        :param image: Player image
        """
        super().__init__(x, y, image)
        if image:
            self.width = image.width()
            self.height = image.height()
        else:
            self.width = -1
            self.height = -1
        self.__update_shieldrect()

    def go_left(self):
        """
        Move left
        :return:
        """
        self.x -= 20
        self.__update_shieldrect()

    def go_right(self):
        """
        Move right
        :return:
        """
        self.x += 20
        self.__update_shieldrect()

    def go_up(self):
        """
        Move up
        :return:
        """
        self.y -= 20
        self.__update_shieldrect()

    def go_down(self):
        """
        Move down
        :return:
        """
        self.y += 20
        self.__update_shieldrect()

    def __update_shieldrect(self):
        """
        Update shield rectangle with every move
        :return: None
        """
        self.shieldx = self.x - Player.offset
        self.shieldy = self.y - Player.offset
        self.shieldw = self.width + 2 * Player.offset
        self.shieldh = self.height + 2 * Player.offset

    def move(self):
        """
        Move object according to its policy
        :return:
        """
        super().move()
        self.__update_shieldrect()


class Enemy(FlyingObject):
    """
    Generic enemy class
    """
    def __init__(self, x, y, odd, image, **kwargs):
        """
        Create enemy object
        :param x: top left x coordinate
        :param y: top left y coordinate
        :param odd: True if odd, false if even
        :param image: associated image
        :param kwargs: additional parameters: radius, angle, speedx, speedy
        Remarks:
        * radius to be specified when enemy moves around the circle
        * angle to be specified when enemy moves around the circle
        * speedx is the single horizontal distance
        * speedy is the single vertical distance
        """
        super().__init__(x, y, image)
        self.spot_x = x
        self.spot_y = y
        self.moved = 0
        self.dx = 1
        self.dy = 1
        if 'radius' in kwargs:
            self.radius = kwargs['radius']
        else:
            self.radius = 0
        if 'angle' in kwargs:
            self.angle = kwargs['angle']
        else:
            self.angle = 0
        if 'speedx' in kwargs:
            self.speedx = kwargs['speedx']
        else:
            self.speedx = 0
        if 'speedy' in kwargs:
            self.speedy = kwargs['speedy']
        else:
            self.speedy = 0
        self.odd = odd


class Medkit(FlyingObject):
    """
    Medical kit flying object
    """
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.basey = y
        self.speedx = -8

    def move(self):
        dy = int(100 * math.sin(self.x / 100))
        self.x += self.speedx
        self.y = self.basey + dy
        if self.x + self.w <= 0:
            self.valid = False


class Boss(FlyingObject):
    """
    Boss object
    """
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.dy = 1
        self.yspeed = 20
        self.indicators = 10

    def is_alive(self):
        """
        Check if boss is still alive
        (its indicators > 0)
        :return:
        """
        return self.indicators > 0

    def decrease_hp(self):
        """
        Get one shot
        :return:
        """
        if self.indicators > 0:
            self.indicators -= 1
        if self.indicators <= 0:
            self.valid = False

    def move(self):
        magic_number = 50
        if self.y >= STAGE_HEIGHT - magic_number:
            self.dy = -1
        if self.y <= 0:
            self.dy = 1
        self.y += self.dy * self.yspeed


class Shield(FlyingObject):
    """
    Flying shield to pick and become immortal for 10s
    """
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.basey = y
        self.speedx = SHIELD_SPEEDX

    def move(self):
        dy = int(100 * math.sin(self.x / 100))
        self.x -= 8
        self.y = self.basey + dy
        if self.x + self.w <= 0:
            self.valid = False


class Missile(FlyingObject):
    def __init__(self, x, y, etype, image):
        super().__init__(x, y, image)
        self.etype = etype
        self.speedx = 12
        self.speedy = 12
        self.speedhy = 6

    def move(self):
        if self.etype == MissileType.FROM:
            self.x += self.speedx
        elif self.etype == MissileType.TO:
            self.x -= self.speedx
        elif self.etype == MissileType.TO_NW:
            self.x -= self.speedx
            self.y -= self.speedy
        elif self.etype == MissileType.TO_SW:
            self.x -= self.speedx
            self.y += self.speedy
        elif self.etype == MissileType.FROM_NE:
            self.x += self.speedx
            self.y -= self.speedy
        elif self.etype == MissileType.FROM_SE:
            self.x += self.speedx
            self.y += self.speedy
        elif self.etype == MissileType.TO_NWW:
            self.x -= self.speedx
            self.y -= self.speedhy
        elif self.etype == MissileType.TO_SWW:
            self.x -= self.speedx
            self.y += self.speedhy
        if self.x > ARENA_WIDTH:
            self.valid = False
        elif self.x + self.w < 0:
            self.valid = False
        elif self.y > STAGE_HEIGHT:
            self.valid = False
        elif self.y + self.h < 0:
            self.valid = False


class Drop(FlyingObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speedx = -8
        self.speedy = 8

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x + self.w <= 0:
            self.valid = False
        if self.y >= ARENA_HEIGHT:
            self.valid = False


class Tnt(FlyingObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.basey = y

    def move(self):
        dy = int(100 * math.sin(self.x / 100))
        self.x += -8
        self.y = self.basey + dy
        if self.x + self.w <= 0:
            self.valid = False


class Meteorite(FlyingObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speedx = -2
        self.speedy = 2

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x + self.w <= 0:
            self.valid = False
        if self.y >= ARENA_HEIGHT:
            self.valid = False


class LightBall(FlyingObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.basey = y

    def move(self):
        dx = -8
        dy = int(100 * math.sin(self.x / 100))
        self.x += dx
        self.y = self.basey + dy
        if self.x + self.w <= 0:
            self.valid = False


class FireMissile(FlyingObject):
    """
    Whenever a LightBall is caught, player can shoot with
    FireMissile
    """

    def __init__(self, x, y, direction: FireballDirection, image):
        super().__init__(x, y, image)
        self.direction = direction
        if self.direction == FireballDirection.UP:
            self.speedx = 30
            self.speedy = -15
        elif self.direction == FireballDirection.STRAIGHT:
            self.speedx = 30
            self.speedy = 0
        elif self.direction == FireballDirection.DOWN:
            self.speedx = 30
            self.speedy = 15

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x > ARENA_WIDTH:
            self.valid = False
        elif self.y > ARENA_HEIGHT:
            self.valid = False
        elif self.y < 0:
            self.valid = False


class Explosion(FlyingObject):
    def __init__(self, x, y, images: list):
        super().__init__(x, y, None)
        self.images = images
        self.frame = 0
        self.frames = len(self.images)

    def paint(self, painter):
        if self.valid:
            image = self.images[self.frame]
            ax = self.x - image.width() // 2
            ay = self.y - image.height() // 2
            painter.drawPixmap(ax, ay, image)

    def move(self):
        if self.frame < self.frames - 1:
            self.frame += 1
        else:
            self.valid = False


class IceBox(FlyingObject):
    """
    When caught by the player, enters frozen mode:
    All the enemies stop and do not shoot and all the missiles disappear.
    After 20 seconds everything goes back to normal.
    """

    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.basey = y

    def move(self):
        dx = -8
        dy = int(100 * math.sin(self.x / 100))
        self.x += dx
        self.y = self.basey + dy
        if self.x + self.w <= 0:
            self.valid = False


class Bomb(FlyingObject):
    def __init__(self, x, y, image, speedy=3):
        super().__init__(x, y, image)
        self.speedx = -2  # TODO: const, taki sam jak Movables
        self.speedy = speedy

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.y >= ARENA_HEIGHT:
            self.valid = False
        if self.x <= 0:
            self.valid = False


class Star(ImageRect):
    def __init__(self, x, y, image, speed=2):
        super().__init__(x, y, image)
        self.y = y
        self.speed = speed

    def move(self):
        self.x -= self.speed
        if self.x + self.w < 0:
            self.x = STAGE_WIDTH

    @staticmethod
    def from_factory(matrix: list, image):
        stars = []
        rows = len(matrix)
        columns = len(matrix[0])
        segment_width = STAGE_WIDTH // columns
        segment_height = STAGE_HEIGHT // rows
        for i in range(rows):
            for j in range(columns):
                if matrix[i][j] == 1:
                    star = Star(
                        j * segment_width + random.randint(0, segment_width),
                        i * segment_height + segment_height // 2,
                        image,
                        STAR_SPEED)
                    stars.append(star)
        return stars
