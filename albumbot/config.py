import logging
from pydantic import BaseSettings
from pathlib import Path

log = logging.getLogger("albumBot")

config = None


class Settings(BaseSettings):
    VERSION: str
    REDDIT_ID: str
    REDDIT_SECRET: str
    REDDIT_USER: str
    REDDIT_PASS: str
    SUBREDDIT: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_RELEASE_COUNTRIES: str
    WANTED_GENRES: str
    LOG_LEVEL: int

    class Config:
        env_file = ".env"

    @property
    def USER_AGENT(self):
        return f"script:albumBot:v{self.VERSION} (by /u/thillsd)"

    @property
    def SPOTIFY_RELEASE_COUNTRIES_LIST(self):
        return self.SPOTIFY_RELEASE_COUNTRIES.split(",")

    @property
    def WANTED_GENRES_LIST(self):
        return self.WANTED_GENRES.split(",")

    @property
    def DB_PATH(self):
        dir = Path(__file__).resolve().absolute().parents[1] / "instance"
        dir.mkdir(exist_ok=True, mode=0o777)
        return str(dir / "db.json")


def setup_config():
    global config

    config = Settings()
    log.debug(f"Running with conf: {dict(config)!r}")
