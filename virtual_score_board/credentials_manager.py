from virtual_score_board.db_manager import DBManager
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

    def sign_in(self, name, password):
        sel = select([self.db.pass_hashes.c.pass_hash]).select_from(
            self.db.users.join(self.db.pass_hashes)).where(
            self.db.users.c.name == name)
        result = self.db.connection.execute(sel)
        hashes = []
        for hashed in result:
            hashes.append(hashed)
        result.close()
        if len(hashes) == 0:
            raise Exception
        elif len(hashes) > 1:
            raise Exception
        #return User()
