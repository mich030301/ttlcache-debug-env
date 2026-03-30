from ttlcache import TTLCache


def test_hit_and_miss_counting():
    c = TTLCache()
    c.set("a", 1)
    c.get("a")
    c.get("a")
    c.get("zzz")
    assert c.stats.hits == 2
    assert c.stats.misses == 1


def test_hit_rate():
    c = TTLCache()
    assert c.stats.hit_rate == 0.0
    c.set("a", 1)
    c.get("a")
    c.get("b")
    assert c.stats.hit_rate == 0.5


def test_eviction_counting():
    c = TTLCache(capacity=1)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    assert c.stats.evictions == 2


def test_overwrite_is_not_an_eviction():
    c = TTLCache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 5)
    assert c.stats.evictions == 0


def test_reset():
    c = TTLCache()
    c.set("a", 1)
    c.get("a")
    c.stats.reset()
    assert c.stats.as_dict()["hits"] == 0
    assert c.stats.lookups == 0
