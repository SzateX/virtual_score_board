from sqlalchemy import create_engine, Table, Column, Integer, \
    String, MetaData, ForeignKey, select
from virtual_score_board.config_manager import ConfigManager


class DBManager(object):
    metadata = MetaData()
    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(80), nullable=False),
                  Column('fullname', String(80)))

    addresses = Table('addresses', metadata, Column('id', Integer,
                                                    primary_key=True),
                      Column('user_id', None, ForeignKey('users.id')),
                      Column('email_address', String(150), nullable=False))

    pass_hashes = Table('pass_hashes', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', None, ForeignKey('users.id')),
                        Column('pass_hash', String(200), nullable=False))

    _instance = None

    @classmethod
    def get_connection_manager(cls):
        if cls._instance is None:
            cls._instance = DBManager()
        return cls._instance

    def __init__(self):
        config = ConfigManager.get_config()
        self.engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(
                                                    config.db_username,
                                                    config.db_password,
                                                    config.mysql_host,
                                                    config.db_name), echo=True)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()


"""db = DBManager()
sel = select([db.users.c.name,
              db.pass_hashes.c.pass_hash]).select_from(db.users.join(
    db.pass_hashes)).where(
    db.users.c.name == "Szatku")
result = db.connection.execute(sel)
for row in result:
    print(row)
result.close()"""
