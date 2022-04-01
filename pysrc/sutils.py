#!/usr/bin/env python

"""
General utilities module
"""


def cycle(my_list):
    """
    Generator that cycles a list
    :param my_list: List to cycle
    :return: Generator handle
    """
    start_at = 0
    while True:
        yield my_list[start_at]
        start_at = (start_at + 1) % len(my_list)
