from ttlcache import TTLCache


def test_eviction_callback_receives_key_value_reason():
    seen = []
    c = TTLCache(capacity=1, on_evict=lambda k, v, r: seen.append((k, v, r)))
    c.set("a", 1)
    c.set("b", 2)
    assert seen == [("a", 1, "capacity")]


def test_updating_existing_key_triggers_no_callback():
    seen = []
    c = TTLCache(capacity=2, on_evict=lambda k, v, r: seen.append((k, v, r)))
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 3)
    assert seen == []


def test_delete_does_not_trigger_callback():
    seen = []
    c = TTLCache(capacity=2, on_evict=lambda k, v, r: seen.append((k, v, r)))
    c.set("a", 1)
    c.delete("a")
    assert seen == []
