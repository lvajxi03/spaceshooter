#!/usr/bin/env python

"""
SpaceShooter common definitions
"""

ARENA_WIDTH = 1920
ARENA_HEIGHT = 1080
BOTTOM_BAR = 60
STAGE_WIDTH = ARENA_WIDTH
STAGE_HEIGHT = ARENA_HEIGHT - BOTTOM_BAR

# Timeouts -- miliseconds
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

# Counters
SHIELD_TIMER = 10  # Shield timer in seconds
LIGHTBALL_TIMER = 10  # Lightball timer in seconds
FROZEN_TIMER = 10  # Frozen timer in seconds

# Object speeds
SPEEDX_BOMB = -2
SHIELD_SPEEDX = -1
MOVABLE_SPEED = 2
STAR_SPEED = 1

# Max values
MAX_PLAYER_INDEX = 3
MAX_LEVEL = 4
MAX_ENEMIES_ITERATIONS = 1
MAX_EVENTS_FACTOR = 3000
MAX_NICK_LEN = 10  # Max length of nickname to enter in new hiscore board

# Misc
DEFAULT_FONT = "Commodore 64 Rounded"


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
