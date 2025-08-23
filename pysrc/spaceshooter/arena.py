#!/usr/bin/env python

"""
Game Arena (Qt implementation)
"""

# Standard library imports
import random
from importlib.resources import files

# PySide imports
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QPainter
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetrics
from PySide6.QtGui import QColor
from PySide6.QtGui import QBrush
from PySide6.QtGui import QPen
from PySide6.QtCore import QSize
from PySide6.QtCore import QTimer
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt

# Local imports
from spaceshooter.sdefs import ARENA_WIDTH, ARENA_HEIGHT, BOTTOM_BAR,\
    STAGE_HEIGHT, MAX_NICK_LEN, DEFAULT_FONT
from spaceshooter.slocales import locales
from spaceshooter.stypes import MouseButton, MouseEvent, Mode, UserInput, \
    SetupMode, Key, MovableType, MissileType, Board

APPLICATION_TITLE = "SpaceShooter"


class Controller(QMainWindow):
    """
    Main application window
    """

    def __init__(self, parent):
        """
        Create window object
        :param parent: application instance handle
        """
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.parent = parent
        self.setWindowIcon(parent.images['icons']['app'])
        self.game = None
        self.setWindowTitle(APPLICATION_TITLE)

    def __pos2arena(self, event):
        """
        Translate screen position to arena-oriented coordinates
        :param event: QMouseEvent to translate
        :return: MouseEvent with translated coordinates
        """
        pos = event.pos()
        return MouseEvent(
            pos.x() * ARENA_WIDTH / self.width(),
            pos.y() * ARENA_HEIGHT / self.height(),
            MouseButton.LEFT)

    def mousePressEvent(self, event):
        """
        Mousebutton press handler
        :param event: Event description
        :return: None
        """
        k_x = self.__pos2arena(event)
        self.game.mouse_pressed(k_x)

    def keyReleaseEvent(self, event):
        """
        Key release event handler
        :param event: Event description
        :return: None
        """
        key = event.key()
        k_x = self.parent.keymapping.get(key, None)
        self.game.keyreleased(k_x)

    def keyPressEvent(self, event) -> None:
        """
        Keypress event handler
        :param event: Event description
        :return: None
        """
        key = event.key()
        k_x = self.parent.keymapping.get(key, None)
        self.game.keypressed(k_x)


