import logging
from typing import Any, Dict, Generator, List, Set, Type, TypeVar

import spotipy
from pydantic import BaseModel
from spotipy.oauth2 import SpotifyClientCredentials

from albumbot.config import Config

log = logging.getLogger("albumBot")
config = Config.config()

T = TypeVar("T", bound="AlbumRelease")


class AlbumRelease(BaseModel):
    id: str
    name: str
    artists: List[str]
    genres: List[str]
    link: str

    @classmethod
    def from_spotipy(cls: Type[T], sp: spotipy.Spotify, release: Dict[str, Any]) -> T:
        artists_ids = [a["id"] for a in release["artists"]]
        return cls(
            id=release["id"],
            name=release["name"],
            artists=[a["name"] for a in release["artists"]],
            genres=AlbumRelease.get_genres(sp, artists_ids),
            link=release["external_urls"]["spotify"],
        )

    def log(self) -> None:
        log.debug(repr(self))

    @staticmethod
    def get_genres(client, artists: List[str]) -> List[str]:
        results = []
        for artist in artists:
            results.extend(client.artist(artist)["genres"])
        return results


def get() -> List[AlbumRelease]:
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET,
        )
    )
    return list(filter(is_wanted_genre_p, stream_releases(sp)))


def is_wanted_genre_p(release: AlbumRelease) -> bool:
    for genre in release.genres:
        if genre in config.WANTED_GENRES:
            return True
    return False


def stream_releases(client: spotipy.Spotify) -> Generator[AlbumRelease, None, None]:
    seen: Set[str] = set()
    for country in config.SPOTIFY_RELEASE_COUNTRIES:
        offset: int = 0
        while True:
            results = client.new_releases(country=country, limit=50, offset=offset)

            for release in results["albums"]["items"]:
                if release["id"] not in seen:
                    yield AlbumRelease.from_spotipy(client, release)
                    seen.add(release["id"])

            offset += 50
            if offset >= results["albums"]["total"]:
                break
