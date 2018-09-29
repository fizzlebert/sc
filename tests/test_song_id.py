import pytest
from sc import sc


def test_song_id():
    assert sc.get_song_id("https://soundcloud.com/fizzlebert/mad-world") == "461806533"
    with pytest.raises(sc.InvalidURL):
        sc.get_song_id("https://google.com")
