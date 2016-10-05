import sqlite3
from virtual_score_board.config_manager import ConfigManager


class CredentialsManager(object):
    def __init__(self):
        config = ConfigManager.get_config()