import json
import pytest
from urllib.request import urlopen

from sc import sc


def test_get_favourites():
    test_json = json.loads(urlopen("http://api.soundcloud.com/users/fizzlebert/favorites?client_id=Oa1hmXnTqqE7F2PKUpRdMZqWoguyDLV0").read())
    assert sc.get_favourites("fizzlebert") == test_json
    with pytest.raises(sc.UsernameNotFound):
        sc.get_favourites("sdlfkjsdlkfjsdlkfjsldkfj")
