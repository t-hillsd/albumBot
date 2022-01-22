import logging
import os.path
from pathlib import Path
from typing import List, Optional

from pydantic import BaseSettings

log = logging.getLogger("albumBot")


class Config(BaseSettings):
    __conf: Optional[BaseSettings] = None

    VERSION: str
    REDDIT_ID: str
    REDDIT_SECRET: str
    REDDIT_USER: str
    REDDIT_PASS: str
    SUBREDDIT: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_RELEASE_COUNTRIES: List[str]
    WANTED_GENRES: List[str]
    LOG_LEVEL: int
    DB_PATH: str

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def USER_AGENT(self) -> str:
        return f"script:albumBot:v{self.VERSION} (by /u/thillsd)"

    @property
    def FIRST_RUN(self) -> bool:
        if not os.path.exists(self.DB_PATH):
            return True
        else:
            return False

    @staticmethod
    def config():
        if Config.__conf is None:  # Read only once, lazy.
            dir = Path(__file__).resolve().absolute().parents[1] / "instance"
            dir.mkdir(exist_ok=True, mode=0o777)
            Config.__conf = Config(DB_PATH=str(dir / "db.json"))
        return Config.__conf
