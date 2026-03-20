from ttlcache import TTLCache


def test_evicts_least_recently_used():
    c = TTLCache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    assert "a" not in c
    assert "b" in c and "c" in c


def test_get_refreshes_recency():
    c = TTLCache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.get("a")
    c.set("c", 3)
    assert "b" not in c
    assert "a" in c


def test_updating_existing_key_does_not_evict_others():
    c = TTLCache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 10)
    assert len(c) == 2
    assert c.get("b") == 2
    assert c.get("a") == 10


def test_updating_key_refreshes_recency():
    c = TTLCache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 10)
    c.set("c", 3)
    assert "b" not in c
    assert c.get("a") == 10


def test_capacity_of_one():
    c = TTLCache(capacity=1)
    c.set("a", 1)
    c.set("b", 2)
    assert "a" not in c
    assert c.get("b") == 2


def test_size_never_exceeds_capacity():
    c = TTLCache(capacity=5)
    for i in range(100):
        c.set(i, i)
        assert len(c) <= 5
