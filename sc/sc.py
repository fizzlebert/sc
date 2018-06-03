#!/usr/bin/env python3

import os
import re
import argparse
from urllib.request import urlopen

import mutagen
import requests
from tqdm import tqdm


# different way of using arguments

CLIENTID = "Oa1hmXnTqqE7F2PKUpRdMZqWoguyDLV0"
illegal_chars = "/\\"

urls = {
    "favorites": "http://api.soundcloud.com/users/{}/favorites",
    "user": "https://api.soundcloud.com/users/{}",
    "track": "https://api.soundcloud.com/tracks/{}",
    "tracks": "https://api.soundcloud.com/users/{}/tracks",
}


class UsernameNotFound(Exception):
    def __init__(self, username):
        pass


class InvalidURL(Exception):
    def __init__(self, url):
        pass


def download_track(url):
    """Download a track based on url."""
    return urlopen("".join([url, f"?client_id={CLIENTID}"]))


def get_favourites(user):
    r = requests.get(
        urls["favorites"].format(user), params={"client_id": CLIENTID, "limit": 400}
    )
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()


def get_user_id(user):
    r = requests.get(urls["user"].format(user), params={"client_id": CLIENTID})
    if r.status_code != 200:
        raise UsernameNotFound(user)
    return r.json()["id"]


def get_tracks(user_id):
    return requests.get(
        urls["tracks"].format(user_id), params={"client_id": CLIENTID, "limit": 400}
    ).json()


def get_track(song_id):
    return requests.get(
        urls["track"].format(song_id), params={"client_id": CLIENTID}
    ).json()


def get_song_id(url):
    html = requests.get(url)
    id = re.search(r"soundcloud://sounds:(\d+)", html.text, re.IGNORECASE)
    if id:
        return id.group(1)
    else:
        raise InvalidURL(url)


def pass_args():
    global tracks, args
    # act upon arguments
    parser = argparse.ArgumentParser(
        description="Simple program to download songs from SoundCloud."
    )
    parser.add_argument(
        "--user", "-u", type=str,
        help="User to all songs from."
    )
    parser.add_argument(
        "--likes", "-l", type=str,
        help="User to download liked tracks from."
    )
    parser.add_argument(
        "--url", "-w", type=str,
        help="URL of SoundCloud song to download."
    )
    # parser.add_argument(
    #     "--artist", "-a", type=bool, default=False,
    #     help="Save songs in artist folder."
    # )
    args = parser.parse_args()
    if args.user:
        user = args.user
        tracks = get_tracks(get_user_id(user))
    elif args.likes:
        user = args.likes
        tracks = get_favourites(user)
    elif args.url:
        songurl = args.url
        tracks = [get_track(get_song_id(songurl))]
    else:
        print("Nothing to do.")
        exit()


def main():
    pass_args()
    # iterate through songs with progress bar
    for track in tqdm(tracks, unit="song"):

        # clean song title
        track["title"] = "".join(
                c for c in track["title"] if c not in illegal_chars
            )

        # don't redownload song
        if "".join([track["title"], ".mp3"]) in os.listdir():
            continue

        # download and save song
        filename = "".join([track["title"], ".mp3"])
        # if args.artist:
        #     filename = "/".join([track["artist"], filename])
        with open(filename, "wb") as song:
            song.write(download_track(track["stream_url"]).read())

        # download artwork
        if track["artwork_url"]:
            artwork_url = track["artwork_url"].replace("large", "t500x500")
            artwork = requests.get(artwork_url)

        # set metadata of song
        song = mutagen.File(filename, easy=True)
        song["title"] = track["title"]
        song["artist"] = track["user"]["username"]
        song["genre"] = track["genre"]
        song.save()
        if track["artwork_url"]:
            song = mutagen.File(filename)
            song["APIC"] = mutagen.id3.APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,
                desc="Cover",
                data=artwork.content,
            )
        song.save()


if __name__ == "__main__":
    main()
