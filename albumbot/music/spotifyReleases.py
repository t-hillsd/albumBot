import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from albumbot.config import config
from box import Box
from rich.console import Console

log = logging.getLogger("albumBot")


def get():
    auth_manager = SpotifyClientCredentials(
        client_id=config.SPOTIFY_CLIENT_ID, client_secret=config.SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return list(filter(is_wanted_genre_p, stream_releases(sp)))


def debug_print_release(release):
    log.debug(
        {
            "album": release.name,
            "artists": [a.name for a in release.artists],
            "genres": release.artists_genres,
            "released": release.release_date,
            "link": release.external_urls.spotify,
        }
    )


def is_wanted_genre_p(release):
    for genre in release.artists_genres:
        if genre in config.WANTED_GENRES_LIST:
            return True


def stream_releases(client):
    seen = set()
    for country in config.SPOTIFY_RELEASE_COUNTRIES_LIST:
        offset = 0
        while True:
            results = client.new_releases(country=country, limit=50, offset=offset)

            for release in results["albums"]["items"]:
                if release["id"] not in seen:
                    release = Box(release)
                    release["artists_genres"] = lookup_artist_genres(
                        client, artists=[a.id for a in release.artists]
                    )
                    yield Box(release)
                    seen.add(release["id"])

            offset += 50
            if offset >= results["albums"]["total"]:
                break


def lookup_artist_genres(client, artists):
    results = []
    for artist in artists:
        results.extend(client.artist(artist)["genres"])
    return results
