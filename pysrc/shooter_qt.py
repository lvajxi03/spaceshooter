#!/usr/bin/env python

# Dealing with fonts:
# 1. Download and install your favourite font
# 2. Use its name below in DEFAULT_FONT variable
# Remark: if font is not found, default one is used
# (and it's pretty awful)

# Sample fonts:
# DEFAULT_FONT = "Good Times Rg"
# DEFAULT_FONT = "Commodore 64"
# DEFAULT_FONT = "C64 Pro"
DEFAULT_FONT = "Commodore 64 Rounded"

APPLICATION_TITLE = "SpaceShooter"

import sys

# This is us:
from spaceshooter import *

try:
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QMainWindow
    from PySide2.QtWidgets import QLabel

    from PySide2.QtGui import QPixmap
    from PySide2.QtGui import QPainter
    from PySide2.QtGui import QFont
    from PySide2.QtGui import QFontMetrics
    from PySide2.QtGui import QPolygon
    from PySide2.QtGui import QColor
    from PySide2.QtGui import QBrush
    from PySide2.QtGui import QPen

    from PySide2.QtMultimedia import QSound

    from PySide2.QtCore import QSize
    from PySide2.QtCore import QPoint
    from PySide2.QtCore import QTimer
    from PySide2.QtCore import QRect

    from PySide2.QtCore import Qt

except ImportError:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QMainWindow
    from PyQt5.QtWidgets import QLabel

    from PyQt5.QtGui import QPixmap
    from PyQt5.QtGui import QImage
    from PyQt5.QtGui import QPainter
    from PyQt5.QtGui import QFont
    from PyQt5.QtGui import QFontMetrics
    from PyQt5.QtGui import QPolygon
    from PyQt5.QtGui import QColor
    from PyQt5.QtGui import qRgb
    from PyQt5.QtGui import qRed
    from PyQt5.QtGui import QBrush
    from PyQt5.QtGui import QPen

    from PyQt5.QtMultimedia import QSound

    from PyQt5.QtCore import QSize
    from PyQt5.QtCore import QPoint
    from PyQt5.QtCore import QTimer
    from PyQt5.QtCore import QRect

    from PyQt5.QtCore import Qt


