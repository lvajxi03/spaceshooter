#/usr/bin/env python

"""
Test primi module
"""


from primi import Rect


def test_rect_1():
    r = Rect(1, 2, 3, 4)
    assert r.x == 1
    assert r.y == 2
    assert r.w == 3
    assert r.h == 4

def test_rect_2():
    r = Rect(1, 2, 5, 6)
    assert r.contains(3, 3)
    assert not r.contains(1, 1)
