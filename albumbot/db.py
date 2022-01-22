from tinydb import TinyDB
from albumbot.config import config

db = None


def setup():
    global db
    db = TinyDB(config.DB_PATH)
