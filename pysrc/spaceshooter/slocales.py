#!/usr/bin/env python

"""
SpaceShooter locales
"""

locales = {
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
            "WRITTEN IN PySide6",
            "AUTHOR: MARCIN BIELEWICZ",
            "(C) 2021-?",
            "LICENSED UNDER GNU GPL",
            "",
            "SOURCE CODE WRITTEN IN EMACS, ALL GRAPHICS MADE IN INKSCAPE",
            "",
            "MORE AT: https://iostream.pl/spaceshooter-en"
        ],
        'pl': [
            "PROSTA STRZELANKA DLA ZABICIA CZASU",
            "NAPISANA W PySide6",
            "AUTOR: MARCIN BIELEWICZ",
            "(C) 2021-?",
            "LICENCJA: GNU GPL",
            "",
            "KOD ZRODLOWY POWSTAL W EDYTORZE EMACS, A GRAFIKI W INKSCAPE",
            "",
            "WIECEJ NA: https://iostream.pl/spaceshooter-pl"
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
