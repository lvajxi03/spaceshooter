#!/usr/bin/env python

"""
SpaceShooter common definitions
"""

ARENA_WIDTH = 1920
ARENA_HEIGHT = 1080
BOTTOM_BAR = 60

SHIELD_SPEEDX = -1

TIMEOUT_PAINT = 15
TIMEOUT_GAME_UPDATE = 40
TIMEOUT_WELCOME = 1000
TIMEOUT_GAME_COUNTER = 1000
TIMEOUT_SETUP_ENTER = 500
TIMEOUT_GAME_EVENTS = 1000
TIMEOUT_ENEMIES_EVENTS = 1000
TIMEOUT_PLAYER_MOVE = 25
TIMEOUT_BOMB_LOCK = 300
TIMEOUT_MISSILE_LOCK = 150

TIMEOUT_SHIELD = 1000
TIMEOUT_FREEZE = 1000
TIMEOUT_LIGHT = 1000
TIMEOUT_NEWSCORE = 500
TIMEOUT_GET_READY = 1000

TIMEOUT_SMOKE = 300

STAGE_WIDTH = ARENA_WIDTH
STAGE_HEIGHT = ARENA_HEIGHT - BOTTOM_BAR

MOVABLE_SPEED = 2
STAR_SPEED = 1
MAX_LEVEL = 4
MAX_ENEMIES_ITERATIONS = 1
MAX_EVENTS_FACTOR = 3000
MAX_NICK_LEN = 10  # Max length of nickname to enter in new hiscore board

SHIELD_TIMER = 10  # Shield timer in seconds

# Stars matrix
star_ids = [
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1]
]
