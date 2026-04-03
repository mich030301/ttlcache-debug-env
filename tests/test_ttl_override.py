from ttlcache import TTLCache


def test_per_key_ttl_overrides_default(clock):
    c = TTLCache(ttl=100, clock=clock)
    c.set("short", 1, ttl=5)
    c.set("long", 2)
    clock.advance(5)
    assert c.get("short") is None
    assert c.get("long") == 2


def test_per_key_ttl_without_default(clock):
    c = TTLCache(clock=clock)
    c.set("a", 1, ttl=3)
    c.set("b", 2)
    clock.advance(3)
    assert "a" not in c
    assert "b" in c


def test_per_key_ttl_can_be_longer_than_default(clock):
    c = TTLCache(ttl=5, clock=clock)
    c.set("a", 1, ttl=50)
    clock.advance(20)
    assert c.get("a") == 1


def test_expiry_updates_stats_and_notifies(clock):
    seen = []
    c = TTLCache(ttl=1, clock=clock, on_evict=lambda k, v, r: seen.append((k, v, r)))
    c.set("a", 1)
    clock.advance(2)
    c.get("a")
    assert c.stats.expirations == 1
    assert seen == [("a", 1, "expired")]
