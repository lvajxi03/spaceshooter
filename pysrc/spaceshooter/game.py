#!/usr/bin/env python

"""
Main Game class
"""

import os

from spaceshooter.stypes import UserInput, Key, Options, MissileType, MovableType,\
    FireballDirection, Board, Mode, SetupMode
from spaceshooter.primi import Rect, Missile, Player, Movable, Explosion, Bomb,\
    FireMissile, Star
from spaceshooter.sconfig import ShooterConfig
from spaceshooter.slocales import locales
from spaceshooter.sdefs import star_ids, ARENA_HEIGHT, ARENA_WIDTH, TIMEOUT_PAINT, TIMEOUT_WELCOME,\
    TIMEOUT_SMOKE, TIMEOUT_GET_READY, TIMEOUT_NEWSCORE, TIMEOUT_GAME_EVENTS, MAX_LEVEL,\
    TIMEOUT_SETUP_ENTER, TIMEOUT_ENEMIES_EVENTS, TIMEOUT_GAME_UPDATE, TIMEOUT_GAME_COUNTER,\
    MAX_NICK_LEN, BOTTOM_BAR, TIMEOUT_MISSILE_LOCK, TIMEOUT_SHIELD, TIMEOUT_LIGHT,\
    TIMEOUT_BOMB_LOCK, SHIELD_TIMER, TIMEOUT_FREEZE, MAX_PLAYER_INDEX, LIGHTBALL_TIMER,\
    FROZEN_TIMER
from spaceshooter.managers import EventManager, EnemyManager