class Arena(QLabel):
    """
    Game arena
    """

    def __init__(self, parent, **kwargs):
        """
        Create Arena object
        :param parent: handle to parent window
        """
        super().__init__()
        font = kwargs.get('font', DEFAULT_FONT)
        if not font:
            font = DEFAULT_FONT
        self.parent = parent
        self.shooter = None
        self.canvas = QPixmap(ARENA_WIDTH, ARENA_HEIGHT)
        self.painter = QPainter()
        self.setMouseTracking(True)
        self.game = parent.game
        self.paint_procs = {
            Board.WELCOME: self.__paint_welcome,
            Board.MENU: self.__paint_menu,
            Board.GAME: self.__paint_game,
            Board.OPTIONS: self.__paint_options,
            Board.HISCORES: self.__paint_hiscores,
            Board.SETUP: self.__paint_setup,
            Board.HELP: self.__paint_help,
            Board.ABOUT: self.__paint_about,
            Board.NEWSCORE: self.__paint_newscore,
            Board.PLAYER: self.__paint_player
        }
        self.paint_subprocs = {
            Mode.INIT: self.__paint_game_init,
            Mode.PREPARE: self.__paint_game_prepare,
            Mode.PLAY: self.__paint_game_play,
            Mode.PAUSED: self.__paint_game_paused,
            Mode.KILLED: self.__paint_game_killed,
            Mode.GAMEOVER: self.__paint_game_over,
            Mode.CONGRATS: self.__paint_game_congrats
        }

        self.fonts = {
            'logo': QFont(font, 96),
            'menu': QFont(font, 54),
            'get-ready': QFont(font, 64),
            'options': QFont(font, 48),
            'help': QFont(font, 28),
            'status-line': QFont(font, 28)
        }
        self.metrics = {
            'logo': QFontMetrics(self.fonts['logo']),
            'menu': QFontMetrics(self.fonts['menu']),
            'options': QFontMetrics(self.fonts['options']),
            'get-ready': QFontMetrics(self.fonts['get-ready']),
            'status-line': QFontMetrics(self.fonts['status-line'])
        }
        self.full_w = self.frameGeometry().width()
        self.full_h = self.frameGeometry().height()
        self.w = ARENA_WIDTH
        self.h = ARENA_HEIGHT
        self.spot_x = int((self.full_w - ARENA_WIDTH) // 2)
        self.spot_y = int((self.full_h - ARENA_HEIGHT) // 2)

    def sizeHint(self):
        """
        Generic size-hint handler
        :return: QSize object with new width and height
        """
        return QSize(
            self.full_w,
            self.full_h)

    def resizeEvent(self, _):
        """
        Window resize event
        :param _: unused
        :return: None
        """
        self.full_w = self.frameGeometry().width()
        self.full_h = self.frameGeometry().height()
        self.w = ARENA_WIDTH
        self.h = ARENA_HEIGHT
        self.spot_x = int((self.full_w - ARENA_WIDTH) // 2)
        self.spot_y = int((self.full_h - ARENA_HEIGHT) // 2)

    def __paint_bottom_bar(self, painter):
        """
        Common painter for stage/bottom area
        :param painter: Painter to paint by
        :return: None
        """
        painter.fillRect(
            0,
            STAGE_HEIGHT,
            ARENA_WIDTH,
            BOTTOM_BAR,
            self.shooter.brushes['bottom-bar'])
        # Indykatory
        indcolor = 'green'
        if self.game.indicators < 7:
            indcolor = 'yellow'
        if self.game.indicators < 4:
            indcolor = 'red'
        for ind in range(0, 10):
            if ind < self.game.indicators:
                painter.drawPixmap(
                    10 + ind * 35,
                    STAGE_HEIGHT + 20,
                    self.shooter.images['indicators'][indcolor])
            else:
                painter.drawPixmap(
                    10 + ind * 35,
                    STAGE_HEIGHT + 20,
                    self.shooter.images['indicators']['black'])
        for ind in range(self.game.lives):
            painter.drawPixmap(
                380 + 50 * ind,
                STAGE_HEIGHT + 20,
                self.shooter.images['indicators']['player'])
        painter.setFont(self.fonts['status-line'])
        painter.setPen(self.shooter.pens['textbottom'])
        x = 600
        # TNT counter
        if self.game.tnt > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 10,
                self.shooter.images['indicators']['tnt'])
            text = f'{self.game.tnt:02}'
            x += 60
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
            x += self.metrics['status-line'].horizontalAdvance(text) + 20
        # Shield Timer
        if self.game.shield_timer > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 10,
                self.shooter.images['indicators']['shield'])
            text = f'{self.game.shield_timer:02}'
            x += 50
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
            x += self.metrics['status-line'].horizontalAdvance(text) + 20
        # LightBall Timer
        if self.game.lightball_timer > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 5,
                self.shooter.images['indicators']['light-ball'])
            text = f'{self.game.lightball_timer:02}'
            x += 60
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
            x += self.metrics['status-line'].horizontalAdvance(text) + 20
        # Frozen Timer
        if self.game.frozen_timer > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 5,
                self.shooter.images['indicators']['frozen-box'])
            text = f'{self.game.frozen_timer:02}'
            x += 60
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
        # Punkty:
        if self.game.points > 0:
            text = f'P: {self.game.points:04}'
            w = self.metrics['status-line'].horizontalAdvance(text) + 20
            painter.drawText(
                ARENA_WIDTH - w,
                STAGE_HEIGHT + 50,
                text)

    def paint(self):
        """
        Generic painter aggregator
        :return: None
        """
        try:
            self.paint_procs[self.game.board]()
        except KeyError:
            pass  # Some special boards without paint method

    def __paint_menu(self):
        """
        Paint Menu board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        x = (ARENA_WIDTH - self.metrics["logo"].horizontalAdvance(
            locales['title'])) // 2
        self.painter.drawText(x + 5, 150, locales['title'])
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(
            x,
            145,
            locales['title'])
        self.painter.setFont(self.fonts['menu'])
        counter = 0
        for item in locales['menu'][self.game.config['lang']]:
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(405, (counter + 3) * 100 + 5, item)
            if counter == self.game.menu_pos:
                self.painter.setPen(self.shooter.pens['logofront2'])
                self.painter.drawPixmap(
                    180, (counter + 3) * 100 - 80, self.shooter.images['players'][0])
            else:
                self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(400, (counter + 3) * 100, item)
            counter += 1
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_game(self):
        """
        Meta-painter for Game-related boards
        :return: None
        """
        painter = self.paint_subprocs[self.game.mode]
        painter()

    def __paint_welcome(self):
        """
        Paint Welcome board
        :return: None
        """
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for i in range(ARENA_HEIGHT // 20):
            color = QColor.fromRgb(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
            self.painter.setPen(QPen(color))
            self.painter.setBrush(QBrush(color))
            self.painter.drawRect(0, i * 20, ARENA_WIDTH, (i + 1) * 20)
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_options(self):
        """
        Painter for Options board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        x = (ARENA_WIDTH - self.metrics["logo"].horizontalAdvance(
            locales['options']['title'][self.game.config['lang']])) // 2
        self.painter.drawText(x + 5, 150,
                              locales['options']['title'][self.game.config['lang']])
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(x, 145,
                              locales['options']['title'][self.game.config['lang']])
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(self.shooter.pens['textfront'])
        counter = 0
        for item in locales['options'][self.game.config['lang']]:
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(405, (counter + 3) * 100 + 5, item)
            if counter == self.game.options_pos:
                self.painter.setPen(self.shooter.pens['logofront2'])
                self.painter.drawPixmap(
                    180,
                    (counter + 3) * 100 - 80,
                    self.shooter.images['players'][0])
            else:
                self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(400, (counter + 3) * 100, item)
            counter += 1
        l_t = locales['options']['line1'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 995, l_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 990, l_t)
        l_t = locales['options']['line2'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l_t)
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio,
                                          Qt.FastTransformation))

    def __paint_hiscores(self):
        """
        Paint routine for HiScores board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        # Back
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.setFont(self.fonts['logo'])
        l_t = locales['hiscores']['title'][self.game.config['lang']]
        l_w = self.metrics['logo'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.drawText(l_x + 5, 150, l_t)
        self.painter.setFont(self.fonts['menu'])
        hiscores = self.game.config['hiscores']
        for i in range(0, 10):
            napis = f'{(i + 1):02}'
            self.painter.drawText(105, 250 + i * 75 + 5, napis)
            try:
                krotka = hiscores[i]
                (name, points) = krotka
                napis = f'{points:4d}'
                self.painter.drawText(405, 250 + i * 75 + 5, name)
                self.painter.drawText(1205, 250 + i * 75 + 5, napis)
            except IndexError:
                self.painter.drawText(405, 250 + i * 75 + 5, "---")
                self.painter.drawText(1205, 250 + i * 75 + 5, "---")
        l_t = locales['standard-line'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l_t)
        # Front
        l_t = locales['hiscores']['title'][self.game.config['lang']]
        l_w = self.metrics['logo'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(l_x, 145, l_t)
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(self.shooter.pens['textfront'])
        for i in range(0, 10):
            napis = f'{(i + 1):02}'
            self.painter.drawText(100, 250 + i * 75, napis)
            try:
                krotka = hiscores[i]
                (name, points) = krotka
                napis = f'{points:4d}'
                self.painter.drawText(400, 250 + i * 75, name)
                self.painter.drawText(1200, 250 + i * 75, napis)
            except IndexError:
                self.painter.drawText(400, 250 + i * 75, "----")
                self.painter.drawText(1200, 250 + i * 75, "----")
        l_t = locales['standard-line'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.drawText(l_x, 1045, l_t)
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_setup(self):
        """
        Paint routine for Setup board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        l_t = locales['setup']['title'][self.game.config['lang']]
        l_w = self.metrics['logo'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.drawText(l_x + 5, 155, l_t)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(l_x, 150, l_t)
        # Keys themselves:
        if self.game.setupmode == SetupMode.ENTER:
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            l_t = locales['setup']['enter-lead'][self.game.config['lang']]
            l_w = self.metrics['status-line'].horizontalAdvance(l_t)
            l_x = (ARENA_WIDTH - l_w) // 2
            self.painter.drawText(l_x + 5, 255, l_t)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(l_x, 250, l_t)
            self.painter.setFont(self.fonts['menu'])
            for i in range(self.game.temp_position + 1):
                if i == self.game.temp_position:
                    if self.game.setup_counter % 2 == 0:
                        self.painter.setPen(self.shooter.pens['textback'])
                        self.painter.drawText(305,
                                              i * 100 + 355,
                                              locales[
                                                  'setup'][self.game.config['lang']][i])
                        self.painter.drawText(1005, i * 100 + 355,
                                              str(self.game.temp_setup[i]))
                        self.painter.setPen(self.shooter.pens['logofront'])
                        self.painter.drawText(300,
                                              i * 100 + 350,
                                              locales[
                                                  'setup'][self.game.config['lang']][i])
                        self.painter.drawText(1000, i * 100 + 350,
                                              str(self.game.temp_setup[i]))
                else:
                    self.painter.setPen(self.shooter.pens['textback'])
                    self.painter.drawText(305,
                                          i * 100 + 355,
                                          locales[
                                              'setup'][self.game.config['lang']][i])
                    self.painter.drawText(1005, i * 100 + 355,
                                          str(self.game.temp_setup[i]))
                    self.painter.setPen(self.shooter.pens['textfront'])
                    self.painter.drawText(300,
                                          i * 100 + 350,
                                          locales[
                                              'setup'][self.game.config['lang']][i])
                    self.painter.drawText(1000, i * 100 + 350,
                                          str(self.game.temp_setup[i]))
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(
                200,
                1050,
                locales['setup']['enter-status'][self.game.config['lang']])
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(
                195,
                1045,
                locales['setup']['enter-status'][self.game.config['lang']])
        else:  # SetupMode.DISPLAY
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            l_t = locales['setup']['display-lead'][self.game.config['lang']]
            l_w = self.metrics['status-line'].horizontalAdvance(l_t)
            l_x = (ARENA_WIDTH - l_w) // 2
            self.painter.drawText(l_x + 5, 255, l_t)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(l_x, 250, l_t)
            self.painter.setFont(self.fonts['menu'])
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(305, 355,
                                  locales[
                                      'setup'][self.game.config['lang']][0])
            self.painter.drawText(305, 455,
                                  locales[
                                      'setup'][self.game.config['lang']][1])
            self.painter.drawText(305, 555,
                                  locales[
                                      'setup'][self.game.config['lang']][2])
            self.painter.drawText(305, 655,
                                  locales[
                                      'setup'][self.game.config['lang']][3])
            self.painter.drawText(305, 755,
                                  locales[
                                      'setup'][self.game.config['lang']][4])
            self.painter.drawText(305, 855,
                                  locales[
                                      'setup'][self.game.config['lang']][5])
            self.painter.drawText(305, 955, locales[
                'setup'][self.game.config['lang']][6])
            self.painter.drawText(1005, 355,
                                  str(self.game.config.get_key(UserInput.LEFT)))
            self.painter.drawText(1005, 455,
                                  str(self.game.config.get_key(UserInput.RIGHT)))
            self.painter.drawText(1005, 555,
                                  str(self.game.config.get_key(UserInput.TOP)))
            self.painter.drawText(1005, 655,
                                  str(self.game.config.get_key(UserInput.BOTTOM)))
            self.painter.drawText(1005, 755,
                                  str(self.game.config.get_key(UserInput.FIRE)))
            self.painter.drawText(1005, 855,
                                  str(self.game.config.get_key(UserInput.BOMB)))
            self.painter.drawText(1005, 955,
                                  str(self.game.config.get_key(UserInput.TNT)))
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(300, 350,
                                  locales['setup'][self.game.config['lang']][0])
            self.painter.drawText(300, 450,
                                  locales['setup'][self.game.config['lang']][1])
            self.painter.drawText(300, 550,
                                  locales['setup'][self.game.config['lang']][2])
            self.painter.drawText(300, 650,
                                  locales['setup'][self.game.config['lang']][3])
            self.painter.drawText(300, 750,
                                  locales['setup'][self.game.config['lang']][4])
            self.painter.drawText(300, 850,
                                  locales['setup'][self.game.config['lang']][5])
            self.painter.drawText(300, 950,
                                  locales['setup'][self.game.config['lang']][6])
            self.painter.drawText(1000, 350,
                                  str(self.game.config.get_key(UserInput.LEFT)))
            self.painter.drawText(1000, 450,
                                  str(self.game.config.get_key(UserInput.RIGHT)))
            self.painter.drawText(1000, 550,
                                  str(self.game.config.get_key(UserInput.TOP)))
            self.painter.drawText(1000, 650,
                                  str(self.game.config.get_key(UserInput.BOTTOM)))
            self.painter.drawText(1000, 750,
                                  str(self.game.config.get_key(UserInput.FIRE)))
            self.painter.drawText(1000, 850,
                                  str(self.game.config.get_key(UserInput.BOMB)))
            self.painter.drawText(1000, 950,
                                  str(self.game.config.get_key(UserInput.TNT)))
            # End keys
            l_t = locales['standard-line'][self.game.config['lang']]
            l_w = self.metrics['status-line'].horizontalAdvance(l_t)
            l_x = (ARENA_WIDTH - l_w) // 2
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(l_x + 5, 1050, l_t)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(l_x, 1045, l_t)
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio,
                                          Qt.FastTransformation))

    def __paint_help(self):
        """
        Paint routine for Help board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        e_t = locales['help']['title'][self.game.config['lang']]
        e_w = self.metrics['logo'].horizontalAdvance(e_t)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(
            e_x + 5,
            155,
            e_t)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(
            e_x,
            150,
            e_t)
        x = 100
        for player in self.shooter.images['enemies']:
            self.painter.drawPixmap(x, 475, player)
            x += 20 + player.width()
        e_t = locales['standard-line'][self.game.config['lang']]
        e_w = self.metrics['status-line'].horizontalAdvance(e_t)
        e_x = (ARENA_WIDTH - e_w) // 2
        # Help text here:
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.setFont(self.fonts['help'])
        self.painter.drawText(100, 250, locales['help'][
            self.game.config['lang']][0])
        self.painter.drawText(100, 400, locales['help'][
            self.game.config['lang']][1])
        self.painter.drawText(100, 600, locales['help'][
            self.game.config['lang']][2])
        self.painter.drawPixmap(100, 650, self.shooter.images['boss'])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 400, locales['help'][
            self.game.config['lang']][3])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 480, locales['help'][
            self.game.config['lang']][4])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 560, locales['help'][
            self.game.config['lang']][5])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 640, locales['help'][
            self.game.config['lang']][6])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 720, locales['help'][
            self.game.config['lang']][7])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 800, locales['help'][
            self.game.config['lang']][8])
        self.painter.drawText(e_x + 5, 1050, e_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(95, 245, locales['help'][
            self.game.config['lang']][0])
        self.painter.drawText(95, 395, locales['help'][
            self.game.config['lang']][1])
        self.painter.drawText(95, 595, locales['help'][
            self.game.config['lang']][2])
        self.painter.drawPixmap(100, 650, self.shooter.images['boss'])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 395, locales['help'][
            self.game.config['lang']][3])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 475, locales['help'][
            self.game.config['lang']][4])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 555, locales['help'][
            self.game.config['lang']][5])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 635, locales['help'][
            self.game.config['lang']][6])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 715, locales['help'][
            self.game.config['lang']][7])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 795, locales['help'][
            self.game.config['lang']][8])
        self.painter.drawText(e_x, 1045, e_t)
        # ... until here.
        self.painter.drawPixmap(ARENA_WIDTH // 2 + 150, 430,
                                self.shooter.images['indicators']['medkit'])
        self.painter.drawPixmap(ARENA_WIDTH // 2 + 150, 520,
                                self.shooter.images['indicators']['shield'])
        self.painter.drawPixmap(ARENA_WIDTH // 2 + 150, 600,
                                self.shooter.images['indicators']['tnt'])
        self.painter.drawPixmap(ARENA_WIDTH // 2 + 150, 670,
                                self.shooter.images['indicators']['frozen-box'])
        self.painter.drawPixmap(ARENA_WIDTH // 2 + 150, 750,
                                self.shooter.images['indicators']['light-ball'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_player(self):
        """
        Paint routine for Player board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(QPen(self.shooter.colors['textback'], 2, Qt.SolidLine))
        e_t = locales['player']['title'][self.game.config['lang']]
        w_e = self.metrics['logo'].horizontalAdvance(e_t)
        self.painter.drawText((ARENA_WIDTH - w_e) // 2 + 5, 155, e_t)
        self.painter.setPen(QPen(self.shooter.colors['logofront'], 2, Qt.SolidLine))
        self.painter.drawText((ARENA_WIDTH - w_e) // 2, 150, e_t)
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawPixmap(
            ARENA_WIDTH / 4 - self.shooter.images['icons']['prev'].width() // 2,
            600 - self.shooter.images['icons']['prev'].height() // 2,
            self.shooter.images['icons']['prev'])
        self.painter.drawPixmap(
            ARENA_WIDTH / 2 - self.shooter.images[
                'big_players'][self.game.player_index].width() // 2,
            600 - self.shooter.images[
                'big_players'][self.game.player_index].height() // 2,
            self.shooter.images['big_players'][self.game.player_index])
        self.painter.drawPixmap(
            3 * ARENA_WIDTH / 4 - self.shooter.images['icons']['next'].width() // 2,
            600 - self.shooter.images['icons']['next'].height() // 2,
            self.shooter.images['icons']['next'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        l_t = locales['player']['line1'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 995, l_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 990, l_t)
        l_t = locales['player']['line2'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l_t)
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_about(self):
        """
        Paint `About` board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        label = locales['about']['title'][self.game.config['lang']]
        label_w = self.metrics['logo'].horizontalAdvance(label)
        label_x = (ARENA_WIDTH - label_w) // 2
        self.painter.drawText(label_x + 5, 155, label)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(label_x, 150, label)
        self.painter.setFont(self.fonts['help'])
        c_y = 0
        for item in locales['about'][self.game.config['lang']]:
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(105, 300 + c_y * 60 + 5, item)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(100, 300 + c_y * 60, item)
            c_y += 1
        label_s = locales['standard-line'][self.game.config['lang']]
        label_w = self.metrics['status-line'].horizontalAdvance(label_s)
        label_x = (ARENA_WIDTH - label_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(label_x + 5, 1055, label_s)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(label_x, 1050, label_s)
        self.painter.drawPixmap(
            int(ARENA_WIDTH * 0.5),
            350,
            self.shooter.images['big_players'][3])
        self.painter.drawPixmap(
            ARENA_WIDTH - 300,
            300,
            self.shooter.images['enemies'][0])
        self.painter.drawPixmap(
            ARENA_WIDTH - 400,
            400,
            self.shooter.images['enemies'][2])
        self.painter.drawPixmap(
            ARENA_WIDTH - 300,
            500,
            self.shooter.images['enemies'][3])
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_newscore(self):
        """
        Paint routine for NewScore board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        l_t = locales['newscore']['title'][self.game.config['lang']]
        l_x = self.metrics['logo'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_x) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(
            l_x + 5,
            205,
            l_t)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(
            l_x,
            200,
            l_t)
        w_x = self.metrics['logo'].horizontalAdvance("W")
        w_h = self.metrics['logo'].height()
        x_0 = (ARENA_WIDTH - (MAX_NICK_LEN + 1) * (w_x + 30)) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        cur = len(self.game.nick)
        for i in range(MAX_NICK_LEN + 1):
            try:
                letter = self.game.nick[i]
                self.painter.drawText(x_0 + i * (w_x + 30) + 20,
                                      685,
                                      letter)
            except IndexError:
                pass
            if i == cur and self.game.newscore_counter == 0:
                r_x = QRect(x_0 + cur * (w_x + 30) + 5 + 15,
                            700 - w_h + 5,
                            w_x,
                            w_h)
                self.painter.fillRect(r_x, QBrush(self.shooter.colors['textback']))
        self.painter.setPen(self.shooter.pens['logofront'])
        for i in range(MAX_NICK_LEN + 1):
            try:
                letter = self.game.nick[i]
                self.painter.drawText(x_0 + i * (w_x + 30) + 15,
                                      680,
                                      letter)
            except IndexError:
                pass
            if i == cur and self.game.newscore_counter == 0:
                r_x = QRect(x_0 + cur * (w_x + 30) + 15,
                            700 - w_h,
                            w_x,
                            w_h)
                self.painter.fillRect(r_x, self.shooter.brushes['logofront'])
        # Status lines:
        l_t = locales['newscore']['line1'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 995, l_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 990, l_t)
        l_t = locales['newscore']['line2'][self.game.config['lang']]
        l_w = self.metrics['status-line'].horizontalAdvance(l_t)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l_t)
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_game_init(self):
        """
        Null painter
        :return: None
        """

    def __paint_game_prepare(self):
        """
        Painter for Prepare board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.__update_pixmap_play(self.painter, False)
        level_text = locales[
                         'game']['level-x'][self.game.config['lang']] % {
                         'l': self.game.level + 1}
        x_2 = (ARENA_WIDTH - self.metrics[
            'get-ready'].horizontalAdvance(level_text)) // 2
        self.painter.setFont(self.fonts['get-ready'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(x_2 + 5, 405, level_text)
        x_3 = 0
        if self.game.get_ready > 0:
            self.painter.setFont(self.fonts['logo'])
            x_3 = (ARENA_WIDTH - self.metrics['logo'].horizontalAdvance(
                f'{self.game.get_ready}')) // 2
            self.painter.drawText(x_3 + 5, 605, f'{self.game.get_ready}')
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.setFont(self.fonts['get-ready'])
        self.painter.drawText(x_2, 400, level_text)
        if self.game.get_ready > 0:
            self.painter.setFont(self.fonts['logo'])
            self.painter.drawText(x_3, 600, f'{self.game.get_ready}')
        self.__paint_bottom_bar(self.painter)
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __update_pixmap_play(self, painter, paint_objects=True):
        """
        Prepare common bitmap for Play board
        (pause and killed events will reuse this)
        Flying objects do not need to be painted on all the
        Killed, Paused or New Level boards
        :param painter: -- QPainter to draw by
        :param paint_objects: -- if True, player will be painted
        :return: None
        """
        # Rysować odtąd...
        for obj in self.game.stars:
            obj.paint(painter)
        # Drops
        # (drops before movables)
        for obj in self.game.drops:
            obj.paint(painter)
        # Movables
        for movable in self.game.movables:
            movable.paint(painter)
            # Smoke
            if movable.etype in self.shooter.smoke_spots:
                smoke = self.shooter.images['smokes'][self.game.smoke_counter]
                for spot in self.shooter.smoke_spots[movable.etype]:
                    x, y = spot
                    x += movable.x - smoke.width()
                    y += movable.y - smoke.height()
                    painter.drawPixmap(x, y, smoke)
        if paint_objects:
            # IceBoxes:
            for obj in self.game.iceboxes:
                obj.paint(painter)
            # Bombs
            for obj in self.game.bombs:
                obj.paint(painter)
            # Medkids
            for obj in self.game.medkits:
                obj.paint(painter)
            # LightBalls
            for obj in self.game.lightballs:
                obj.paint(painter)
            # TNTs
            for obj in self.game.tnts:
                obj.paint(painter)
            # Shields
            for obj in self.game.shields:
                obj.paint(painter)
            # Meteorites
            for obj in self.game.meteorites:
                obj.paint(painter)
            # Player
            self.game.player.paint(painter)
            if self.game.shield_timer > 0:
                painter.fillRect(QRect(self.game.player.shieldx,
                                       self.game.player.shieldy,
                                       self.game.player.shieldw,
                                       self.game.player.shieldh),
                                 self.shooter.brushes['shieldinter'])
                painter.setPen(self.shooter.pens['shieldline'])
                painter.drawRect(QRect(self.game.player.shieldx,
                                       self.game.player.shieldy,
                                       self.game.player.shieldw,
                                       self.game.player.shieldh))
            # Enemies
            self.game.enemymanager.paint(painter)
            # Missiles
            self.paint_missiles(painter)
            # Firemissiles
            for obj in self.game.firemissiles:
                obj.paint(painter)
            # Boss
            if self.game.boss:
                self.game.boss.paint(painter)
            # Explosions
            for obj in self.game.explosions:
                obj.paint(painter)
        self.__paint_bottom_bar(painter)
        # ... dotąd

    def paint_missiles(self, painter):
        """
        Paint all the missiles.
        Block externalized to separate method to calculate execution time
        (as there is a glitch when moving missiles)
        :param painter: Painter used for painting
        :return: None
        """
        for missile in self.game.missiles:
            missile.paint(painter)

    def __paint_game_play(self):
        """
        Paint Play board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        self.__update_pixmap_play(self.painter)
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio,
                                          Qt.FastTransformation))

    def __paint_game_paused(self):
        """
        Paint Paused board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        self.__update_pixmap_play(self.painter, False)
        self.painter.setFont(self.fonts['logo'])
        t_e = locales['awaiting']['paused'][self.game.config['lang']]
        t_w = self.metrics['logo'].horizontalAdvance(t_e)
        t_x = (ARENA_WIDTH - t_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(t_x + 5, 505, t_e)
        self.painter.setPen(self.shooter.pens['logofront2'])
        self.painter.drawText(t_x, 500, t_e)
        self.painter.setFont(self.fonts['menu'])
        e_t = locales['awaiting']['enter'][self.game.config['lang']]
        e_w = self.metrics['menu'].horizontalAdvance(e_t)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(e_x + 5, 655, e_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(e_x, 650, e_t)
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_game_killed(self):
        """
        Paint Killed board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        self.__update_pixmap_play(self.painter, False)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        t_t = locales['awaiting']['killed'][self.game.config['lang']]
        t_w = self.metrics['logo'].horizontalAdvance(t_t)
        t_x = (ARENA_WIDTH - t_w) // 2
        self.painter.drawText(t_x + 5, 505, t_t)
        self.painter.setPen(self.shooter.pens['logofront2'])
        self.painter.drawText(t_x, 500, t_t)
        self.painter.setFont(self.fonts['menu'])
        e_t = locales['awaiting']['enter'][self.game.config['lang']]
        e_w = self.metrics['menu'].horizontalAdvance(e_t)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(e_x + 5, 655, e_t)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(e_x, 650, e_t)
        # dotąd...
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_game_congrats(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        x = locales['gameover']['win'][self.game.config['lang']]
        w_x = self.metrics['logo'].horizontalAdvance(x)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(QPen(self.shooter.colors['textback'], 2, Qt.SolidLine))
        self.painter.drawText((ARENA_WIDTH - w_x) // 2 + 5,
                              305,
                              x)
        self.painter.setPen(QPen(self.shooter.colors['logofront'], 2, Qt.SolidLine))
        self.painter.drawText((ARENA_WIDTH - w_x) // 2,
                              300,
                              x)
        self.painter.drawPixmap(
            (ARENA_WIDTH - self.shooter.images['indicators']['cup'].width()) // 2,
            400,
            self.shooter.images['indicators']['cup'])
        # Status line
        label_s = locales['standard-line'][self.game.config['lang']]
        label_w = self.metrics['status-line'].horizontalAdvance(label_s)
        label_x = (ARENA_WIDTH - label_w) // 2
        self.painter.setFont(self.fonts['status-line'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(label_x + 5, 1055, label_s)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(label_x, 1050, label_s)
        # dotąd...
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))

    def __paint_game_over(self):
        """
        Paint Game Over board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        e_t = locales['gameover']['title'][self.game.config['lang']]
        f_t = locales['gameover']['description'][self.game.config['lang']]
        g_t = locales['gameover']['description2'][self.game.config['lang']]
        h_t = locales['gameover']['description3'][self.game.config['lang']]
        w_e = self.metrics['logo'].horizontalAdvance(e_t)
        w_f = self.metrics['menu'].horizontalAdvance(f_t)
        w_g = self.metrics['status-line'].horizontalAdvance(g_t)
        w_h = self.metrics['status-line'].horizontalAdvance(h_t)
        label_s = locales['standard-line'][self.game.config['lang']]
        label_w = self.metrics['status-line'].horizontalAdvance(label_s)
        label_x = (ARENA_WIDTH - label_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.setFont(self.fonts['logo'])
        self.painter.drawText(
            (ARENA_WIDTH - w_e) // 2 + 5,
            ARENA_HEIGHT // 3 + 5,
            e_t)
        self.painter.setFont(self.fonts['menu'])
        self.painter.drawText(
            (ARENA_WIDTH - w_f) // 2 + 5,
            ARENA_HEIGHT // 3 + 205,
            f_t)
        self.painter.setFont(self.fonts['status-line'])
        self.painter.drawText(
            (ARENA_WIDTH - w_g) // 2 + 5,
            ARENA_HEIGHT // 3 + 405,
            g_t)
        self.painter.drawText(
            (ARENA_WIDTH - w_h) // 2 + 5,
            ARENA_HEIGHT // 3 + 505,
            h_t)
        self.painter.drawText(label_x + 5, 1055, label_s)

        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['logofront'])

        self.painter.drawText(
            (ARENA_WIDTH - w_e) // 2,
            ARENA_HEIGHT // 3,
            e_t)
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(
            (ARENA_WIDTH - w_f) // 2,
            ARENA_HEIGHT // 3 + 200,
            f_t)
        self.painter.setFont(self.fonts['status-line'])
        self.painter.drawText(
            (ARENA_WIDTH - w_g) // 2,
            ARENA_HEIGHT // 3 + 400,
            g_t)
        self.painter.drawText(
            (ARENA_WIDTH - w_h) // 2,
            ARENA_HEIGHT // 3 + 500,
            h_t)
        self.painter.drawText(label_x, 1050, label_s)
        self.painter.drawPixmap(
            ARENA_WIDTH - 160,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['pl'])
        self.painter.drawPixmap(
            ARENA_WIDTH - 80,
            ARENA_HEIGHT - 60,
            self.shooter.images['icons']['en'])
        # dotąd...
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w,
                                          self.full_h,
                                          Qt.IgnoreAspectRatio))


class SpaceShooter(QApplication):
    """
    Main SpaceShooter application class
    This class holds all the Qt resouces (pixmaps, pens, colors, etc)
    """

    def __init__(self, args: list):
        """
        Application constructor
        :param args: Optional arguments
        """
        super().__init__(args)
        self.window = None
        self.keymapping = {
            Qt.Key_Return: Key.KEY_ENTER,
            Qt.Key_Left: Key.KEY_LEFT,
            Qt.Key_Right: Key.KEY_RIGHT,
            Qt.Key_Up: Key.KEY_TOP,
            Qt.Key_Down: Key.KEY_BOTTOM,
            Qt.Key_Enter: Key.KEY_ENTER,
            Qt.Key_Escape: Key.KEY_ESCAPE,
            Qt.Key_Backspace: Key.KEY_BACKSPACE,
            Qt.Key_A: Key.KEY_A,
            Qt.Key_B: Key.KEY_B,
            Qt.Key_C: Key.KEY_C,
            Qt.Key_D: Key.KEY_D,
            Qt.Key_E: Key.KEY_E,
            Qt.Key_F: Key.KEY_F,
            Qt.Key_G: Key.KEY_G,
            Qt.Key_H: Key.KEY_H,
            Qt.Key_I: Key.KEY_I,
            Qt.Key_J: Key.KEY_J,
            Qt.Key_K: Key.KEY_K,
            Qt.Key_L: Key.KEY_L,
            Qt.Key_M: Key.KEY_M,
            Qt.Key_N: Key.KEY_N,
            Qt.Key_O: Key.KEY_O,
            Qt.Key_P: Key.KEY_P,
            Qt.Key_Q: Key.KEY_Q,
            Qt.Key_R: Key.KEY_R,
            Qt.Key_S: Key.KEY_S,
            Qt.Key_T: Key.KEY_T,
            Qt.Key_U: Key.KEY_U,
            Qt.Key_V: Key.KEY_V,
            Qt.Key_W: Key.KEY_W,
            Qt.Key_X: Key.KEY_X,
            Qt.Key_Y: Key.KEY_Y,
            Qt.Key_Z: Key.KEY_Z,
            Qt.Key_0: Key.KEY_0,
            Qt.Key_1: Key.KEY_1,
            Qt.Key_2: Key.KEY_2,
            Qt.Key_3: Key.KEY_3,
            Qt.Key_4: Key.KEY_4,
            Qt.Key_5: Key.KEY_5,
            Qt.Key_6: Key.KEY_6,
            Qt.Key_7: Key.KEY_7,
            Qt.Key_8: Key.KEY_8,
            Qt.Key_9: Key.KEY_9,
            Qt.Key_Underscore: Key.KEY_UNDERSCORE,
            Qt.Key_Minus: Key.KEY_DASH,
            Qt.Key_Space: Key.KEY_SPACE,
            Qt.Key_F1: Key.KEY_F1
        }
        self.colors = {
            'background': QColor("#09275b"),
            'textback': QColor(12, 12, 12, 127),
            'logofront': QColor(250, 79, 141, 127),
            'logofront2': QColor(240, 161, 234, 127),
            'textfront': QColor(147, 218, 255, 127),
            'textbottom': QColor(156, 201, 85),
            'shieldline': QColor(34, 97, 13, 127)
        }
        self.pens = {
            'textback': QPen(self.colors['textback'], 2, Qt.SolidLine),
            'textfront': QPen(self.colors['textfront'], 2, Qt.SolidLine),
            'logofront': QPen(self.colors['logofront'], 2, Qt.SolidLine),
            'logofront2': QPen(self.colors['logofront2'], 2, Qt.SolidLine),
            'textbottom': QPen(self.colors['textbottom'], 2, Qt.SolidLine),
            'shieldline': QPen(self.colors['shieldline'], 4, Qt.DashLine)
        }
        self.brushes = {
            'bottom-bar': QBrush(QColor(47, 47, 47)),
            'logofront': QBrush(self.colors['logofront']),
            'shieldinter': QBrush(QColor(75, 100, 67, 96))
        }
        self.smoke_spots = {
            MovableType.FABRYKA1: [(124, 80), (246, 80), (322, 0)],
            MovableType.FABRYKA2: [(95, 130), (165, 0), (253, 0), (328, 0)],
            MovableType.FABRYKA3: [(232, 0)]
        }
        path = files("spaceshooter.images")
        self.images = {
            'star': QPixmap(path.joinpath("star.png")),
            'players': [
                QPixmap(path.joinpath("aplayer0.png")),
                QPixmap(path.joinpath("aplayer1.png")),
                QPixmap(path.joinpath("aplayer2.png")),
                QPixmap(path.joinpath("asterowiec.png"))
            ],
            'big_players': [
                QPixmap(path.joinpath("player0.png")),
                QPixmap(path.joinpath("player2.png")),
                QPixmap(path.joinpath("player3.png")),
                QPixmap(path.joinpath("sterowiec.png"))
            ],
            'movables': {
                MovableType.DZIALO: QPixmap(path.joinpath("dzialo.png")),
                MovableType.DOM1: QPixmap(path.joinpath("dom1.png")),
                MovableType.DOM2: QPixmap(path.joinpath("dom2.png")),
                MovableType.DOM3: QPixmap(path.joinpath("dom3.png")),
                MovableType.FABRYKA1: QPixmap(path.joinpath("fabryka1.png")),
                MovableType.FABRYKA2: QPixmap(path.joinpath("fabryka2.png")),
                MovableType.FABRYKA3: QPixmap(path.joinpath("fabryka3.png")),
                MovableType.WIEZOWIEC1: QPixmap(path.joinpath("wiezowiec1.png")),
                MovableType.WIEZOWIEC2: QPixmap(path.joinpath("wiezowiec2.png")),
                MovableType.WIEZOWIEC3: QPixmap(path.joinpath("wiezowiec3.png"))
            },
            'smokes': [
                QPixmap(path.joinpath("smoke-1.png")),
                QPixmap(path.joinpath("smoke-2.png")),
                QPixmap(path.joinpath("smoke-3.png")),
                QPixmap(path.joinpath("smoke-4.png"))
            ],
            'enemies': [
                QPixmap(path.joinpath("enemy4.png")),
                QPixmap(path.joinpath("enemy5.png")),
                QPixmap(path.joinpath("enemy6.png")),
                QPixmap(path.joinpath("enemy7.png")),
                QPixmap(path.joinpath("enemy8.png")),
                QPixmap(path.joinpath("enemy9.png")),
            ],
            'explosions': [
                QPixmap(path.joinpath("explosion-1.png")),
                QPixmap(path.joinpath("explosion-2.png")),
                QPixmap(path.joinpath("explosion-3.png")),
                QPixmap(path.joinpath("explosion-2.png")),
                QPixmap(path.joinpath("explosion-1.png")),
            ],
            'missiles': {
                MissileType.FROM: QPixmap(path.joinpath("missile-2.png")),
                MissileType.TO: QPixmap(path.joinpath("missile-1.png")),
                MissileType.TO_NW: QPixmap(path.joinpath("missile-3.png")),
                MissileType.TO_SW: QPixmap(path.joinpath("missile-4.png")),
                MissileType.TO_NWW: QPixmap(path.joinpath("missile-5.png")),
                MissileType.TO_SWW: QPixmap(path.joinpath("missile-6.png"))
            },
            'icons': {
                'app': QPixmap(path.joinpath("aicon.png")),
                'pl': QPixmap(path.joinpath("flag_pl.png")),
                'en': QPixmap(path.joinpath("flag_en.png")),
                'next': QPixmap(path.joinpath("next.png")),
                'prev': QPixmap(path.joinpath("prev.png"))
            },
            'boss': QPixmap(path.joinpath("pzm.png")),
            'indicators': {
                'red': QPixmap(path.joinpath("indicator_red.png")),
                'green': QPixmap(path.joinpath("indicator_green.png")),
                'yellow': QPixmap(path.joinpath("indicator_yellow.png")),
                'black': QPixmap(path.joinpath("indicator_black.png")),
                'player': QPixmap(path.joinpath("player_indicator.png")),
                'shield': QPixmap(path.joinpath("shield-green.png")),
                'tnt': QPixmap(path.joinpath("tnt.png")),
                'light-ball': QPixmap(path.joinpath("light_ball.png")),
                'frozen-box': QPixmap(path.joinpath("frozen_box.png")),
                'medkit': QPixmap(path.joinpath("apteczka.png")),
                'drop': QPixmap(path.joinpath("drop.png")),
                'bomb': QPixmap(path.joinpath("bomba.png")),
                'cup': QPixmap(path.joinpath("cup.png"))
            }
        }
        self.timers = {
            'welcome-event': QTimer(),
            'stars-update-event': QTimer(),
            'game-counter-event': QTimer(),
            'movable-update-event': QTimer(),
            'get-ready-event': QTimer(),
            'game-update-event': QTimer(),
            'paint-event': QTimer(),
            'setup-enter-event': QTimer(),
            'enemies-event': QTimer(),
            'game-events': QTimer(),
            'game-shield-event': QTimer(),
            'game-freeze-event': QTimer(),
            'game-light-event': QTimer(),
            'newscore-event': QTimer(),
            'bomb-timer': QTimer(),
            'missile-timer': QTimer(),
            'smoke-timer': QTimer()
        }
        self.timer_handlers = {
            'stars-update-event': self.game_stars_event,
            'game-counter-event': self.game_counter_event,
            'movable-update-event': self.game_movable_update_event,
            'get-ready-event': self.game_get_ready_event,
            'game-update-event': self.game_update_event,
            'paint-event': self.game_paint_event,
            'welcome-event': self.game_welcome_event,
            'setup-enter-event': self.setup_enter_event,
            'enemies-event': self.game_enemies_event,
            'game-events': self.game_events_event,
            'game-shield-event': self.game_shield_event,
            'game-freeze-event': self.game_freeze_event,
            'game-light-event': self.game_light_event,
            'newscore-event': self.newscore_event,
            'bomb-timer': self.bomb_timer,
            'missile-timer': self.missile_timer,
            'smoke-timer': self.smoke_timer
        }
        for name, timer in self.timers.items():
            timer.timeout.connect(self.timer_handlers[name])
        self.game = None

    def newscore_event(self):
        """
        Newscore timer delegator
        :return: None
        """
        self.game.newscore_event()

    def game_enemies_event(self):
        """
        Enemies timer delegator
        :return: None
        """
        self.game.enemies_event()

    def game_events_event(self):
        """
        Game Events timer delegator
        :return: None
        """
        self.game.events_event()

    def game_welcome_event(self):
        """
        Welcome timer delegator
        :return: None
        """
        self.game.welcome_event()

    def game_movable_update_event(self):
        """
        Movable timer delegator
        :return: None
        """
        self.game.movable_update_event()

    def game_update_event(self):
        """
        Game update timer delegator
        :return: None
        """
        self.game.game_update_event()

    def game_shield_event(self):
        """
        Shield timer delegator
        :return: None
        """
        self.game.shield_event()

    def game_light_event(self):
        """
        Lightball timer delegator
        :return: None
        """
        self.game.light_event()

    def game_get_ready_event(self):
        """
        GetReady timer delegator
        :return: None
        """
        self.game.get_ready_event()

    def game_stars_event(self):
        """
        Stars timer delegator
        :return: None
        """
        self.game.stars_update_event()

    def game_paint_event(self):
        """
        Paint timer delegator
        :return: None
        """
        self.game.game_paint_event()

    def game_counter_event(self):
        """
        Counter timer delegator
        :return: None
        """
        self.game.game_counter_event()

    def game_freeze_event(self):
        """
        Freeze timer delegator
        :return: None
        """
        self.game.freeze_event()

    def setup_enter_event(self):
        """
        Setup timer delegator
        :return: None
        """
        self.game.setup_enter_event()

    def bomb_timer(self):
        """
        Bomb timer delegator
        :return: None
        """
        self.game.bomb_timer()

    def missile_timer(self):
        """
        Missile timer delegator
        :return: None
        """
        self.game.missile_timer()

    def smoke_timer(self):
        """
        Smoke timer delegator
        :return: None
        """
        self.game.smoke_timer()
