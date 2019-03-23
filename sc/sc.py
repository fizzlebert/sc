#!/usr/bin/env python3
"""
sc, download songs from SoundCloud.

Usage:
    sc <username> likes
    sc <username> tracks
    sc <username> playlists
    sc search <query> [<number>]
    sc <url>

Options:
    <number>    Number of songs to download.
    -h, --help  Show this screen.
    --version   Show version.
"""

import os
import re
from concurrent import futures

import mutagen
import requests
from tqdm import tqdm
from docopt import docopt

from sc import __version__

CLIENT_ID = "a3e059563d7fd3372b49b37f00a00bcf"
ILLEGAL_CHARS = "/\\"

URLS = {
    "favourites": "http://api.soundcloud.com/users/{}/favorites",
    "user": "https://api.soundcloud.com/users/{}",
    "playlists": "http://api.soundcloud.com/users/{}/playlists",
    "track": "https://api.soundcloud.com/tracks/{}",
    "tracks": "https://api.soundcloud.com/users/{}/tracks",
    "search": "https://api.soundcloud.com/tracks/",
}

tracks = playlists = search = None
session = requests.Session()
session.params.update({"client_id": CLIENT_ID})


class UsernameNotFound(Exception):
    def __init__(self, username: str):
        pass


class InvalidURL(Exception):
    def __init__(self, url: str):
        pass


def download_track(track: dict, album: str = None):
    """Download a track based on url."""
    track["title"] = clean_title(track["title"])

    # save albums to separate folder
    if album:
        directory = os.path.join(track["user"]["username"], album)
    else:
        directory = track["user"]["username"]
    file_name = os.path.join(directory, track["title"] + ".mp3")

    # don't redownload song
    if os.path.isfile(file_name):
        return

    # if the artist directory doesn't exist make it; should only run once
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    # download and save song
    with open(file_name, "wb") as song:
        song.write(session.get(track["stream_url"]).content)

    set_metadata(file_name, track, album=album)


def get_favourites(user: str):
    """Make a request for users favourite songs."""
    r = session.get(URLS["favourites"].format(user))
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()


def get_user_id(user: str):
    """Make a request to find user's id."""
    r = session.get(URLS["user"].format(user))
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()["id"]


def get_tracks(user_id: str):
    """Make a request for tracks by a user."""
    return session.get(URLS["tracks"].format(user_id)).json()


def get_playlists(user_id: str):
    """Make a request for playlists by a user."""
    return session.get(URLS["playlists"].format(user_id)).json()


def get_track(song_id: str):
    """Make a request for a song."""
    return session.get(URLS["track"].format(song_id)).json()


def get_song_id(url: str):
    """Get soundcloud id from website."""
    html = session.get(url)
    match = re.search(r"soundcloud://sounds:(\d+)", html.text)
    if match:
        return match.group(1)
    else:
        raise InvalidURL(url)


def clean_title(title: str):
    """Remove non hex characters from song title."""
    return "".join([c for c in title if c not in ILLEGAL_CHARS])


def set_metadata(file_name: str, track: dict, album: str = None):
    """Set metadata for a specific file."""
    song = mutagen.File(file_name, easy=True)
    if album:
        song["album"] = album
    song["title"] = track["title"]
    song["artist"] = track["user"]["username"]
    if track["genre"]:
        song["genre"] = track["genre"]
    song.save()

    # add artwork
    if track["artwork_url"]:
        artwork = session.get(
            track["artwork_url"].replace("large", "t500x500"), timeout=10
        )
        song = mutagen.File(file_name)
        song["APIC"] = mutagen.id3.APIC(
            encoding=3, mime="image/jpeg", type=3, desc="Cover", data=artwork.content
        )
        song.save()


def parse_args(args: dict):
    """Act upon arguments."""
    global tracks, playlists
    if args["tracks"]:
        user = args["<username>"]
        tracks = get_tracks(get_user_id(user))
    elif args["likes"]:
        user = args["<username>"]
        tracks = get_favourites(user)
    elif args["playlists"]:
        user = args["<username>"]
        playlists = get_playlists(user)
    elif args["search"]:
        number = int(args["<number>"]) if args["<number>"] else 1
        tracks = get_search(args["<query>"], number=number)
    elif args["<url>"]:
        songurl = args["<url>"]
        tracks = [get_track(get_song_id(songurl))]


def download_playlists():
    """Download tracks from a playlist."""
    global tracks
    for playlist in tqdm(playlists, unit="playlist"):
        tracks = playlist["tracks"]
        download_tracks(album=playlist["title"])


def get_search(search: str, number: int):
    """Download a search query."""
    r = session.get(URLS["search"], params={"q": search}).json()
    return r[:number]


def download_tracks(album: str = None):
    """Download specified tracks."""
    with futures.ThreadPoolExecutor(max_workers=15) as executor:
        to_do = []
        for track_data in tracks:
            future = executor.submit(download_track, track_data)
            to_do.append(future)

        for future in tqdm(futures.as_completed(to_do), unit="song", total=len(tracks)):
            _ = future.result()


def main():
    """Iterate through songs and save them."""
    args = docopt(__doc__, version=__version__)
    parse_args(args)
    if tracks:
        download_tracks()
    elif playlists:
        download_playlists()
    elif search:
        download_tracks()


if __name__ == "__main__":
    main()