class Game:
    """
    Main Game class, with all logic here
    """
    def __init__(self, shooter, params=None):
        """
        Create game instance
        :param shooter: Shooter handle
        """
        if params:
            lastfont = params.get('lastfont', None)
            read = params.get('reset', False)
        else:
            lastfont = None
            read = False
        self.config = ShooterConfig(
            filename=os.path.expanduser("~/.spaceshooterrc"),
            lastfont=lastfont)
        if read:
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
            Board.WELCOME: self.__mousepress_welcome,
            Board.MENU: self.__mousepress_menu,
            Board.PLAYER: self.__mousepress_player,
            Board.GAME: self.__mousepress_game,
            Board.OPTIONS: self.__mousepress_options,
            Board.HISCORES: self.__mousepress_hiscores,
            Board.SETUP: self.__mousepress_setup,
            Board.HELP: self.__mousepress_help,
            Board.ABOUT: self.__mousepress_about,
            Board.QUIT: self.__mousepress_quit,
            Board.NEWSCORE: self.__mousepress_newscore
        }
        self.keyrelease_events = {
            Board.WELCOME: self.__keyrelease_welcome,
            Board.PLAYER: self.__keyrelease_player,
            Board.MENU: self.__keyrelease_menu,
            Board.GAME: self.__keyrelease_game,
            Board.OPTIONS: self.__keyrelease_options,
            Board.HISCORES: self.__keyrelease_hiscores,
            Board.SETUP: self.__keyrelease_setup,
            Board.HELP: self.__keyrelease_help,
            Board.ABOUT: self.__keyrelease_about,
            Board.QUIT: self.__keyrelease_quit,
            Board.NEWSCORE: self.__keyrelease_newscore
        }
        self.keypress_events = {
            Board.GAME: self.__keypress_game
        }
        self.keyreleasegame_events = {
            Mode.INIT: self.__keyrelease_init,
            Mode.PLAY: self.__keyrelease_play,
            Mode.PAUSED: self.__keyrelease_paused,
            Mode.KILLED: self.__keyrelease_killed,
            Mode.PREPARE: self.__keyrelease_prepare,
            Mode.GAMEOVER: self.__keyrelease_gameover,
            Mode.CONGRATS: self.__keyrelease_congrats
        }
        self.keypressgame_events = {
            Mode.PLAY: self.__keypress_play
        }
        self.board_initializers = {
            Board.WELCOME: self.__init_welcome,
            Board.PLAYER: self.__init_player,
            Board.MENU: self.__init_menu,
            Board.GAME: self.__init_game,
            Board.OPTIONS: self.__init_options,
            Board.HISCORES: self.__init_hiscores,
            Board.SETUP: self.__init_setup,
            Board.HELP: self.__init_help,
            Board.ABOUT: self.__init_about,
            Board.QUIT: self.__init_quit,
            Board.NEWSCORE: self.__init_newscore
        }
        self.mode_initializers = {
            Mode.INIT: self.__init_init,  # Yes.
            Mode.PREPARE: self.__init_prepare,
            Mode.PLAY: self.__init_play,
            Mode.PAUSED: self.__init_paused,
            Mode.KILLED: self.__init_killed,
            Mode.GAMEOVER: self.__init_gameover,
            Mode.CONGRATS: self.__init_congrats
        }
        self.setupmode_initializers = {
            SetupMode.DISPLAY: self.__init_display,
            SetupMode.ENTER: self.__init_enter
        }
        self.useractions = {}
        keys = self.config.db['keys']
        for key, mapping in keys.items():
            self.useractions[mapping] = key
        # Board-related
        self.menu_pos = 0
        # Options related
        self.options_pos = self.config['lastmode']
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
        r_x = Rect(ARENA_WIDTH - 160, ARENA_HEIGHT - 60, 80, 60)
        self.lang_rectangles.append(r_x)
        r_x = Rect(ARENA_WIDTH - 80, ARENA_HEIGHT - 60, 80, 60)
        self.lang_rectangles.append(r_x)
        self.player_rectangles = []
        r_x = Rect(ARENA_WIDTH / 4 - self.shooter.images['icons']['prev'].width() / 2,
                   600 - self.shooter.images['icons']['prev'].height() / 2,
                   self.shooter.images['icons']['prev'].width(),
                   self.shooter.images['icons']['prev'].height())
        self.player_rectangles.append(r_x)
        r_x = Rect(ARENA_WIDTH / 2 - self.shooter.images[
            'big_players'][self.player_index].width() / 2,
                   600 - self.shooter.images['big_players'][self.player_index].height() / 2,
                   self.shooter.images['big_players'][self.player_index].width(),
                   self.shooter.images['big_players'][self.player_index].height())
        self.player_rectangles.append(r_x)
        r_x = Rect(3 * ARENA_WIDTH / 4 - self.shooter.images['icons']['next'].width() / 2,
                   600 - self.shooter.images['icons']['next'].height() / 2,
                   self.shooter.images['icons']['next'].width(),
                   self.shooter.images['icons']['next'].height())
        self.player_rectangles.append(r_x)
        self.eventmanager = EventManager(self, self.shooter)
        self.enemymanager = EnemyManager(self, self.shooter)
        # Newscore
        self.newscore_counter = 0
        # Player related
        self.player = None
        # Bombs related
        self.bomb_lock = False
        # Missiles related
        self.missile_lock = False
        # Smoke related
        self.smoke_counter = 0

    def __has_key_setup(self, key):
        """
        Check if key is already set
        :param key: Key to be checked
        :return: True if set, False otherwise
        """
        return key in self.temp_setup

    def __mousepress_welcome(self, _):
        """
        Mouse button handler for Welcome board
        :param _: unused
        :return: None
        """
        self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
        self.change_board(Board.MENU)

    def __mousepress_player(self, event):
        """
        Mouse button handler for Player board
        :param event: Event to process
        :return: None
        """
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.player_rectangles[0].contains(event.x, event.y):
            if self.player_index > 0:
                self.player_index -= 1
            return
        if self.player_rectangles[2].contains(event.x, event.y):
            if self.player_index < MAX_PLAYER_INDEX:
                self.player_index += 1
            return
        if self.player_rectangles[1].contains(event.x, event.y):
            self.change_board(Board.GAME)

    def __mousepress_menu(self, event):
        """
        Mouse button handler for Menu board
        :param event: Event to process
        :return: None
        """
        pos = 0
        for r_e in self.menu_rectangles:
            if r_e.contains(event.x, event.y):
                self.change_board(self.menupos2board[pos])
                return
            pos += 1
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()

    def __mousepress_game(self, event):
        """
        Mouse button meta-handler for Game board
        :param event: Event to process
        :return: None
        """
        if self.mode in [Mode.GAMEOVER, Mode.CONGRATS]:
            if self.lang_rectangles[0].contains(event.x, event.y):
                self.config['lang'] = 'pl'
                self.__update_menu_rectangles()
                self.__update_options_rectangles()
                return
            if self.lang_rectangles[1].contains(event.x, event.y):
                self.config['lang'] = 'en'
                self.__update_menu_rectangles()
                self.__update_options_rectangles()

    def __mousepress_options(self, event):
        """
        Mouse button handler for Options board
        :param event: Event to process
        :return: None
        """
        pos = 0
        for r_e in self.options_rectangles:
            if r_e.contains(event.x, event.y):
                self.config['lastmode'] = self.optionspos2option[pos]
                self.change_board(Board.MENU)
                return
            pos += 1
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()

    def __mousepress_hiscores(self, event):
        """
        Mouse button handler for HiScores board
        :param event: Event to process
        :return: None
        """
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
        else:
            self.change_board(Board.MENU)

    def __mousepress_setup(self, event):
        """
        Mouse button handler for Setup board
        :param event: Event to process
        :return: None
        """
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()

    def __mousepress_help(self, event):
        """
        Mouse button handler for Help board
        :param event: Event to process
        :return: None
        """
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
        else:
            self.change_board(Board.MENU)

    def __mousepress_about(self, event):
        """
        Mouse button handler for About board
        :param event: Event to process
        :return: None
        """
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
        else:
            self.change_board(Board.MENU)

    def __mousepress_quit(self, event):
        """
        Unused handler
        :param event: unused
        :return: None
        """

    def __mousepress_newscore(self, event):
        """
        Mouse button handler for NewScore board
        :param event: Event to process
        :return: None
        """
        if self.lang_rectangles[0].contains(event.x, event.y):
            self.config['lang'] = 'pl'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()
            return
        if self.lang_rectangles[1].contains(event.x, event.y):
            self.config['lang'] = 'en'
            self.__update_menu_rectangles()
            self.__update_options_rectangles()

    def mouse_pressed(self, event):
        """
        Generic mouse button event aggregator
        :param event: Event to handle
        :return: None
        """
        self.mousepress_events[self.board](event)

    def __update_menu_rectangles(self):
        """
        Update menu rectangles according to language
        :return: None
        """
        self.menu_rectangles = []
        f_m = self.arena.metrics['menu']
        counter = 3
        for label in locales['menu'][self.config['lang']]:
            r_x = Rect(400, counter * 100 - f_m.height(),
                       f_m.horizontalAdvance(label), f_m.height())
            self.menu_rectangles.append(r_x)
            counter += 1

    def __update_options_rectangles(self):
        """
        Update options rectanges according to language
        :return: None
        """
        self.options_rectangles = []
        f_m = self.arena.metrics['options']
        counter = 3
        for label in locales['options'][self.config['lang']]:
            r_x = Rect(400, counter * 100 - f_m.height(),
                       f_m.horizontalAdvance(label), f_m.height())
            self.options_rectangles.append(r_x)
            counter += 1

    def change_board(self, board, nextb=Board.NONE):
        """
        Change board, then execute its initial action
        :param board: Board to change to
        :param nextb: Next board, if needed
        :return: None
        """
        self.next_board = nextb
        if board != self.board:
            self.board = board
            initializer = self.board_initializers[board]
            initializer()

    def __change_mode(self, mode):
        """
        Change game mode, then execute its initial action
        :param mode: Mode to change to
        :return: None
        """
        if mode != self.mode:
            self.mode = mode
            initializer = self.mode_initializers[mode]
            initializer()

    def __change_setup(self, setup):
        """
        Change setup mode, then execute its initial action
        :param setup: Setup mode to change to
        :return: None
        """
        if self.setupmode != setup:
            self.setupmode = setup
            initializer = self.setupmode_initializers[setup]
            initializer()

    def __init_player(self):
        """
        Unused handler
        :return: None
        """

    def __init_welcome(self):
        """
        Initialize Welcome board
        :return: None
        """
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

    def __init_menu(self):
        """
        Initialize menu board
        :return: None
        """
        self.player = None
        self.__update_menu_rectangles()
        self.__stop_timers()
        self.shooter.timers['setup-enter-event'].stop()

    def __init_congrats(self):
        """
        Initialize Congratulations board
        :return: None
        """
        self.__stop_timers()

    def __init_game(self):
        """
        Initialize Game board
        :return: None
        """
        self.__change_mode(Mode.INIT)

    def __init_options(self):
        """
        Initialize options board
        :return: None
        """
        self.options_pos = int(self.config['lastmode'])
        self.__update_options_rectangles()

    def __init_hiscores(self):
        """
        Initialize HiScores board
        :return: None
        """
        self.shooter.timers['newscore-event'].stop()

    def __init_setup(self):
        """
        Initialize Setup board
        :return: None
        """
        self.__init_display()

    def __init_about(self):
        """
        Unused handler
        :return: None
        """

    def __init_quit(self):
        """
        Close game window
        :return: None
        """
        self.config.save()
        self.arena.parent.close()

    def __init_newscore(self):
        """
        Initialize NewScore board
        :return: None
        """
        self.shooter.timers['newscore-event'].start(TIMEOUT_NEWSCORE)

    def __init_display(self):
        """
        Unused handler
        :return: None
        """

    def __init_enter(self):
        """
        Initialize Enter Setup mode
        :return: None
        """
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

    def __init_init(self):
        """
        Very first game initializer
        :return: None
        """
        self.points = 0
        self.level = -1
        self.lives = 3
        self.indicators = 10
        self.tnt = 3
        self.eventmanager = EventManager(self, self.shooter)
        self.enemymanager = EnemyManager(self, self.shooter)
        self.__change_mode(Mode.PREPARE)
        self.shooter.timers['smoke-timer'].start(TIMEOUT_SMOKE)

    def __init_prepare(self):
        """
        Game prepare initializer
        :return: None
        """
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
        self.bombs = []
        movs = []
        for _ in range(0, 16):
            movs.append(next(self.movable_factory))
        self.movables = Movable.from_factory(movs,
                                             ARENA_WIDTH,
                                             self.shooter.images['movables'])
        if not self.player:
            self.player = Player(200, 400,
                                 self.shooter.images['players'][self.player_index])
        self.shooter.timers['get-ready-event'].start(TIMEOUT_GET_READY)

    def __init_play(self):
        """
        Perform all the actions necessary to start the game
        :return: None
        """
        self.game_counter = 0
        option = self.options_pos % 3
        timeout_ge = TIMEOUT_GAME_EVENTS - 100 * (option + self.level)
        timeout_ee = TIMEOUT_ENEMIES_EVENTS - 100 * (option + self.level)
        self.shooter.timers['game-update-event'].start(TIMEOUT_GAME_UPDATE)
        self.shooter.timers['game-counter-event'].start(TIMEOUT_GAME_COUNTER)
        self.shooter.timers['game-events'].start(timeout_ge)
        self.shooter.timers['enemies-event'].start(timeout_ee)
        self.shooter.timers['smoke-timer'].start(TIMEOUT_SMOKE)

    def __init_paused(self):
        """
        Perform all the actions needed when paused
        :return: None
        """
        self.shooter.timers['game-update-event'].stop()
        self.shooter.timers['game-counter-event'].stop()
        self.shooter.timers['game-events'].stop()
        self.shooter.timers['enemies-event'].stop()
        self.shooter.timers['smoke-timer'].stop()

    def __init_killed(self):
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
        self.bombs = []

    def __init_help(self):
        """
        Initial actions done when help (no actions)
        :return: None
        """

    def __init_gameover(self):
        """
        Initial actions done when game over
        :return: None
        """
        self.__stop_timers()

    def __keyrelease_player(self, key):
        """
        Key handler for Player board
        :param key: Key to handle
        :return: None
        """
        if key in (Key.KEY_Q, Key.KEY_ESCAPE):
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.change_board(Board.GAME)
        elif key == Key.KEY_LEFT:
            if self.player_index > 0:
                self.player_index -= 1
        elif key == Key.KEY_RIGHT:
            if self.player_index < 3:
                self.player_index += 1

    def __keyrelease_congrats(self, key):
        """
        Key handler for Congratulations board
        :param key: Key to handle
        :return: None
        """
        if key in (Key.KEY_ESCAPE, Key.KEY_Q):
            if self.config.is_hiscore(self.points):
                self.change_board(Board.NEWSCORE)
            else:
                self.change_board(Board.HISCORES)

    def __keyrelease_welcome(self, _k):
        """
        Key handler for Welcome board
        :param _k: unused
        :return: None
        """
        self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
        self.change_board(Board.MENU)

    def __keyrelease_menu(self, key):
        """
        Key handler for Menu board
        :param key: Key to be handled
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.QUIT)
        elif key == Key.KEY_TOP:
            if self.menu_pos > 0:
                self.menu_pos -= 1
        elif key == Key.KEY_BOTTOM:
            if self.menu_pos < len(locales['menu']['en']) - 1:
                self.menu_pos += 1
        elif key == Key.KEY_ENTER:
            self.change_board(self.menupos2board[self.menu_pos])

    def __keyrelease_game(self, key):
        """
        General key meta-handler for Game -- release event
        :param key: Key to handle
        :return: None
        """
        if self.mode in self.keyreleasegame_events:
            handler = self.keyreleasegame_events[self.mode]
            handler(key)

    def __keypress_game(self, key):
        """
        General key meta-handler for Game -- press event
        :param key: Key to handle
        :return: None
        """
        if self.mode in self.keypressgame_events:
            handler = self.keypressgame_events[self.mode]
            handler(key)

    def __keyrelease_options(self, key):
        """
        Key handler for Options board
        :param key: Key to handle
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_TOP:
            if self.options_pos > 0:
                self.options_pos -= 1
        elif key == Key.KEY_BOTTOM:
            if self.options_pos < len(locales['options']['en']) - 1:
                self.options_pos += 1
        elif key == Key.KEY_ENTER:
            self.config['lastmode'] = self.optionspos2option[self.options_pos]
            self.change_board(Board.MENU)

    def __keyrelease_hiscores(self, key):
        """
        Handle heyrelease when in HiScores board
        :param key: Key to handle
        :return: None
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(Board.MENU)

    def __keyrelease_prepare(self, key):
        """
        Handle keyrelease when in Prepare board
        :param key: Key to handle
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)

    def __keyrelease_setup(self, key):
        """
        Key handler for Setup board
        :param key: Key to handle
        :return: None
        """
        if key:
            if self.setupmode == SetupMode.DISPLAY:
                if key in [Key.KEY_Q, Key.KEY_ESCAPE]:
                    self.change_board(Board.MENU)
                elif key == Key.KEY_F1:
                    self.__change_setup(SetupMode.ENTER)
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
                    for kez, mapping in keys.items():
                        self.useractions[mapping] = kez
                    self.__change_setup(SetupMode.DISPLAY)
                elif key == Key.KEY_ESCAPE:
                    # Nie przepisywać klawszy
                    self.__change_setup(SetupMode.DISPLAY)
                elif key.is_move():
                    if not self.__has_key_setup(key):
                        if self.temp_position <= 6:
                            self.temp_setup[self.temp_position] = key
                            self.temp_position += 1
                            self.temp_position = min(self.temp_position, 6)

    def __keyrelease_about(self, key):
        """
        Key handler for ABOUT board.
        :param key: key to handle
        :return: None
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(Board.MENU)

    def __keyrelease_quit(self, _k):
        """
        Key handler for QUIT board
        :param _k: unused
        :return: None
        """
        self.arena.parent.close()

    def __keyrelease_newscore(self, key):
        """
        Key handler for NewScore board
        :param key: Key to handle
        :return: None
        """
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
                    n_list = list(self.nick)
                    n_list[MAX_NICK_LEN - 1] = str(key)
                    self.nick = "".join(n_list)
            elif key == Key.KEY_ENTER:
                if len(self.nick) > 0:
                    self.config.add_hiscore(self.nick, self.points)
                self.change_board(Board.HISCORES)

    def __keyrelease_init(self, key):
        """
        Key handler for Init board
        :param key: Key to handle
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)

    def __keypress_play(self, key):
        """
        Key handler for Play board -- press event
        :param key: Key to handle
        :return: None
        """
        if key in self.useractions:
            action = self.useractions[key]
            if action == UserInput.TOP:
                if self.player.y > 20:
                    self.player.go_up()
            elif action == UserInput.BOTTOM:
                if self.player.y < ARENA_HEIGHT - BOTTOM_BAR - self.player.height - 20:
                    self.player.go_down()
            elif action == UserInput.RIGHT:
                if self.player.x < ARENA_WIDTH - self.player.width - 20:
                    self.player.go_right()
            elif action == UserInput.LEFT:
                if self.player.x > 20:
                    self.player.go_left()

    def __keyrelease_play(self, key):
        """
        Key handler for Play board -- release event
        :param key: Key to handle
        :return: None
        """
        if key == Key.KEY_Q:
            self.__stop_timers()
            self.change_board(Board.MENU)
        elif key == Key.KEY_ESCAPE:
            self.shooter.timers['movable-update-event'].stop()
            self.__change_mode(Mode.PAUSED)
        elif key in self.useractions:
            action = self.useractions[key]
            if action == UserInput.FIRE:
                if self.lightball_timer > 0:
                    self.__create_firemissile(
                        self.player.x + self.player.w,
                        self.player.y + self.player.h // 2)
                else:
                    self.__create_missile(
                        self.player.x + self.player.w,
                        self.player.y + self.player.h // 2,
                        MissileType.FROM)
            elif action == UserInput.BOMB:
                self.__create_bomb(
                    self.player.x + self.player.w // 4,
                    self.player.y + self.player.h)
            elif action == UserInput.TNT:
                self.__explode_tnt()

    def __keyrelease_paused(self, key):
        """
        Key handler for Paused board
        :param key: Key to handle
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.__change_mode(Mode.PLAY)

    def __keyrelease_killed(self, key):
        """
        Key handler for Killed board
        :param key: Key to handle
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.__process_killed()
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.__change_mode(Mode.PLAY)

    def __keyrelease_help(self, key):
        """
        Key handler for Help board
        :param key: Key to handle
        :return: None
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(Board.MENU)

    def __keyrelease_gameover(self, key):
        """
        Key release handler for Mode.GAMEOVER
        :param key: Released key
        """
        if key in [Key.KEY_Q,
                   Key.KEY_ESCAPE]:
            self.change_board(
                Board.NEWSCORE if self.config.is_hiscore(
                    self.points) else Board.HISCORES)

    def __process_killed(self):
        """
        Process killed player
        :return: None
        """
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
        """
        Generic paint event
        :return: None
        """
        self.arena.paint()

    def stars_update_event(self):
        """
        Move all stars according to their policy
        :return: None
        """
        for star in self.stars:
            star.move()

    def welcome_event(self):
        """
        Welcome event handler
        :return: None
        """
        if self.counter['welcome'] > 0:
            self.counter['welcome'] -= 1
        else:
            self.shooter.timers['welcome-event'].stop()
            self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
            self.change_board(Board.MENU)

    def game_counter_event(self):
        """
        Game counter event handler
        :return: None
        """
        self.game_counter += 1

    def __add_movable(self):
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
        """
        Move all movables according to their policy
        :return: None
        """
        for movable in self.movables:
            movable.move()
        if not self.movables[0].is_valid():
            self.movables.pop(0)
            self.__add_movable()

    def get_ready_event(self):
        """
        Get-ready event handler
        :return: None
        """
        if self.get_ready > 0:
            self.get_ready -= 1
        else:
            self.shooter.timers['get-ready-event'].stop()
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.__change_mode(Mode.PLAY)

    def keyreleased(self, key):
        """
        Generic key handler -- released event
        :param key: Key to handle
        :return: None
        """
        if self.board in self.keyrelease_events:
            self.keyrelease_events[self.board](key)

    def keypressed(self, key):
        """
        Generic key handler -- pressed event
        :param key: Key to handle
        :return: None
        """
        if self.board in self.keypress_events:
            self.keypress_events[self.board](key)

    def __create_missile(self, x, y, etype):
        """
        Create new missile
        :param x: Missile X coordinate
        :param y: Missile Y coordinate
        :param etype: Missile type
        :return: None
        """
        if not self.missile_lock:
            self.missile_lock = True
            self.shooter.timers['missile-timer'].start(TIMEOUT_MISSILE_LOCK)
            image = self.shooter.images['missiles'][etype]
            self.missiles.append(Missile(x, y, etype, image))

    def game_update_event(self):
        """
        Move all objects according to their policies
        :return: None
        """
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
        self.__check_collision_shield()
        self.__check_collision_medkit()
        self.__check_collision_tnt()
        self.__check_collision_missiles()
        self.__check_collision_drops()
        self.__check_collision_enemies()
        self.__check_collision_lightball()
        self.__check_collision_icebox()
        self.__check_collision_bomb()
        self.__check_collision_movables()

    def enemies_event(self):
        """
        Process enemy manager run
        :return:
        """
        if not self.enemymanager.run():
            if self.level == MAX_LEVEL:
                if self.lives == 0:
                    self.__change_mode(Mode.GAMEOVER)
                else:
                    self.explosions.append(
                        Explosion(self.boss.x + self.boss.image.width() // 2,
                                  self.boss.y + self.boss.image.height() // 2,
                                  self.shooter.images['explosions']))
                    self.__change_mode(Mode.CONGRATS)
            else:
                self.__change_mode(Mode.PREPARE)

    def events_event(self):
        """
        Handle game events counter event
        :return: None
        """
        self.eventmanager.run()

    def setup_enter_event(self):
        """
        Handle Setup Enter counter event
        :return: None
        """
        self.setup_counter += 1

    def __check_collision_drops(self):
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
                    self.__explode(
                        self.player.x + self.player.w // 2,
                        self.player.y + self.player.h // 2)
                    self.drops = [x for x in self.drops if x.is_valid()]
                    self.__decrease_hp()

    def __check_collision_missiles(self):
        """
        Check all collisions with missiles
        :return: None
        """
        for missile in self.missiles:
            if missile.etype == MissileType.FROM and missile.is_valid():
                for enemy in self.enemymanager.enemies:
                    if missile.collides(enemy) and enemy.is_valid():
                        enemy.valid = False
                        missile.valid = False
                        self.__explode(enemy.x + enemy.w // 2,
                                       enemy.y + enemy.h // 2)
                        self.points += 1
                for movable in self.movables:
                    if movable.is_valid() and movable.etype == MovableType.DZIALO and \
                            movable.collides(missile):
                        movable.valid = False
                        self.points += 1
                        self.__explode(movable.x + movable.w // 2,
                                       movable.y + movable.h // 2)
                        self.__add_movable()
            elif missile.etype in [MissileType.TO,
                                   MissileType.TO_NWW,
                                   MissileType.TO_SWW,
                                   MissileType.TO_NW] and missile.is_valid():
                if self.shield_timer == 0 and self.options_pos != Options.UNLIMITED:
                    if missile.collides(self.player):
                        missile.valid = False
                        self.__explode(self.player.x + self.player.w // 2,
                                       self.player.y + self.player.h // 2)
                        self.__decrease_hp()
        for fireball in self.firemissiles:
            for enemy in self.enemymanager.enemies:
                if enemy.is_valid() and fireball.collides(enemy) and fireball.is_valid():
                    enemy.valid = False
                    fireball.valid = False
                    self.points += 1
                    self.__explode(enemy.x + enemy.w // 2,
                                   enemy.y + enemy.h // 2)
            for movable in self.movables:
                if movable.is_valid() and movable.etype == MovableType.DZIALO and \
                        fireball.collides(movable) and fireball.is_valid():
                    movable.valid = False
                    self.points += 1
                    self.__explode(movable.x + movable.w // 2,
                                   movable.y + movable.h // 2)
                    self.__add_movable()
        if self.enemymanager.boss:
            for missile in self.missiles:
                if missile.etype == MissileType.FROM and missile.is_valid():
                    if self.enemymanager.boss.collides(missile):
                        self.enemymanager.boss.decrease_hp()

        self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
        self.missiles = [x for x in self.missiles if x.is_valid()]
        self.movables = [x for x in self.movables if x.is_valid()]
        self.firemissiles = [x for x in self.firemissiles if x.is_valid()]

    def __decrease_hp(self):
        """
        Decrease indicator points when collided by an object
        :return: None
        """
        if self.indicators > 0:
            self.indicators -= 1
        if self.indicators == 0:
            self.lives -= 1
            if self.lives <= 0:  # In case of two timers did the lives < 0
                self.__change_mode(Mode.GAMEOVER)
            else:
                self.__process_killed()
                self.__change_mode(Mode.KILLED)

    def __increase_hp(self):
        """
        Increase indicator points (when medkit caught)
        :return: None
        """
        if self.indicators < 10:
            self.indicators += 1

    def __check_collision_enemies(self):
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
                self.__explode(enemy.x + enemy.w // 2,
                               enemy.y + enemy.h // 2)
                self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
                if self.shield_timer == 0 and self.frozen_timer == 0 and \
                        self.options_pos != Options.UNLIMITED:
                    self.__decrease_hp()

    def __check_collision_movables(self):
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
                    self.__explode(movable.x + movable.w // 2,
                                   movable.y + movable.h // 2)
                    self.__add_movable()
                    self.movables = [x for x in self.movables if x.is_valid()]
                    self.__decrease_hp()

    def __explode(self, x, y):
        """
        Create new explosion and append to all explosions list
        :param x: X coordinate of explosion
        :param y: Y coordinate of explosion
        :return: None
        """
        self.explosions.append(
            Explosion(
                x, y, self.shooter.images['explosions']))

    def __explode_tnt(self):
        """
        Create 3 explosions when TNT used
        :return: None
        """
        if self.tnt > 0 and len(self.enemymanager.enemies) > 0:
            for i in range(0, 3):
                try:
                    enemy = self.enemymanager.enemies[i]
                    self.__explode(enemy.x + enemy.w // 2,
                                   enemy.y + enemy.h // 2)
                    enemy.valid = False
                except IndexError:
                    pass
            self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
            self.tnt -= 1

    def __check_collision_medkit(self):
        """
        Check collision with medkits -- collect health points
        """
        for medkit in self.medkits:
            if medkit.collides(self.player):
                medkit.valid = False
                self.__increase_hp()
        self.medkits = [x for x in self.medkits if x.is_valid()]

    def __check_collision_shield(self):
        """
        Check collision with shields -- collect a shield
        (remove all remaining shields if any)
        """
        for shield in self.shields:
            if shield.collides(self.player):
                self.shield_timer = SHIELD_TIMER
                self.shields = []
                self.shooter.timers['game-shield-event'].start(TIMEOUT_SHIELD)

    def __check_collision_tnt(self):
        """
        Check collision with TNT -- collect a TNT
        """
        for tnt in self.tnts:
            if tnt.collides(self.player):
                self.tnt += 1
                tnt.valid = False
        self.tnts = [x for x in self.tnts if x.is_valid()]

    def __check_collision_lightball(self):
        """
        Check collision with lightball -- enter LightBall mode
        (3 missiles in a single shot)
        """
        for light_ball in self.lightballs:
            if light_ball.collides(self.player):
                self.lightball_timer = LIGHTBALL_TIMER
                light_ball.valid = False
                self.lightballs = []
                self.shooter.timers['game-light-event'].start(TIMEOUT_LIGHT)

    def __check_collision_icebox(self):
        """
        Check if player caught icebox
        :return: None
        """
        for icebox in self.iceboxes:
            if icebox.collides(self.player):
                icebox.valid = False
                self.frozen_timer = FROZEN_TIMER
                self.iceboxes = []
                self.missiles = []  # If frozen mode, no missiles shall be present.
                self.shooter.timers['game-freeze-event'].start(TIMEOUT_FREEZE)

    def __check_collision_bomb(self):
        """
        Check if movable or enemy collided with a bomb
        :return: None
        """
        for bomb in self.bombs:
            for movable in self.movables:
                if movable.is_valid() and bomb.collides(movable):
                    self.__explode(movable.x + movable.w // 2, movable.y + movable.h // 2)
                    bomb.valid = False
                    movable.valid = False
                    self.__add_movable()
                    self.points += 1
            for enemy in self.enemymanager.enemies:
                if enemy.is_valid() and bomb.collides(enemy):
                    self.__explode(enemy.x + enemy.w // 2, enemy.y + enemy.h // 2)
                    enemy.valid = False
                    bomb.valid = False
                    self.points += 1
        self.movables = [x for x in self.movables if x.is_valid()]
        self.bombs = [x for x in self.bombs if x.is_valid()]

    def __create_bomb(self, x, y):
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
        """
        Handle shield counter event
        :return: None
        """
        if self.shield_timer > 0:
            self.shield_timer -= 1
        else:
            self.shooter.timers['game-shield-event'].stop()

    def light_event(self):
        """
        Handle lightball event
        :return: None
        """
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

    def __create_firemissile(self, x, y):
        """
        Create fire missile, which in fact contains 3 fireballs
        :param x: initial X position of firemissile
        :param y: initial Y position of firemissile
        :return: None
        """
        if not self.missile_lock:
            self.missile_lock = True
            self.shooter.timers['missile-timer'].start(TIMEOUT_MISSILE_LOCK)
            self.firemissiles.append(
                FireMissile(x,
                            y,
                            FireballDirection.UP,
                            self.shooter.images['indicators']['light-ball']))
            self.firemissiles.append(
                FireMissile(x,
                            y,
                            FireballDirection.STRAIGHT,
                            self.shooter.images['indicators']['light-ball']))
            self.firemissiles.append(
                FireMissile(x,
                            y,
                            FireballDirection.DOWN,
                            self.shooter.images['indicators']['light-ball']))

    def newscore_event(self):
        """
        Handle newscore event
        (cursor blinking)
        :return: None
        """
        self.newscore_counter = 0 if self.newscore_counter == 1 else 1

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
