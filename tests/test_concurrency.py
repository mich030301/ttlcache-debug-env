import random
import sys
import threading
import time

import pytest

from ttlcache import TTLCache


@pytest.fixture
def aggressive_switching():
    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    yield
    sys.setswitchinterval(old)


def _run(threads):
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def test_get_or_set_is_single_flight_under_contention():
    c = TTLCache()
    calls = []
    results = []
    barrier = threading.Barrier(8)

    def factory():
        calls.append(1)
        time.sleep(0.05)
        return "v"

    def worker():
        barrier.wait()
        results.append(c.get_or_set("k", factory))

    _run([threading.Thread(target=worker) for _ in range(8)])
    assert len(calls) == 1
    assert results == ["v"] * 8


def test_mixed_operations_do_not_raise(aggressive_switching):
    c = TTLCache(capacity=16)
    errors = []

    def worker(seed):
        rnd = random.Random(seed)
        try:
            for _ in range(4000):
                k = rnd.randrange(64)
                op = rnd.random()
                if op < 0.5:
                    c.get(k)
                elif op < 0.9:
                    c.set(k, k)
                else:
                    c.delete(k)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    _run([threading.Thread(target=worker, args=(i,)) for i in range(8)])
    assert errors == []
    assert len(c) <= 16


def test_stats_stay_consistent_under_contention(aggressive_switching):
    c = TTLCache(capacity=1000)
    for i in range(1000):
        c.set(i, i)
    per_thread = 3000

    def worker(seed):
        rnd = random.Random(seed)
        for _ in range(per_thread):
            c.get(rnd.randrange(2000))

    _run([threading.Thread(target=worker, args=(i,)) for i in range(6)])
    assert c.stats.hits + c.stats.misses == 6 * per_thread
