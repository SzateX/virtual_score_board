from sqlalchemy import create_engine, Table, Column, Integer, \
    String, MetaData, ForeignKey
from virtual_score_board.config_manager import ConfigManager


class DBManager(object):
    metadata = MetaData()
    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String, nullable=False),
                  Column('fullname', String))

    addresses = Table('addresses', metadata, Column('id', Integer,
                                                    primary_key=True),
                      Column('user_id', None, ForeignKey('users.id')),
                      Column('email_address', String, nullable=False))

    pass_hashes = Table('pass_hashes', Column('id', Integer, primary_key=True),
                        Column('user_id', None, ForeignKey('users.id')),
                        Column('pass_hash', String, nullable=False))

    _instance = None

    @classmethod
    def get_connection_manager(cls):
        if cls._instance is None:
            cls._instance = DBManager()
        return cls._instance

    def __init__(self):
        config = ConfigManager.get_config()
        engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(
                                                    config.db_username,
                                                    config.db_password,
                                                    config.mysql_host,
                                                    config.db_name))
        self.metadata.create_all(engine)
        engine.connect()



