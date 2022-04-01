#!/usr/bin/env python

import os


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
    Missile,
    Player,
    Movable,
    Explosion,
    Bomb,
    FireMissile,
    Star
)
from sconfig import ShooterConfig
from slocales import locales
from sdefs import *
from managers import (
    EventManager,
    EnemyManager)


class Game:
    """
    Main Game class, with all logic here
    """
    def __init__(self, shooter):
        """
        Create game instance
        :param shooter: Shooter handle
        """
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
        # Bombs related
        self.bomb_lock = False
        # Missiles related
        self.missile_lock = False
        # Smoke related
        self.smoke_counter = 0

    def has_key_setup(self, key):
        """
        Check if key is already set
        :param key: Key to be checked
        :return: True if set, False otherwise
        """
        return True if key in self.temp_setup else False

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
        for label in locales['menu'][self.config['lang']]:
            r = Rect(400, c * 100 - fm.height(), fm.horizontalAdvance(label), fm.height())
            self.menu_rectangles.append(r)
            c += 1

    def update_options_rectangles(self):
        self.options_rectangles = []
        fm = self.arena.metrics['options']
        c = 3
        for label in locales['options'][self.config['lang']]:
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
        self.shooter.timers['setup-enter-event'].stop()

    def init_congrats(self):
        self.__stop_timers()

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
        self.bombs = []

    def init_help(self):
        """
        Initial actions done when help (no actions)
        :return: None
        """

    def init_gameover(self):
        """
        Initial actions done when game over
        :return: None
        """
        self.__stop_timers()

    def keyrelease_player(self, key, _):
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

    def keyrelease_congrats(self, key, _):
        if key in (Key.KEY_ESCAPE, Key.KEY_Q):
            if self.config.is_hiscore(self.points):
                self.change_board(Board.NEWSCORE)
            else:
                self.change_board(Board.HISCORES)

    def keyrelease_welcome(self, _k, _t):
        self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
        self.change_board(Board.MENU)

    def keyrelease_menu(self, key, _):
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
            if self.options_pos < len(locales['options']['en']) - 1:
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
                    for kez in keys:
                        self.useractions[keys[kez]] = kez
                    self.change_setup(SetupMode.DISPLAY)
                elif key == Key.KEY_ESCAPE:
                    # Nie przepisywać klawszy
                    self.change_setup(SetupMode.DISPLAY)
                elif key.is_move():
                    if not self.has_key_setup(key):
                        if self.temp_position <= 6:
                            self.temp_setup[self.temp_position] = key
                            self.temp_position += 1
                            self.temp_position = min(self.temp_position, 6)

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
        """
        Key handler for NewScore board
        :param key: Key to handle
        :param _t: unused
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
                    n = list(self.nick)
                    n[MAX_NICK_LEN - 1] = str(key)
                    self.nick = "".join(n)
            elif key == Key.KEY_ENTER:
                if len(self.nick) > 0:
                    self.config.add_hiscore(self.nick, self.points)
                self.change_board(Board.HISCORES)

    def keyrelease_init(self, key, _):
        """
        Key handler for Init board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)

    def keyrelease_play(self, key, _):
        """
        Key handler for Play board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        if key == Key.KEY_Q:
            self.__stop_timers()
            self.change_board(Board.MENU)
        elif key == Key.KEY_ESCAPE:
            self.shooter.timers['movable-update-event'].stop()
            self.change_mode(Mode.PAUSED)
        elif key in self.useractions:
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
        """
        Key handler for Paused board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.change_mode(Mode.PLAY)

    def keyrelease_killed(self, key, _):
        """
        Key handler for Killed board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        if key == Key.KEY_Q:
            self.change_board(Board.MENU)
        elif key == Key.KEY_ENTER:
            self.process_killed()
            self.shooter.timers['movable-update-event'].start(TIMEOUT_PAINT)
            self.change_mode(Mode.PLAY)

    def keyrelease_help(self, key, _):
        """
        Key handler for Help board
        :param key: Key to handle
        :param _: unused
        :return: None
        """
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
        for star in self.stars:
            star.move()

    def welcome_event(self):
        if self.counter['welcome'] > 0:
            self.counter['welcome'] -= 1
        else:
            self.shooter.timers['welcome-event'].stop()
            self.shooter.timers['stars-update-event'].start(TIMEOUT_PAINT)
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

    def keyreleased(self, key, _):
        """
        Generic key handler
        :param key: Key to handle
        :param _: unused
        :return: None
        """
        self.keyrelease_events[self.board](key, None)

    def create_missile(self, x, y, etype):
        if not self.missile_lock:
            self.missile_lock = True
            self.shooter.timers['missile-timer'].start(TIMEOUT_MISSILE_LOCK)
            image = self.shooter.images['missiles'][etype]
            self.missiles.append(Missile(x, y, etype, image))

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
                    if missile.collides(enemy) and enemy.is_valid():
                        enemy.valid = False
                        missile.valid = False
                        self.explode(enemy.x + enemy.w // 2,
                                     enemy.y + enemy.h // 2)
                        self.points += 1
                for movable in self.movables:
                    if movable.is_valid() and movable.etype == MovableType.DZIALO and \
                            movable.collides(missile):
                        movable.valid = False
                        self.points += 1
                        self.explode(movable.x + movable.w // 2,
                                     movable.y + movable.h // 2)
                        self.add_movable()
            elif missile.etype in [MissileType.TO,
                                   MissileType.TO_NWW,
                                   MissileType.TO_SWW,
                                   MissileType.TO_NW] and missile.is_valid():
                if self.shield_timer == 0 and self.options_pos != Options.UNLIMITED:
                    if missile.collides(self.player):
                        missile.valid = False
                        self.explode(self.player.x + self.player.w // 2,
                                     self.player.y + self.player.h // 2)
                        self.decrease_hp()
        for fireball in self.firemissiles:
            for enemy in self.enemymanager.enemies:
                if enemy.is_valid() and fireball.collides(enemy) and fireball.is_valid():
                    enemy.valid = False
                    fireball.valid = False
                    self.points += 1
                    self.explode(enemy.x + enemy.w // 2,
                                 enemy.y + enemy.h // 2)
            for movable in self.movables:
                if movable.is_valid() and movable.etype == MovableType.DZIALO and \
                        fireball.collides(movable) and fireball.is_valid():
                    movable.valid = False
                    self.points += 1
                    self.explode(movable.x + movable.w // 2,
                                 movable.y + movable.h // 2)
                    self.add_movable()
        if self.enemymanager.boss:
            for missile in self.missiles:
                if missile.etype == MissileType.FROM and missile.is_valid():
                    if self.enemymanager.boss.collides(missile):
                        self.enemymanager.boss.decrease_hp()

        self.enemymanager.enemies = [x for x in self.enemymanager.enemies if x.is_valid()]
        self.missiles = [x for x in self.missiles if x.is_valid()]
        self.movables = [x for x in self.movables if x.is_valid()]
        self.firemissiles = [x for x in self.firemissiles if x.is_valid()]

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
                    self.add_movable()
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
        for light_ball in self.lightballs:
            if light_ball.collides(self.player):
                self.lightball_timer = 10
                light_ball.valid = False
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
