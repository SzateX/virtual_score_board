from sqlalchemy import create_engine, Column, Integer, \
    String, ForeignKey
from virtual_score_board.config_manager import ConfigManager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
Session = sessionmaker()


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    user_id = Column(None, ForeignKey('users.id'), nullable=False)
    email_address = Column(String(150), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


class PassHash(Base):
    __tablename__ = 'pass_hashes'

    id = Column(Integer, primary_key=True)
    user_id = Column(None, ForeignKey('users.id'), nullable=False)
    pass_hash = Column(String(200), nullable=False)

    user = relationship("User", back_populates="pass_hashes")

    def __repr__(self):
        return "<PassHash(pass_hash='%s')>" % self.pass_hash


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(80), nullable=False)
    fullname = Column('fullname', String(80))

    addresses = relationship("Address", order_by = Address.id, back_populates = "user")

    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (
            self.name, self.fullname)


class DBManager(object):
    """users = Table('users', metadata,
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
                        Column('pass_hash', String(200), nullable=False))"""

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
        Base.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session()

print(User.__table__)

db = DBManager()
session = db.session
result = session.query(User.name, PassHash.pass_hash).join(PassHash).filter(
    User.name == "Szatku")
for row in result:
    print(row)


"""sel = select([db.users.c.name,
              db.pass_hashes.c.pass_hash]).select_from(db.users.join(
    db.pass_hashes)).where(
    db.users.c.name == "Szatku")
result = db.connection.execute(sel)
for row in result:
    print(row)
result.close()"""
