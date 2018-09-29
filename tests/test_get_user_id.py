import pytest

from sc import sc


def test_get_user_id():
    assert sc.get_user_id("fizzlebert") == 368628269
    with pytest.raises(sc.UsernameNotFound):
        sc.get_user_id("sdlfkjsdlkfjsdlkfjsldkfj")
