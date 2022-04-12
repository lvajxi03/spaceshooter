#/usr/bin/env python

"""
Test primi module
"""


from spaceshooter.primi import Rect


def test_rect_1():
    """
    Check if a rectangle was created
    :return: None
    """
    rect = Rect(1, 2, 3, 4)
    assert rect.x == 1
    assert rect.y == 2
    assert rect.w == 3
    assert rect.h == 4

def test_rect_2():
    """
    Check if rectangle contains a point
    and does not contains another one.
    :return:
    """
    rect = Rect(1, 2, 5, 6)
    assert rect.contains(3, 3)
    assert not rect.contains(1, 1)
