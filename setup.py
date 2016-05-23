import os
from setuptools import setup, find_packages

setup(
    name = "virtual_score_board",
    version = "0.0.1",
    author = "Jakub Szatkowski",
    author_email = "jaksza18@gmail.com",
    description = ("A virtual scoreboard for presenting match details."),
    install_requires = ['autobahn>=0.12.1', 'Twisted>=15.5.0', 'pytest>=2.8.7', 'click>=6.2', 'passlib>=2.0.0'],
    license = "MiT",
    keywords = "virtual scoreboard score sport",
    packages = find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MiT",
    ]
)