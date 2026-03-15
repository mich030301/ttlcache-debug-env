from ttlcache import TTLCache


def test_get_missing_returns_default():
    c = TTLCache()
    assert c.get("a") is None
    assert c.get("a", 5) == 5


def test_set_then_get():
    c = TTLCache()
    c.set("a", 1)
    assert c.get("a") == 1


def test_overwrite_value():
    c = TTLCache()
    c.set("a", 1)
    c.set("a", 2)
    assert c.get("a") == 2


def test_none_is_a_valid_value():
    c = TTLCache()
    c.set("a", None)
    assert c.get("a", "default") is None
