from ttlcache import TTLCache


def test_peek_does_not_change_recency_or_stats():
    c = TTLCache(capacity=2)
    c.set("a", 1)
    c.set("b", 2)
    assert c.peek("a") == 1
    c.set("c", 3)
    assert "a" not in c
    assert c.stats.hits == 0 and c.stats.misses == 0


def test_peek_ignores_expired_entries(clock):
    c = TTLCache(ttl=5, clock=clock)
    c.set("a", 1)
    clock.advance(5)
    assert c.peek("a", "gone") == "gone"


def test_clear_empties_cache():
    c = TTLCache()
    c.set("a", 1)
    c.set("b", 2)
    c.clear()
    assert len(c) == 0
