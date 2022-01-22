from albumbot.music import spotifyReleases
from albumbot.db import db
from tinydb import Query
import logging
from albumbot.config import config
from yaspin import yaspin

log = logging.getLogger("albumBot")


def get_unseen_releases():
    unseen_releases = list(filter(is_unseen_p, spotifyReleases.get()))
    if not unseen_releases:
        log.debug("No unseen releases.")

    return unseen_releases


def is_unseen_p(release):
    Album = Query()
    album = db.search(Album.id == release.id)
    if not album:
        return True


def mark_as_processed(releases):
    db.insert_multiple(
        [
            {
                "id": release.id,
            }
            for release in releases
        ]
    )


def run(r):
    with yaspin(color="yellow") as spinner:
        new = get_unseen_releases()

    for release in new:
        spotifyReleases.debug_print_release(release)
        artists = ", ".join(a.name for a in release.artists)
        submission = r.subreddit(config.SUBREDDIT).submit(
            url=release.external_urls.spotify,
            title=f"[FRESH] {artists} - {release.name}",
        )
        db.insert({"id": release.id})
        log.debug(
            {
                "album": release.name,
                "link": submission.url,
                "comments": f"https://reddit.com{submission.permalink}",
            }
        )


def first_run():
    with yaspin(color="yellow") as spinner:
        new = get_unseen_releases()
    for release in new:
        spotifyReleases.debug_print_release(release)

    mark_as_processed(new)
    log.debug(
        "First run detected. Posting nothing. Marking all new albums as seen to prevent future posting."
    )
