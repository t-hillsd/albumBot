import logging
from typing import List

import praw
from tinydb import Query
from yaspin import yaspin

from albumbot.config import Config
from albumbot.db import DB
from albumbot.music import spotifyReleases
from albumbot.music.spotifyReleases import AlbumRelease

log = logging.getLogger("albumBot")
config = Config.config()
db = DB.db()


def get_unseen_releases() -> List[AlbumRelease]:
    unseen_releases = list(filter(is_unseen_p, spotifyReleases.get()))
    if not unseen_releases:
        log.debug("No unseen releases.")

    return unseen_releases


def is_unseen_p(release: AlbumRelease) -> bool:
    Album = Query()
    album = db.search(Album.id == release.id)
    if not album:
        return True
    return False


def mark_as_processed(releases: List[AlbumRelease]) -> None:
    db.insert_multiple(
        [
            {
                "id": release.id,
            }
            for release in releases
        ]
    )


def run() -> None:
    r = praw.Reddit(
        client_id=config.REDDIT_ID,
        client_secret=config.REDDIT_SECRET,
        user_agent=config.USER_AGENT,
        username=config.REDDIT_USER,
        password=config.REDDIT_PASS,
    )

    with yaspin(color="yellow"):
        new = get_unseen_releases()

    for release in new:
        release.log()
        submission = r.subreddit(config.SUBREDDIT).submit(
            url=release.link,
            title=f"[FRESH] {release.artists} - {release.name}",
        )
        db.insert({"id": release.id})
        log.debug(
            {
                "album": release.name,
                "link": submission.url,
                "comments": f"https://reddit.com{submission.permalink}",
            }
        )


def first_run() -> None:
    with yaspin(color="yellow"):
        new = get_unseen_releases()
    for release in new:
        release.log()

    mark_as_processed(new)
    log.debug("First run detected. Posting nothing. Marking all new albums as seen to prevent future posting.")
