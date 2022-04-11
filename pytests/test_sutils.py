#!/usr/bin/env python

"""
Test sutils module
"""


from sutils import cycle


def test_cycle_1():
    arr = [1, 2, 3, 4, 5]
    gen = cycle(arr)
    result = next(gen)
    assert result == 1
    result = next(gen)
    assert result == 2
