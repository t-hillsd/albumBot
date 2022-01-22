from tinydb import TinyDB

from albumbot.config import Config


class DB:
    __handle = None

    @staticmethod
    def db():
        if DB.__handle is None:
            DB.__handle = TinyDB(Config.config().DB_PATH)
        return DB.__handle
