import os.path
import logging
import praw
from rich.logging import RichHandler
from rich.traceback import install

# rich exception handler
install(show_locals=True)

# setup config
from albumbot import config

config.setup_config()
from albumbot.config import config

if not os.path.exists(config.DB_PATH):
    FIRST_RUN = True
else:
    FIRST_RUN = False

# setup logging
logging.basicConfig(
    level="DEBUG", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("albumBot")
logging.getLogger("praw").setLevel(config.LOG_LEVEL)
logging.getLogger("requests").setLevel(config.LOG_LEVEL)
logging.getLogger("urllib3").setLevel(config.LOG_LEVEL)
logging.getLogger("spotipy.client").setLevel(config.LOG_LEVEL)
logging.getLogger("prawcore").setLevel(config.LOG_LEVEL)

# setup db
from albumbot import db

db.setup()


if __name__ == "__main__":
    log.debug(config)
    reddit = praw.Reddit(
        client_id=config.REDDIT_ID,
        client_secret=config.REDDIT_SECRET,
        user_agent=config.USER_AGENT,
        username=config.REDDIT_USER,
        password=config.REDDIT_PASS,
    )

    from albumbot import bot

    if FIRST_RUN:
        bot.first_run()
    else:
        bot.run(reddit)
