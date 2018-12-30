#!/usr/bin/env python3
"""
sc, download songs from SoundCloud.

Usage:
    sc <username> likes
    sc <username> tracks
    sc <username> playlists
    sc <url>

Options:
    -h, --help    Show this screen.
    --version     Show version.
    -a, --artist  Save songs in artist folders.
"""

import os
import re

import mutagen
from tqdm import tqdm
from docopt import docopt
from requests import get

from sc import __version__

CLIENTID = "Oa1hmXnTqqE7F2PKUpRdMZqWoguyDLV0"
ILLEGAL_CHARS = "/\\"

URLS = {
    "favorites": "http://api.soundcloud.com/users/{}/favorites",
    "user": "https://api.soundcloud.com/users/{}",
    "playlists": "http://api.soundcloud.com/users/{}/playlists",
    "track": "https://api.soundcloud.com/tracks/{}",
    "tracks": "https://api.soundcloud.com/users/{}/tracks",
}

tracks = playlists = None


class UsernameNotFound(Exception):
    def __init__(self, username):
        pass


class InvalidURL(Exception):
    def __init__(self, url):
        pass


def download_track(url):
    """Download a track based on url."""
    return get(url, params={"client_id": CLIENTID})


def get_favourites(user):
    """Make a request for users favourite songs."""
    r = get(URLS["favorites"].format(user), params={"client_id": CLIENTID})
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()


def get_user_id(user):
    """Make a request to find user's id."""
    r = get(URLS["user"].format(user), params={"client_id": CLIENTID})
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()["id"]


def get_tracks(user_id):
    """Make a request for tracks by a user."""
    return get(
        URLS["tracks"].format(user_id), params={"client_id": CLIENTID}
    ).json()


def get_playlists(user_id):
    """Make a request for playlists by a user."""
    return get(
        URLS["playlists"].format(user_id), params={"client_id": CLIENTID}
    ).json()


def get_track(song_id):
    """Make a request for a song."""
    return get(
        URLS["track"].format(song_id), params={"client_id": CLIENTID}
    ).json()


def get_song_id(url):
    """Get song id from website."""
    html = get(url)
    song_id = re.search(r"soundcloud://sounds:(\d+)", html.text, re.IGNORECASE)
    if song_id:
        return song_id.group(1)
    else:
        raise InvalidURL(url)


def clean_title(title):
    """Remove non hex characters from song title."""
    return "".join([c for c in title if c not in ILLEGAL_CHARS])


def set_metadata(file_name, track, album=None):
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
        artwork = get(
            track["artwork_url"].replace("large", "t500x500"), timeout=10
        )
        song = mutagen.File(file_name)
        song["APIC"] = mutagen.id3.APIC(
            encoding=3, mime="image/jpeg", type=3, desc="Cover", data=artwork.content
        )
        song.save()


def parse_args():
    """Act upon arguments."""
    global tracks, playlists
    args = docopt(__doc__, version=__version__)
    if args["tracks"]:
        user = args["<username>"]
        tracks = get_tracks(get_user_id(user))
    elif args["likes"]:
        user = args["<username>"]
        tracks = get_favourites(user)
    elif args["playlists"]:
        user = args["<username>"]
        playlists = get_playlists(user)
    elif args["<url>"]:
        songurl = args["<url>"]
        tracks = [get_track(get_song_id(songurl))]


def download_playlists():
    """Download tracks from a playlist."""
    global tracks
    for playlist in tqdm(playlists, unit="playlist"):
        tracks = playlist["tracks"]
        download_tracks(album=playlist["title"])


def download_tracks(album=None):
    """Download specified tracks."""
    for track in tqdm(tracks, unit="song", desc=album):
        track["title"] = clean_title(track["title"])

        # save albums to separate folder
        if album:
            directory = os.path.join(track["user"]["username"], album)
        else:
            directory = track["user"]["username"]
        file_name = os.path.join(directory, track["title"] + ".mp3")

        # don't redownload song
        if os.path.isfile(file_name):
            continue

        # if the artist directory doesn't exist make it; should only run once
        if not os.path.isdir(directory):
            os.makedirs(directory)

        # download and save song
        with open(file_name, "wb") as song:
            song.write(download_track(track["stream_url"]).content)

        set_metadata(file_name, track, album=album)


def main():
    """Iterate through songs and save them."""
    parse_args()
    if tracks:
        download_tracks()
    elif playlists:
        download_playlists()


if __name__ == "__main__":
    main()
