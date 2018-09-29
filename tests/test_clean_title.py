from sc import sc


def test_clean_title():
    assert sc.clean_title("Someone\\//with.mp3") == "Someonewith.mp3"
