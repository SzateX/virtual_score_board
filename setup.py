import os
from setuptools import setup, find_packages

setup(
    name="virtual_score_board",
    version="0.0.1",
    author="Jakub Szatkowski",
    author_email="jaksza18@gmail.com",
    description=("A virtual scoreboard for presenting match details."),
    install_requires=['autobahn==0.16.0', 'Twisted==16.4.1',
                      'pytest==3.0.2', 'click==6.6', 'passlib==1.6.5',
                      'sqlalchemy==1.1', 'pymysql==0.7.9'],
    license="MiT",
    keywords="virtual scoreboard score sport",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MiT",
    ]
)