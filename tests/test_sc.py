from sc import sc

import os
import sys
import json
import shutil

import pytest
from mutagen import File
from urllib.request import urlopen


def test_song_id():
    assert sc.get_song_id("https://soundcloud.com/fizzlebert/mad-world") == "461806533"
    with pytest.raises(sc.InvalidURL):
        sc.get_song_id("https://google.com")


def test_get_user_id():
    assert sc.get_user_id("fizzlebert") == 368628269
    with pytest.raises(sc.UsernameNotFound):
        sc.get_user_id("sdlfkjsdlkfjsdlkfjsldkfj")


def test_get_favourites():
    test_json = json.loads(
        urlopen(
            "http://api.soundcloud.com/users/fizzlebert/favorites?client_id=a3e059563d7fd3372b49b37f00a00bcf"
        ).read()
    )
    assert sc.get_favourites("fizzlebert") == test_json
    with pytest.raises(sc.UsernameNotFound):
        sc.get_favourites("sdlfkjsdlkfjsdlkfjsldkfj")


def test_clean_title():
    assert sc.clean_title("Someone\\//with.mp3") == "Someonewith.mp3"