class Controller(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.parent = parent
        self.game = None
        self.setWindowTitle(APPLICATION_TITLE)

    def pos2arena(self, event):
        """
        Translate screen position to arena-oriented coordinates

        Parameters:
        * event: QMouseEvent to translate

        Return
        MouseEvent with translated coordinates
        """
        pos = event.pos()
        return MouseEvent(
            pos.x() * ARENA_WIDTH / self.width(),
            pos.y() * ARENA_HEIGHT / self.height(),
            MouseButton.LEFT)

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        k = self.parent.keymapping.get(key, None)
        self.game.keypressed(k, text)

    def mousePressEvent(self, event):
        k = self.pos2arena(event)
        self.game.mouse_pressed(k)

    def keyReleaseEvent(self, event):
        key = event.key()
        text = event.text()
        k = self.parent.keymapping.get(key, None)
        self.game.keyreleased(k, text)


class Arena(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.shooter = None
        self.canvas = QPixmap(ARENA_WIDTH, ARENA_HEIGHT)
        self.painter = QPainter()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle(APPLICATION_TITLE)
        self.setMouseTracking(True)
        self.game = parent.game
        self.paint_procs = {
            Board.WELCOME: self.paint_welcome,
            Board.MENU: self.paint_menu,
            Board.GAME: self.paint_game,
            Board.OPTIONS: self.paint_options,
            Board.HISCORES: self.paint_hiscores,
            Board.SETUP: self.paint_setup,
            Board.HELP: self.paint_help,
            Board.ABOUT: self.paint_about,
            Board.NEWSCORE: self.paint_newscore,
            Board.PLAYER: self.paint_player
        }

        self.paint_subprocs = {
            Mode.INIT: self.paint_game_init,
            Mode.PREPARE: self.paint_game_prepare,
            Mode.PLAY: self.paint_game_play,
            Mode.PAUSED: self.paint_game_paused,
            Mode.KILLED: self.paint_game_killed,
            Mode.GAMEOVER: self.paint_game_over,
            Mode.CONGRATS: self.paint_game_congrats
        }

        self.fonts = {
            'logo': QFont(DEFAULT_FONT, 96),
            'menu': QFont(DEFAULT_FONT, 54),
            'get-ready': QFont(DEFAULT_FONT, 64),
            'options': QFont(DEFAULT_FONT, 48),
            'help': QFont(DEFAULT_FONT, 28),
            'status-line': QFont(DEFAULT_FONT, 28)
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
        return QSize(
            self.full_w,
            self.full_h)

    def resizeEvent(self, _):
        self.full_w = self.frameGeometry().width()
        self.full_h = self.frameGeometry().height()
        self.w = ARENA_WIDTH
        self.h = ARENA_HEIGHT
        self.spot_x = int((self.full_w - ARENA_WIDTH) // 2)
        self.spot_y = int((self.full_h - ARENA_HEIGHT) // 2)

    def paint_bottom_bar(self, painter):
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
        painter.setPen(QPen(QColor(156, 201, 85), 2, Qt.SolidLine))
        x = 600
        # TNT counter
        if self.game.tnt > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 10,
                self.shooter.images['indicators']['tnt'])
            text = "%(f)02d" % {'f': self.game.tnt}
            x += 60
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
            x += self.metrics['status-line'].width(text) + 20
        # Shield Timer
        if self.game.shield_timer > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 10,
                self.shooter.images['indicators']['shield'])
            text = "%(f)02d" % {'f': self.game.shield_timer}
            x += 50
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
            x += self.metrics['status-line'].width(text) + 20
        # LightBall Timer
        if self.game.lightball_timer > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 5,
                self.shooter.images['indicators']['light-ball'])
            text = "%(f)02d" % {'f': self.game.lightball_timer}
            x += 60
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
            x += self.metrics['status-line'].width(text) + 20
        # Frozen Timer
        if self.game.frozen_timer > 0:
            painter.drawPixmap(
                x,
                STAGE_HEIGHT + 5,
                self.shooter.images['indicators']['frozen-box'])
            text = "%(f)02d" % {'f': self.game.frozen_timer}
            x += 60
            painter.drawText(
                x,
                STAGE_HEIGHT + 50,
                text)
        # Punkty:
        if self.game.points > 0:
            text = "P: %(f)04d" % {'f': self.game.points}
            w = self.metrics['status-line'].width(text) + 20
            painter.drawText(
                ARENA_WIDTH - w,
                STAGE_HEIGHT + 50,
                text)

    @log_usage
    def paint(self):
        try:
            self.paint_procs[self.game.board]()
        except KeyError:
            pass  # Some special boards without paint method

    @log_usage
    def paint_menu(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(QPen(QColor(12, 12, 12, 127), 2, Qt.SolidLine))
        x = (ARENA_WIDTH - self.metrics["logo"].width(
            self.shooter.labels['title'])) // 2
        self.painter.drawText(x + 5, 150, self.shooter.labels['title'])
        self.painter.setPen(QPen(QColor(250, 79, 141, 127), 2, Qt.SolidLine))
        self.painter.drawText(
            x,
            145,
            self.shooter.labels['title'])
        self.painter.setFont(self.fonts['menu'])
        c = 3
        counter = 0
        for item in self.shooter.labels['menu'][self.game.config['lang']]:
            self.painter.setPen(QPen(QColor(12, 12, 12, 127), 2, Qt.SolidLine))
            self.painter.drawText(405, c * 100 + 5, item)
            if counter == self.game.menu_pos:
                self.painter.setPen(QPen(QColor(240, 161, 234, 127), 2, Qt.SolidLine))
                self.painter.drawPixmap(
                    180, c * 100 - 80, self.shooter.images['players'][0])
            else:
                self.painter.setPen(QPen(QColor(147, 218, 255, 127), 2, Qt.SolidLine))
            self.painter.drawText(400, c * 100, item)
            c += 1
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_game(self):
        painter = self.paint_subprocs[self.game.mode]
        painter()

    def paint_welcome(self):
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_options(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(QPen(QColor(12, 12, 12, 127), 2, Qt.SolidLine))
        x = (ARENA_WIDTH - self.metrics["logo"].width(
            self.shooter.labels['options']['title'][self.game.config['lang']])) // 2
        self.painter.drawText(x + 5, 150,
                    self.shooter.labels['options']['title'][self.game.config['lang']])
        self.painter.setPen(QPen(QColor(240, 161, 234, 127), 2, Qt.SolidLine))
        self.painter.setPen(QPen(QColor(250, 79, 141, 127), 2, Qt.SolidLine))
        self.painter.drawText(x, 145,
                    self.shooter.labels['options']['title'][self.game.config['lang']])
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(QPen(QColor(147, 218, 255, 127), 2, Qt.SolidLine))
        c = 3
        counter = 0
        for item in self.shooter.labels['options'][self.game.config['lang']]:
            self.painter.setPen(QPen(QColor(12, 12, 12, 127), 2, Qt.SolidLine))
            self.painter.drawText(405, c * 100 + 5, item)
            if counter == self.game.options_pos:
                self.painter.setPen(QPen(QColor(250, 79, 141, 127), 2, Qt.SolidLine))
                self.painter.setPen(QPen(QColor(240, 161, 234, 127), 2, Qt.SolidLine))
                self.painter.drawPixmap(180, c * 100 - 80, self.shooter.images['players'][0])
            else:
                self.painter.setPen(QPen(QColor(147, 218, 255, 127), 2, Qt.SolidLine))
            self.painter.drawText(400, c * 100, item)
            c += 1
            counter += 1
        l = self.shooter.labels['options']['line1'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 995, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 990, l)
        l = self.shooter.labels['options']['line2'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio, Qt.FastTransformation))

    def paint_hiscores(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        l = self.shooter.labels['hiscores']['title'][self.game.config['lang']]
        l_w = self.metrics['logo'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 150, l)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(l_x, 145, l)
        self.painter.setFont(self.fonts['menu'])
        hiscores = self.game.config['hiscores']
        for i in range(0, 10):
            napis = "%(i)2d." % {'i': i + 1}
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(105, 250 + i * 75 + 5, napis)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(100, 250 + i * 75, napis)
            try:
                krotka = hiscores[i]
                (name, points) = krotka
                napis = "%(p)3d" % {'p': points}
                self.painter.setPen(self.shooter.pens['textback'])
                self.painter.drawText(405, 250 + i * 75 + 5, name)
                self.painter.drawText(1205, 250 + i * 75 + 5, napis)
                self.painter.setPen(self.shooter.pens['textfront'])
                self.painter.drawText(400, 250 + i * 75, name)
                self.painter.drawText(1200, 250 + i * 75, napis)
            except IndexError:
                pass
                self.painter.setPen(self.shooter.pens['textback'])
                self.painter.drawText(405, 250 + i * 75 + 5, "---")
                self.painter.drawText(1205, 250 + i * 75 + 5, "---")
                self.painter.setPen(self.shooter.pens['textfront'])
                self.painter.drawText(400, 250 + i * 75, "---")
                self.painter.drawText(1200, 250 + i * 75, "---")
        l = self.shooter.labels['standard-line'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_setup(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        l = self.shooter.labels['setup']['title'][self.game.config['lang']]
        l_w = self.metrics['logo'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.drawText(l_x + 5, 155, l)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(l_x, 150, l)
        # Keys themselves:
        if self.game.setupmode == SetupMode.ENTER:
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            l = self.shooter.labels['setup']['enter-lead'][self.game.config['lang']]
            l_w = self.metrics['status-line'].width(l)
            l_x = (ARENA_WIDTH - l_w) // 2
            self.painter.drawText(l_x + 5, 255, l)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(l_x, 250, l)
            self.painter.setFont(self.fonts['menu'])
            for i in range(self.game.temp_position + 1):
                if i == self.game.temp_position:
                    if self.game.setup_counter % 2 == 0:
                        self.painter.setPen(self.shooter.pens['textback'])
                        self.painter.drawText(305,
                                    i * 100 + 355,
                                    self.shooter.labels[
                                        'setup'][self.game.config['lang']][i])
                        self.painter.drawText(1005, i * 100 + 355,
                                    str(self.game.temp_setup[i]))
                        self.painter.setPen(self.shooter.pens['logofront'])
                        self.painter.drawText(300,
                                    i * 100 + 350,
                                    self.shooter.labels[
                                        'setup'][self.game.config['lang']][i])
                        self.painter.drawText(1000, i * 100 + 350,
                                    str(self.game.temp_setup[i]))
                else:
                    self.painter.setPen(self.shooter.pens['textback'])
                    self.painter.drawText(305,
                                i * 100 + 355,
                                self.shooter.labels[
                                    'setup'][self.game.config['lang']][i])
                    self.painter.drawText(1005, i * 100 + 355,
                                str(self.game.temp_setup[i]))
                    self.painter.setPen(self.shooter.pens['textfront'])
                    self.painter.drawText(300,
                                i * 100 + 350,
                                self.shooter.labels[
                                    'setup'][self.game.config['lang']][i])
                    self.painter.drawText(1000, i * 100 + 350,
                                str(self.game.temp_setup[i]))
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(200, 1050, self.shooter.labels['setup']['enter-status'][self.game.config['lang']])
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(195, 1045, self.shooter.labels['setup']['enter-status'][self.game.config['lang']])
        else:  # SetupMode.DISPLAY
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            l = self.shooter.labels['setup']['display-lead'][self.game.config['lang']]
            l_w = self.metrics['status-line'].width(l)
            l_x = (ARENA_WIDTH - l_w) // 2
            self.painter.drawText(l_x + 5, 255, l)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(l_x, 250, l)
            self.painter.setFont(self.fonts['menu'])
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(305, 355,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][0])
            self.painter.drawText(305, 455,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][1])
            self.painter.drawText(305, 555,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][2])
            self.painter.drawText(305, 655,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][3])
            self.painter.drawText(305, 755,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][4])
            self.painter.drawText(305, 855,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][5])
            self.painter.drawText(305, 955, self.shooter.labels[
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
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][0])
            self.painter.drawText(300, 450,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][1])
            self.painter.drawText(300, 550,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][2])
            self.painter.drawText(300, 650,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][3])
            self.painter.drawText(300, 750,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][4])
            self.painter.drawText(300, 850,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][5])
            self.painter.drawText(300, 950,
                        self.shooter.labels[
                            'setup'][self.game.config['lang']][6])
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
            l = self.shooter.labels['standard-line'][self.game.config['lang']]
            l_w = self.metrics['status-line'].width(l)
            l_x = (ARENA_WIDTH - l_w) // 2
            self.painter.setFont(self.fonts['help'])
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(l_x + 5, 1050, l)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(l_x, 1045, l)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio, Qt.FastTransformation))

    def paint_help(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(painter)
        e = self.shooter.labels['help']['title'][self.game.config['lang']]
        e_w = self.metrics['logo'].width(e)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(
            e_x + 5,
            155,
            e)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(
            e_x,
            150,
            self.shooter.labels['help']['title'][self.game.config['lang']])
        x = 100
        for player in self.shooter.images['enemies']:
            self.painter.drawPixmap(x, 475, player)
            x += 20 + player.width()
        e = self.shooter.labels['standard-line'][self.game.config['lang']]
        e_w = self.metrics['status-line'].width(e)
        e_x = (ARENA_WIDTH - e_w) // 2
        # Help text here:
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.setFont(self.fonts['help'])
        self.painter.drawText(100, 250, self.shooter.labels['help'][
            self.game.config['lang']][0])
        self.painter.drawText(100, 400, self.shooter.labels['help'][
            self.game.config['lang']][1])
        self.painter.drawText(100, 600, self.shooter.labels['help'][
            self.game.config['lang']][2])
        self.painter.drawPixmap(100, 650, self.shooter.images['boss'])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 400, self.shooter.labels['help'][
            self.game.config['lang']][3])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 480, self.shooter.labels['help'][
            self.game.config['lang']][4])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 560, self.shooter.labels['help'][
            self.game.config['lang']][5])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 640, self.shooter.labels['help'][
            self.game.config['lang']][6])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 720, self.shooter.labels['help'][
            self.game.config['lang']][7])
        self.painter.drawText(ARENA_WIDTH // 2 + 250, 800, self.shooter.labels['help'][
            self.game.config['lang']][8])
        self.painter.drawText(e_x + 5, 1050, e)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(95, 245, self.shooter.labels['help'][
            self.game.config['lang']][0])
        self.painter.drawText(95, 395, self.shooter.labels['help'][
            self.game.config['lang']][1])
        self.painter.drawText(95, 595, self.shooter.labels['help'][
            self.game.config['lang']][2])
        self.painter.drawPixmap(100, 650, self.shooter.images['boss'])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 395, self.shooter.labels['help'][
            self.game.config['lang']][3])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 475, self.shooter.labels['help'][
            self.game.config['lang']][4])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 555, self.shooter.labels['help'][
            self.game.config['lang']][5])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 635, self.shooter.labels['help'][
            self.game.config['lang']][6])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 715, self.shooter.labels['help'][
            self.game.config['lang']][7])
        self.painter.drawText(ARENA_WIDTH // 2 + 245, 795, self.shooter.labels['help'][
            self.game.config['lang']][8])
        self.painter.drawText(e_x, 1045, e)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_player(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(QPen(self.shooter.colors['textback'], 2, Qt.SolidLine))
        e = self.shooter.labels['player']['title'][self.game.config['lang']]
        we = self.metrics['logo'].width(e)
        self.painter.drawText((ARENA_WIDTH - we) // 2 + 5 , 155, e)
        self.painter.setPen(QPen(self.shooter.colors['logofront'], 2, Qt.SolidLine))
        self.painter.drawText((ARENA_WIDTH - we) // 2, 150, e)
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawPixmap(
            ARENA_WIDTH / 4 - self.shooter.images['icons']['prev'].width() // 2,
            600 - self.shooter.images['icons']['prev'].height() // 2,
            self.shooter.images['icons']['prev'])
        self.painter.drawPixmap(
            ARENA_WIDTH / 2 - self.shooter.images['big_players'][self.game.player_index].width() // 2,
            600 - self.shooter.images['big_players'][self.game.player_index].height() // 2,
            self.shooter.images['big_players'][self.game.player_index]
        )
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
        l = self.shooter.labels['player']['line1'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 995, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 990, l)
        l = self.shooter.labels['player']['line2'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l)
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_about(self):
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
        label = self.shooter.labels['about']['title'][self.game.config['lang']]
        label_w = self.metrics['logo'].width(label)
        label_x = (ARENA_WIDTH - label_w) // 2
        self.painter.drawText(label_x + 5, 155, label)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(label_x, 150, label)
        self.painter.setFont(self.fonts['help'])
        c = 0
        for item in self.shooter.labels['about'][self.game.config['lang']]:
            self.painter.setPen(self.shooter.pens['textback'])
            self.painter.drawText(105, 300 + c * 60 + 5, item)
            self.painter.setPen(self.shooter.pens['textfront'])
            self.painter.drawText(100, 300 + c * 60, item)
            c += 1
        label_s = self.shooter.labels['standard-line'][self.game.config['lang']]
        label_w = self.metrics['status-line'].width(label_s)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_newscore(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        self.painter.setFont(self.fonts['logo'])
        e = self.shooter.labels['newscore']['title'][self.game.config['lang']]
        e_w = self.metrics['logo'].width(e)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(
            e_x + 5,
            205,
            e)
        self.painter.setPen(self.shooter.pens['logofront'])
        self.painter.drawText(
            e_x,
            200,
            e
        )
        wx = self.metrics['logo'].width("W")
        wh = self.metrics['logo'].height()
        wy = (MAX_NICK_LEN + 1) * (wx + 30)
        x0 = (ARENA_WIDTH - wy) // 2
        self.painter.setPen(self.shooter.pens['textback'])

        cur = len(self.game.nick)

        for i in range(MAX_NICK_LEN + 1):
            try:
                letter = self.game.nick[i]
                self.painter.drawText(x0 + i * (wx + 30) + 20,
                            685,
                            letter)
            except IndexError:
                pass
            if i == cur and self.game.newscore_counter == 0:
                r = QRect(x0 + cur * (wx + 30) + 5 + 15,
                          700 - wh + 5,
                          wx,
                          wh)
                self.painter.fillRect(r, QBrush(self.shooter.colors['textback']))
        self.painter.setPen(self.shooter.pens['logofront'])
        for i in range(MAX_NICK_LEN + 1):
            try:
                letter = self.game.nick[i]
                self.painter.drawText(x0 + i * (wx + 30) + 15,
                            680,
                            letter)
            except IndexError:
                pass
            if i == cur and self.game.newscore_counter == 0:
                r = QRect(x0 + cur * (wx + 30) + 15,
                            700 - wh,
                            wx,
                            wh)
                self.painter.fillRect(r, self.shooter.brushes['logofront'])
        # Status lines:
        l = self.shooter.labels['newscore']['line1'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 995, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 990, l)
        l = self.shooter.labels['newscore']['line2'][self.game.config['lang']]
        l_w = self.metrics['status-line'].width(l)
        l_x = (ARENA_WIDTH - l_w) // 2
        self.painter.setFont(self.fonts['help'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(l_x + 5, 1050, l)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(l_x, 1045, l)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_game_init(self):
        pass  # Nothing to paint

    def paint_game_prepare(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        # Movables
        for movable in self.game.movables:
            movable.paint(self.painter)
            # Smoke
            if movable.etype in self.shooter.smoke_spots:
                spots = self.shooter.smoke_spots[movable.etype]
                smoke = self.shooter.images['smokes'][self.game.smoke_counter]
                for spot in spots:
                    x, y = spot
                    x += movable.x - smoke.width()
                    y += movable.y - smoke.height()
                    self.painter.drawPixmap(x, y, smoke)

        self.game.player.paint(self.painter)
        level_text = self.shooter.labels[
                         'game']['level-x'][self.game.config['lang']] % {
                         'l': self.game.level + 1}
        x2 = (ARENA_WIDTH - self.metrics[
            'get-ready'].width(level_text)) // 2
        self.painter.setFont(self.fonts['get-ready'])
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(x2 + 5, 405, level_text)
        x3 = 0
        if self.game.get_ready > 0:
            self.painter.setFont(self.fonts['logo'])
            x3 = (ARENA_WIDTH - self.metrics['logo'].width(
                "%(f)d" % {'f': self.game.get_ready})) // 2
            self.painter.drawText(x3 + 5, 605, "%(f)d" % {'f': self.game.get_ready})
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.setFont(self.fonts['get-ready'])
        self.painter.drawText(x2, 400, level_text)
        if self.game.get_ready > 0:
            self.painter.setFont(self.fonts['logo'])
            self.painter.drawText(x3, 600, "%(f)d" % {'f': self.game.get_ready})
        self.paint_bottom_bar(self.painter)
        # ... dotąd
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    @log_usage
    def update_pixmap_play(self, painter):
        """
        Prepare common bitmap for Play board
        (pause and killed events will reuse this)
        :param painter: -- QPainter to draw by
        :return: None
        """
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(painter)
        # Drops
        # (drops before movables)
        for drop in self.game.drops:
            drop.paint(painter)
        # Movables
        for movable in self.game.movables:
            movable.paint(painter)
            # Smoke
            if movable.etype in self.shooter.smoke_spots:
                spots = self.shooter.smoke_spots[movable.etype]
                smoke = self.shooter.images['smokes'][self.game.smoke_counter]
                for spot in spots:
                    x, y = spot
                    x += movable.x - smoke.width()
                    y += movable.y - smoke.height()
                    painter.drawPixmap(x, y, smoke)
        # IceBoxes:
        for icebox in self.game.iceboxes:
            icebox.paint(painter)
        # Bombs
        for bomb in self.game.bombs:
            bomb.paint(painter)
        # Medkids
        for medkit in self.game.medkits:
            medkit.paint(painter)
        # LightBalls
        for lightball in self.game.lightballs:
            lightball.paint(painter)
        # TNTs
        for tnt in self.game.tnts:
            tnt.paint(painter)
        # Shields
        for shield in self.game.shields:
            shield.paint(painter)
        # Meteorites
        for meteorite in self.game.meteorites:
            meteorite.paint(painter)
        # Player
        self.game.player.paint(painter)
        if self.game.shield_timer > 0:
            painter.fillRect(QRect(self.game.player.shieldx,
                                   self.game.player.shieldy,
                                   self.game.player.shieldw,
                                   self.game.player.shieldh), QBrush(QColor(75, 100, 67, 96)))
            painter.setPen(QPen(QColor(34, 97, 13, 127), 2, Qt.DashLine))
            painter.drawRect(QRect(self.game.player.shieldx,
                                   self.game.player.shieldy,
                                   self.game.player.shieldw,
                                   self.game.player.shieldh))
        # Enemies
        self.game.enemymanager.paint(painter)
        # Missiles
        self.paint_missiles(painter)
        # Firemissiles
        for firemissile in self.game.firemissiles:
            firemissile.paint(painter)
        # Boss
        if self.game.boss:
            self.game.boss.paint(painter)
        # Explosions
        for explosion in self.game.explosions:
            explosion.paint(painter)
        self.paint_bottom_bar(painter)
        # ... dotąd

    @log_usage
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

    @log_usage
    def paint_game_play(self):
        """
        Paint Play board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        self.update_pixmap_play(self.painter)
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio, Qt.FastTransformation))

    def paint_game_paused(self):
        """
        Paint Paused board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        self.update_pixmap_play(self.painter)
        self.painter.setFont(self.fonts['logo'])
        t = self.shooter.labels['awaiting']['paused'][self.game.config['lang']]
        t_w = self.metrics['logo'].width(t)
        t_x = (ARENA_WIDTH - t_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(t_x + 5, 505, t)
        self.painter.setPen(self.shooter.pens['logofront2'])
        self.painter.drawText(t_x, 500, t)
        self.painter.setFont(self.fonts['menu'])
        e = self.shooter.labels['awaiting']['enter'][self.game.config['lang']]
        e_w = self.metrics['menu'].width(e)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(e_x + 5, 655, e)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(e_x, 650, e)
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_game_killed(self):
        """
        Paint Killed board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        self.update_pixmap_play(self.painter)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['textback'])
        t = self.shooter.labels['awaiting']['killed'][self.game.config['lang']]
        t_w = self.metrics['logo'].width(t)
        t_x = (ARENA_WIDTH - t_w) // 2
        self.painter.drawText(t_x + 5, 505, t)
        self.painter.setPen(self.shooter.pens['logofront2'])
        self.painter.drawText(t_x, 500, t)
        self.painter.setFont(self.fonts['menu'])
        e = self.shooter.labels['awaiting']['enter'][self.game.config['lang']]
        e_w = self.metrics['menu'].width(e)
        e_x = (ARENA_WIDTH - e_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.drawText(e_x + 5, 655, e)
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(e_x, 650, e)
        # dotąd...
        self.painter.end()
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    @log_usage
    def paint_game_congrats(self):
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        x = self.shooter.labels['gameover']['win'][self.game.config['lang']]
        wx = self.metrics['logo'].width(x)
        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(QPen(self.shooter.colors['textback'], 2, Qt.SolidLine))
        self.painter.drawText((ARENA_WIDTH - wx) // 2 + 5,
                    305,
                    x)
        self.painter.setPen(QPen(self.shooter.colors['logofront'], 2, Qt.SolidLine))
        self.painter.drawText((ARENA_WIDTH - wx) // 2,
                    300,
                    x)
        self.painter.drawPixmap(
            (ARENA_WIDTH - self.shooter.images['indicators']['cup'].width()) // 2,
            400,
            self.shooter.images['indicators']['cup'])
        # Status line
        label_s = self.shooter.labels['standard-line'][self.game.config['lang']]
        label_w = self.metrics['status-line'].width(label_s)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))

    def paint_game_over(self):
        """
        Paint Game Over board
        :return: None
        """
        self.canvas.fill(self.shooter.colors['background'])
        self.painter.begin(self.canvas)
        # Rysować odtąd...
        for star in self.game.stars:
            star.paint(self.painter)
        e = self.shooter.labels['gameover']['title'][self.game.config['lang']]
        f = self.shooter.labels['gameover']['description'][self.game.config['lang']]
        g = self.shooter.labels['gameover']['description2'][self.game.config['lang']]
        h = self.shooter.labels['gameover']['description3'][self.game.config['lang']]
        we = self.metrics['logo'].width(e)
        wf = self.metrics['menu'].width(f)
        wg = self.metrics['status-line'].width(g)
        wh = self.metrics['status-line'].width(h)
        label_s = self.shooter.labels['standard-line'][self.game.config['lang']]
        label_w = self.metrics['status-line'].width(label_s)
        label_x = (ARENA_WIDTH - label_w) // 2
        self.painter.setPen(self.shooter.pens['textback'])
        self.painter.setFont(self.fonts['logo'])
        self.painter.drawText(
            (ARENA_WIDTH - we) // 2 + 5,
            ARENA_HEIGHT // 3 + 5,
            e)
        self.painter.setFont(self.fonts['menu'])
        self.painter.drawText(
            (ARENA_WIDTH - wf) // 2 + 5,
            ARENA_HEIGHT // 3 + 205,
            f)
        self.painter.setFont(self.fonts['status-line'])
        self.painter.drawText(
            (ARENA_WIDTH - wg) // 2 + 5,
            ARENA_HEIGHT // 3 + 405,
            g)
        self.painter.drawText(
            (ARENA_WIDTH - wh) // 2 + 5,
            ARENA_HEIGHT // 3 + 505,
            h)
        self.painter.drawText(label_x + 5, 1055, label_s)

        self.painter.setFont(self.fonts['logo'])
        self.painter.setPen(self.shooter.pens['logofront'])

        self.painter.drawText(
            (ARENA_WIDTH - we) // 2,
            ARENA_HEIGHT // 3,
            e)
        self.painter.setFont(self.fonts['menu'])
        self.painter.setPen(self.shooter.pens['textfront'])
        self.painter.drawText(
            (ARENA_WIDTH - wf) // 2,
            ARENA_HEIGHT // 3 + 200,
            f)
        self.painter.setFont(self.fonts['status-line'])
        self.painter.drawText(
            (ARENA_WIDTH - wg) // 2,
            ARENA_HEIGHT // 3 + 400,
            g)
        self.painter.drawText(
            (ARENA_WIDTH - wh) // 2,
            ARENA_HEIGHT // 3 + 500,
            h)
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
        self.setPixmap(self.canvas.scaled(self.full_w, self.full_h, Qt.IgnoreAspectRatio))


class SpaceShooter(QApplication):
    def __init__(self, args: list):
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
        self.labels = {
            'title': 'SPACESHOOTER',
            'standard-line': {
                'pl': '(UZYJ ESC LUB Q, ABY OPUSCIC TEN EKRAN)',
                'en': '(USE ESC OR Q TO LEAVE THIS SCREEN)'
            },
            'menu': {
                'title': {
                    'pl': 'SPACESHOOTER',
                    'en': 'SPACESHOOTER'
                },
                'pl': [
                    'NOWA GRA',
                    'OPCJE',
                    'NAJLEPSZE WYNIKI',
                    'USTAWIENIA',
                    'POMOC',
                    'O PROGRAMIE',
                    'KONIEC'
                ],
                'en': [
                    'NEW GAME',
                    'OPTIONS',
                    'HISCORES',
                    'SETUP',
                    'HELP',
                    'ABOUT',
                    'QUIT'
                ]
            },
            'game': {
                'level-x': {
                    'pl': "WITAJ NA POZIOMIE %(l)d",
                    'en': "WELCOME TO LEVEL %(l)d"
                },
            },
            'options': {
                'title': {
                    'pl': 'OPCJE',
                    'en': 'OPTIONS'
                },
                'line1': {
                    'pl': '(UZYJ ENTER, BY WYBRAC POZIOM',
                    'en': '(USE ENTER TO SELECT A LEVEL'
                },
                'line2': {
                    'pl': 'ESC LUB Q, BY OPUSCIC TEN EKRAN)',
                    'en': 'ESC OR Q TO LEAVE THIS SCREEN)'
                },
                'pl': [
                    "TRYB LATWY",
                    "TRYB NORMALNY",
                    "TRYB HARDKOROWY",
                    "NIESMIERTELNOSC"
                ],
                'en': [
                    "EASY MODE",
                    "NORMAL MODE",
                    "HARDCORE MODE",
                    "IMMORTAL MODE"
                ],
            },
            'hiscores': {
                'title': {
                    'en': 'HISCORES',
                    'pl': 'NAJLEPSI'
                },
            },
            'newscore': {
                'title': {
                    'en': 'NEW SCORE',
                    'pl': 'NOWY REKORD'
                },
                'line1': {
                    'pl': '(WPIS SWOJE IMIE I WCISNIJ ENTER',
                    'en': '(ENTER YOUR NAME AND PRESS ENTER'
                },
                'line2': {
                    'pl': 'LUB UZYJ ESC BY OPUSCIC TEN EKRAN)',
                    'en': 'OR USE ESC TO LEAVE THIS SCREEN)'
                }
            },
            'setup': {
                'title': {
                    'en': 'SETUP',
                    'pl': 'USTAWIENIA',
                },
                'status-line': {
                    'pl': '',
                    'en': ''
                },
                'enter-lead': {
                    'en': "HIT A KEY YOU WANT TO SET",
                    'pl': "NACISNIJ KLAWISZ, KTORY CHCESZ USTAWIC"
                },
                'display-lead': {
                    'en': "HIT F1 TO RECONFIGURE KEYS",
                    'pl': "WCISNIJ F1 BY SKONFIGUROWAC KLAWISZE"
                },
                'enter-status': {
                    'en': "(HIT ENTER TO ACCEPT OR ESC TO DISCARD CONFIGURATION)",
                    'pl': "(WCISNIJ ENTER BY ZATWIERDZIC LUB ESC BY ANULOWAC)"
                },
                'pl': [
                    'W LEWO:',
                    'W PRAWO:',
                    'W GORE:',
                    'W DOL:',
                    'STRZAL:',
                    'BOMBA:',
                    'TNT:'
                ],
                'en': [
                    'LEFT:',
                    'RIGHT:',
                    'UP:',
                    'DOWN:',
                    'FIRE:',
                    'BOMB:',
                    'TNT:'
                ],
            },
            'player': {
                'title': {
                    'en': 'SELECT YOUR SHIP',
                    'pl': 'WYBIERZ STATEK',
                },
                'line1': {
                    'pl': '(UZYJ ←, → I ENTER BY WYBRAC',
                    'en': '(USE ←, → AND ENTER TO SELECT,'
                },
                'line2': {
                    'pl': 'ORAZ ESC LUB Q BY OPUSCIC TEN EKRAN)',
                    'en': 'AND ESC OR Q TO LEAVE THIS SCREEN)'
                }
            },
            'help': {
                'title': {
                    'en': "HELP",
                    'pl': "POMOC"
                },
                'en': ['BEAT THE HORDE OF ENEMY SPACESHIPS AND THEIR BOSS AT THE END!',
                       'ENEMIES',
                       'BOSS'
                       '',
                       'USEFUL ARTIFACTS',
                       'HEALTH POINTS',
                       'SHIELD',
                       'TNT',
                       'FREEZE',
                       'LIGHTBALLS'
                       ],
                'pl': ['POKONAJ HORDE WROGICH STATKOW, A NA KONCU ICH BOSSA!',
                       'WROGOWIE',
                       'BOSS',
                       'POMOCNE ARTEFAKTY',
                       'PUNKTY ZDROWIA',
                       'TARCZA',
                       'TNT',
                       'MROZ',
                       'KULE SWIATLA'
                       ],
            },
            'about': {
                'title': {
                    'en': "ABOUT",
                    'pl': "O PROGRAMIE"
                },
                'en': [
                    "SIMPLE SHOOTER GAME TO PASS THE TIME",
                    "WRITTEN IN PYQT",
                    "AUTHOR: MARCIN BIELEWICZ",
                    "(C) 2021-?",
                    "LICENSED UNDER GNU GPL",
                    "",
                    "SOURCE CODE WRITTEN IN EMACS, ALL GRAPHICS MADE IN INKSCAPE",
                    "",
                    "MORE AT: HTTPS://PRINTF.PL/SPACESHOOTER-EN"
                ],
                'pl': [
                    "PROSTA STRZELANKA DLA ZABICIA CZASU",
                    "NAPISANA W PYQT",
                    "AUTOR: MARCIN BIELEWICZ",
                    "(C) 2021-?",
                    "LICENCJA: GNU GPL",
                    "",
                    "KOD ZRODLOWY POWSTAL W EDYTORZE EMACS, A GRAFIKI W INKSCAPE",
                    "",
                    "WIECEJ NA: HTTPS://PRINTF.PL/SPACESHOOTER-PL"
                ]
            },
            'awaiting': {
                'killed': {
                    'pl': 'NIESTETY!',
                    'en': 'OOPS!'
                },
                'paused': {
                    'pl': 'GRA WSTRZYMANA',
                    'en': 'PAUSED'
                },
                'enter': {
                    'pl': 'NACISNIJ ENTER BY KONTYNUOWAC',
                    'en': 'PRESS ENTER TO CONTINUE'
                }
            },
            'gameover': {
                'title': {
                    'en': 'GAME OVER',
                    'pl': 'GAME OVER'
                },
                'description': {
                    'en': "THAT'S ALL, FOLKS!",
                    'pl': 'KUP SE ROWER'
                },
                'description2': {
                    'en': 'UNFORTUNATELY, YOU LOST',
                    'pl': 'NIESTETY, NIE UDALO SIE WYGRAC'
                },
                'description3': {
                    'en': 'BETTER LUCK NEXT TIME!',
                    'pl': 'POWODZENIA NASTEPNYM RAZEM!'
                },
                'win': {
                    'en': 'CONGRATULATIONS!',
                    'pl': 'GRATULACJE!'
                }
            }
        }
        self.colors = {
            'background': QColor("#09275b"),
            'textback': QColor(12, 12, 12, 127),
            'logofront': QColor(250, 79, 141, 127),
            'logofront2': QColor(240, 161, 234, 127),
            'textfront': QColor(147, 218, 255, 127)
        }
        self.pens = {
            'textback': QPen(self.colors['textback'], 2, Qt.SolidLine),
            'textfront': QPen(self.colors['textfront'], 2, Qt.SolidLine),
            'logofront': QPen(self.colors['logofront'], 2, Qt.SolidLine),
            'logofront2': QPen(self.colors['logofront2'], 2, Qt.SolidLine)
        }
        self.brushes = {
            'bottom-bar': QBrush(QColor(47, 47, 47)),
            'logofront': QBrush(self.colors['logofront'])
        }
        self.smoke_spots = {
            MovableType.FABRYKA1: [(124, 80), (246, 80), (322, 0)],
            MovableType.FABRYKA2: [(95, 130), (165, 0), (253, 0), (328, 0)],
            MovableType.FABRYKA3: [(232, 0)]
        }
        self.images = {
            'star': QPixmap("images/star.png"),
            'players': [
                QPixmap("images/aplayer0.png"),
                QPixmap("images/aplayer1.png"),
                QPixmap("images/aplayer2.png"),
                QPixmap("images/asterowiec.png")
            ],
            'big_players': [
                QPixmap("images/player0.png"),
                QPixmap("images/player2.png"),
                QPixmap("images/player3.png"),
                QPixmap("images/sterowiec.png")
            ],
            'movables': {
                MovableType.DZIALO: QPixmap("images/dzialo.png"),
                MovableType.DOM1: QPixmap("images/dom1.png"),
                MovableType.DOM2: QPixmap("images/dom2.png"),
                MovableType.DOM3: QPixmap("images/dom3.png"),
                MovableType.FABRYKA1: QPixmap("images/fabryka1.png"),
                MovableType.FABRYKA2: QPixmap("images/fabryka2.png"),
                MovableType.FABRYKA3: QPixmap("images/fabryka3.png"),
                MovableType.WIEZOWIEC1: QPixmap("images/wiezowiec1.png"),
                MovableType.WIEZOWIEC2: QPixmap("images/wiezowiec2.png"),
                MovableType.WIEZOWIEC3: QPixmap("images/wiezowiec3.png")
            },
            'smokes': [
                QPixmap("images/smoke-1.png"),
                QPixmap("images/smoke-2.png"),
                QPixmap("images/smoke-3.png"),
                QPixmap("images/smoke-4.png")
            ],
            'enemies': [
                QPixmap("images/enemy4.png"),
                QPixmap("images/enemy5.png"),
                QPixmap("images/enemy6.png"),
                QPixmap("images/enemy7.png"),
                QPixmap("images/enemy8.png"),
                QPixmap("images/enemy9.png"),
            ],
            'explosions': [
                QPixmap("images/explosion-1.png"),
                QPixmap("images/explosion-2.png"),
                QPixmap("images/explosion-3.png"),
                QPixmap("images/explosion-2.png"),
                QPixmap("images/explosion-1.png"),
            ],
            'missiles': {
                MissileType.FROM: QPixmap("images/missile-2.png"),
                MissileType.TO: QPixmap("images/missile-1.png"),
                MissileType.TO_NW: QPixmap("images/missile-3.png"),
                MissileType.TO_SW: QPixmap("images/missile-4.png"),
                MissileType.TO_NWW: QPixmap("images/missile-5.png"),
                MissileType.TO_SWW: QPixmap("images/missile-6.png")
            },
            'icons': {
                'pl': QPixmap("images/flag_pl.png"),
                'en': QPixmap("images/flag_en.png"),
                'next': QPixmap("images/next.png"),
                'prev': QPixmap("images/prev.png")
            },
            'boss': QPixmap("images/pzm.png"),
            'indicators': {
                'red': QPixmap('images/indicator_red.png'),
                'green': QPixmap('images/indicator_green.png'),
                'yellow': QPixmap('images/indicator_yellow.png'),
                'black': QPixmap('images/indicator_black.png'),
                'player': QPixmap('images/player_indicator.png'),
                'shield': QPixmap('images/shield-green.png'),
                'tnt': QPixmap('images/tnt.png'),
                'light-ball': QPixmap('images/light_ball.png'),
                'frozen-box': QPixmap('images/frozen_box.png'),
                'medkit': QPixmap('images/apteczka.png'),
                'drop': QPixmap('images/drop.png'),
                'bomb': QPixmap('images/bomba.png'),
                'cup': QPixmap('images/cup')
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
            'player-move-event': QTimer(),
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
            'player-move-event': self.player_move_event,
            'bomb-timer': self.bomb_timer,
            'missile-timer': self.missile_timer,
            'smoke-timer': self.smoke_timer
        }
        for name in self.timers:
            self.timers[name].timeout.connect(self.timer_handlers[name])
        self.game = Game(self)

    def newscore_event(self):
        self.game.newscore_event()

    def game_enemies_event(self):
        self.game.enemies_event()

    def game_events_event(self):
        self.game.events_event()

    def game_welcome_event(self):
        self.game.welcome_event()

    def game_movable_update_event(self):
        self.game.movable_update_event()

    def game_update_event(self):
        self.game.game_update_event()

    def game_shield_event(self):
        self.game.shield_event()

    def game_light_event(self):
        self.game.light_event()

    def game_get_ready_event(self):
        self.game.get_ready_event()

    def game_stars_event(self):
        self.game.stars_update_event()

    def game_paint_event(self):
        self.game.game_paint_event()

    def game_counter_event(self):
        self.game.game_counter_event()

    def game_freeze_event(self):
        self.game.freeze_event()

    def setup_enter_event(self):
        self.game.setup_enter_event()

    def player_move_event(self):
        self.game.player_move_event()

    def bomb_timer(self):
        self.game.bomb_timer()

    def missile_timer(self):
        self.game.missile_timer()

    def smoke_timer(self):
        self.game.smoke_timer()


if __name__ == "__main__":
    fixed = False
    try:
        fixed = (sys.argv[1] == "-f")
    except IndexError:
        pass
    random.seed()
    shooter = SpaceShooter(sys.argv)
    shooter.game = Game(shooter)
    window = Controller(shooter)
    window.game = shooter.game
    shooter.window = window
    arena = Arena(window)
    arena.shooter = shooter
    shooter.game.arena = arena
    window.setCentralWidget(arena)
    arena.window = window
    if fixed:
        window.showFullScreen()
    else:
        window.setFixedSize(ARENA_WIDTH, ARENA_HEIGHT)
        window.show()
    shooter.game.change_board(Board.WELCOME)
    sys.exit(shooter.exec_())
