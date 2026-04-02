from ttlcache import TTLCache


def test_entry_is_available_before_ttl(clock):
    c = TTLCache(ttl=10, clock=clock)
    c.set("a", 1)
    clock.advance(9.9)
    assert c.get("a") == 1


def test_entry_expires_exactly_at_ttl(clock):
    c = TTLCache(ttl=10, clock=clock)
    c.set("a", 1)
    clock.advance(10)
    assert c.get("a") is None


def test_entry_expired_after_ttl(clock):
    c = TTLCache(ttl=10, clock=clock)
    c.set("a", 1)
    clock.advance(11)
    assert c.get("a", "gone") == "gone"
    assert len(c) == 0


def test_contains_is_false_for_expired_entries(clock):
    c = TTLCache(ttl=10, clock=clock)
    c.set("a", 1)
    clock.advance(10)
    assert "a" not in c


def test_cache_without_ttl_never_expires(clock):
    c = TTLCache(clock=clock)
    c.set("a", 1)
    clock.advance(10**9)
    assert c.get("a") == 1


def test_overwrite_resets_ttl(clock):
    c = TTLCache(ttl=10, clock=clock)
    c.set("a", 1)
    clock.advance(8)
    c.set("a", 2)
    clock.advance(8)
    assert c.get("a") == 2
