import os
from setuptools import setup

"""
Setup module for packaging
(required by setuptools)
"""


def read(file_name):
    """
    Read file content.
    Utility function for setup, below
    :param file_name: Name of the file to read
    :return: file content (string)
    """
    return open(
        os.path.join(
            os.path.dirname(__file__), file_name)).read()


setup(
    name="spaceshooter",
    version="0.0.6",
    author="Marcin Bielewicz",
    author_email="marcin.bielewicz@gmail.com",
    description="Simple spaceshooter game, written in PyQt",
    license="GPL",
    keywords="pyqt spaceshooter game arcade",
    packages=['spaceshooter'],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://iostream.pl/spaceshooter-en",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ]
)
