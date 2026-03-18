from ttlcache import TTLCache


def test_delete_existing_key():
    c = TTLCache()
    c.set("a", 1)
    assert c.delete("a") is True
    assert "a" not in c


def test_delete_missing_key():
    assert TTLCache().delete("nope") is False


def test_len_tracks_entries():
    c = TTLCache()
    assert len(c) == 0
    c.set("a", 1)
    c.set("b", 2)
    assert len(c) == 2
    c.delete("a")
    assert len(c) == 1


def test_contains_with_none_value():
    c = TTLCache()
    c.set("a", None)
    assert "a" in c
