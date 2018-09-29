#!/usr/bin/env python3
"""
sc, download songs from SoundCloud.

Usage:
    sc <username> likes
    sc <username> tracks
    sc <url>

Options:
    -h, --help    Show this screen.
    --version     Show version.
    -a, --artist  Save songs in artist folders.
"""

import os
import re
from urllib.request import urlopen

import mutagen
import requests
from tqdm import tqdm
from docopt import docopt

from sc import __version__

CLIENTID = "Oa1hmXnTqqE7F2PKUpRdMZqWoguyDLV0"
ILLEGAL_CHARS = "/\\"

URLS = {
    "favorites": "http://api.soundcloud.com/users/{}/favorites",
    "user": "https://api.soundcloud.com/users/{}",
    "track": "https://api.soundcloud.com/tracks/{}",
    "tracks": "https://api.soundcloud.com/users/{}/tracks",
}

tracks = None


class UsernameNotFound(Exception):
    def __init__(self, username):
        pass


class InvalidURL(Exception):
    def __init__(self, url):
        pass


def download_track(url):
    """Download a track based on url.

    Args:
        url (str): URL from SoundCloud of song to download

    Returns:
        HTTPResponse: Raw bytes of song to save
    """
    return urlopen("".join([url, f"?client_id={CLIENTID}"]))


def get_favourites(user):
    """Make a request for users favourite songs.

    Args:
        user (str): Name of user displayed on SoundCloud

    Returns:
        json: Information about user's favourite songs
    """
    r = requests.get(
        URLS["favorites"].format(user),
        params={"client_id": CLIENTID}
    )
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()


def get_user_id(user):
    """Make a request to find user's id.

    Args:
        user (str): Name of user displayed on SoundCloud

    Returns:
        str: Id of user given by SoundCloud
    """
    r = requests.get(URLS["user"].format(user), params={"client_id": CLIENTID})
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()["id"]


def get_tracks(user_id):
    """Make a request for tracks by a user.

    Args:
        user_id (str): Id of user given by SoundCloud

    Returns:
        json: Information about tracks by user
    """
    return requests.get(
        URLS["tracks"].format(user_id), params={"client_id": CLIENTID}
    ).json()


def get_track(song_id):
    """Make a request for a song.

    Args:
        song_id (str): Song id given by SoundCloud

    Returns:
        json: Information about song
    """
    return requests.get(
        URLS["track"].format(song_id), params={"client_id": CLIENTID}
    ).json()


def get_song_id(url):
    """Get song id from website.

    Args:
        url (str): URL from SoundCloud of song to download

    Returns:
        str: Id of song
    """
    html = requests.get(url)
    song_id = re.search(r"soundcloud://sounds:(\d+)", html.text, re.IGNORECASE)
    if song_id:
        return song_id.group(1)
    else:
        raise InvalidURL(url)


def clean_title(title):
    """Remove non hex characters from song title.

    Args:
        title (str): Song title

    Returns:
        str: Clean song title
    """
    return "".join([c for c in title if c not in ILLEGAL_CHARS])


def parse_args():
    """Act upon arguments."""
    global tracks
    args = docopt(__doc__, version=__version__)
    if args["tracks"]:
        user = args["<username>"]
        tracks = get_tracks(get_user_id(user))
    elif args["likes"]:
        user = args["<username>"]
        tracks = get_favourites(user)
    elif args["<url>"]:
        songurl = args["<url>"]
        tracks = [get_track(get_song_id(songurl))]


def main():
    """Iterate through songs and save them."""
    parse_args()
    for track in tqdm(tracks, unit="song"):

        # clean song title
        track["title"] = clean_title(track["title"])

        # don't redownload song
        directory = track["user"]["username"]
        if os.path.isfile("/".join([directory, track["title"] + ".mp3"])):
            continue

        # if the artist directory doesn't exist make it
        if not os.path.isdir(directory):
            os.makedirs(directory)

        # download and save song
        filename = track["user"]["username"] + "/" + track["title"] + ".mp3"
        with open(filename, "wb") as song:
            song.write(download_track(track["stream_url"]).read())

        # download artwork
        if track["artwork_url"]:
            # use largest artwork
            artwork_url = track["artwork_url"].replace("large", "t500x500")
            artwork = requests.get(artwork_url)

        # set metadata of song
        song = mutagen.File(filename, easy=True)
        song["title"] = track["title"]
        song["artist"] = track["user"]["username"]
        song["genre"] = track["genre"]

        # add artwork
        if track["artwork_url"]:
            song = mutagen.File(filename)
            song["APIC"] = mutagen.id3.APIC(
                encoding=3, mime="image/jpeg", type=3,
                desc="Cover", data=artwork.content,
            )
        song.save()


if __name__ == "__main__":
    main()
