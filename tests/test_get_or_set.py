from ttlcache import TTLCache


def test_computes_on_miss_and_caches():
    calls = []
    c = TTLCache()

    def factory():
        calls.append(1)
        return "v"

    assert c.get_or_set("k", factory) == "v"
    assert c.get_or_set("k", factory) == "v"
    assert len(calls) == 1


def test_caches_none_results():
    calls = []
    c = TTLCache()

    def factory():
        calls.append(1)
        return None

    assert c.get_or_set("k", factory) is None
    assert c.get_or_set("k", factory) is None
    assert len(calls) == 1


def test_recomputes_after_expiry(clock):
    calls = []
    c = TTLCache(ttl=5, clock=clock)

    def factory():
        calls.append(1)
        return len(calls)

    assert c.get_or_set("k", factory) == 1
    clock.advance(5)
    assert c.get_or_set("k", factory) == 2


def test_per_call_ttl(clock):
    c = TTLCache(clock=clock)
    c.get_or_set("k", lambda: 1, ttl=2)
    clock.advance(2)
    assert "k" not in c
