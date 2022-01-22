import logging

from rich.logging import RichHandler
from rich.traceback import install

from albumbot import bot
from albumbot.config import Config

# rich exception handler
install(show_locals=True)

config = Config.config()

# setup logging
logging.basicConfig(level="DEBUG", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("albumBot")
for logger in ("praw", "requests", "urllib3", "spotipy.client", "prawcore"):
    logging.getLogger(logger).setLevel(config.LOG_LEVEL)


if __name__ == "__main__":
    log.debug(config)

    if config.FIRST_RUN:
        bot.first_run()
    else:
        bot.run()
