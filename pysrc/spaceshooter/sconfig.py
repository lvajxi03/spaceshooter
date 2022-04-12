#!/usr/bin/env python

"""
SpaceShooter configuration
"""

import json
from spaceshooter.stypes import Key, UserInput, Options
from spaceshooter.sdefs import DEFAULT_FONT


class ShooterConfig:
    """
    Basic program configuration
    """
    def __init__(self, **kwargs):
        self.filename = None
        self.forcefont = False
        if 'filename' in kwargs:
            self.filename = kwargs['filename']
        self.db = {
            'keys': {
                UserInput.LEFT: Key.KEY_LEFT,
                UserInput.RIGHT: Key.KEY_RIGHT,
                UserInput.TOP: Key.KEY_TOP,
                UserInput.BOTTOM: Key.KEY_BOTTOM,
                UserInput.FIRE: Key.KEY_SPACE,
                UserInput.BOMB: Key.KEY_B,
                UserInput.TNT: Key.KEY_T},
            'lang': 'en',
            'hiscores': [],
            'lastmode': Options.NORMAL,
            'lastfont': DEFAULT_FONT}
        font = kwargs.get('lastfont', None)
        if font:
            self.forcefont = True
            self.db['lastfont'] = font

    def __getitem__(self, item):
        """
        Square brackets operator (indexing) - getter
        """
        return self.db.get(item, None)

    def __setitem__(self, key, value):
        """
        Square brackets operator (indexing) - setter
        """
        self.db[key] = value

    def get_key(self, keyname: UserInput, fallback=None) -> Key:
        """
        Get a key associated to a user input
        :param keyname: user input control
        :param fallback: default value
        :return: associated key
        """
        if keyname in self.db['keys']:
            return self.db['keys'][keyname]
        return fallback

    def set_key(self, keyname: UserInput, keyvalue: Key):
        """
        Assign a key to specified user input control
        :param keyname: user input control
        :param keyvalue: associated key
        :return:
        """
        if keyvalue:
            self.db['keys'][keyname] = keyvalue
        else:
            del self.db['keys'][keyname]

    def read(self):
        """
        Read from a file, if associated
        :return: None
        """
        if self.filename:
            self.read_from(self.filename)

    def read_from(self, filename):
        """
        Read configuration from a file
        :param filename: file to read from
        :return: None
        """
        if not self.filename:
            self.filename = filename
        content = "{}"
        try:
            with open(filename, encoding="UTF-8") as fh:
                content = fh.read()
        except IOError:
            pass  # Read error -- let's go with defaults
        j = json.loads(content)
        for i in ['hiscores', 'lastmode', 'lang']:
            try:
                self.db[i] = j[i]
            except KeyError:
                pass
        if not self.forcefont:
            try:
                self.db['lastfont'] = j['lastfont']
            except KeyError:
                pass
        self.db['hiscores'].sort(reverse=True, key=lambda y: y[1])
        self.db['hiscores'] = self.db['hiscores'][:10]
        if 'keys' in j:
            for key in j['keys']:
                self.db['keys'][key] = Key(int(j['keys'][key]))

    def save(self):
        """
        Save to a file, if associated
        :return:
        """
        if self.filename:
            self.save_as(self.filename)

    def save_as(self, filename):
        """
        Save configuration to a file
        :param filename: file to save to
        :return: None
        """
        if not self.filename:
            self.filename = filename
        with open(filename, "w", encoding="UTF-8") as fh:
            json.dump(self.db, fh)

    def is_hiscore(self, score: int):
        """
        Check if score can be added to hiscore list
        :param score: Score to be checked
        :return: True if score can be added to hiscore list, False otherwise
        """
        try:
            return score > self.db['hiscores'][9][1]
        except IndexError:
            return True  # yes, no scores added so far

    def add_hiscore(self, name, score):
        """
        Append new hiscore result
        :param name: player name
        :param score: player score
        :return: None
        """
        self.db['hiscores'].append([name, score])
        self.db['hiscores'].sort(reverse=True, key=lambda x: x[1])
        self.db['hiscores'] = self.db['hiscores'][:10]
