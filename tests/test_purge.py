from ttlcache import TTLCache


def test_purge_removes_only_expired_entries(clock):
    c = TTLCache(clock=clock)
    c.set("a", 1, ttl=5)
    c.set("b", 2, ttl=5)
    c.set("c", 3, ttl=50)
    clock.advance(10)
    assert len(c) == 3
    assert c.purge_expired() == 2
    assert len(c) == 1
    assert c.get("c") == 3


def test_purge_updates_stats_and_notifies(clock):
    seen = []
    c = TTLCache(clock=clock, on_evict=lambda k, v, r: seen.append((k, r)))
    c.set("a", 1, ttl=1)
    clock.advance(1)
    c.purge_expired()
    assert c.stats.expirations == 1
    assert seen == [("a", "expired")]


def test_purge_on_empty_cache():
    assert TTLCache().purge_expired() == 0
