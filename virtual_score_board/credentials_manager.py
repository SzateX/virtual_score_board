from virtual_score_board.db_manager import DBManager, User, Address, PassHash
from sqlalchemy import select


class CredentialsManager(object):
    _instance = None

    @classmethod
    def get_config(cls):
        if cls._instance is None:
            cls._instance = CredentialsManager()
        return cls._instance

    def __init__(self):
        self.db = DBManager.get_connection_manager()
        self.db_session = self.db.session

    def sign_in(self, name, password):
        result = self.db_session.query(User.name, PassHash.pass_hash).join(
            PassHash).filter(User.name == name)
        hashes = []
        for hashed in result:
            hashes.append(hashed)
        result.close()
        if len(hashes) == 0:
            raise Exception
        elif len(hashes) > 1:
            raise Exception
        # return User()
