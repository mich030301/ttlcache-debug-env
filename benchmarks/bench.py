"""Micro-benchmark for the hot paths. Run with ``make bench``."""

from __future__ import annotations

import random
import time

from ttlcache import TTLCache


def bench(n: int = 200_000, capacity: int = 1024) -> None:
    cache = TTLCache(capacity=capacity, ttl=60)
    rnd = random.Random(0)
    keys = [rnd.randrange(capacity * 2) for _ in range(n)]

    start = time.perf_counter()
    for k in keys:
        cache.set(k, k)
    set_s = time.perf_counter() - start

    start = time.perf_counter()
    for k in keys:
        cache.get(k)
    get_s = time.perf_counter() - start

    print(f"set: {n / set_s:,.0f} ops/s")
    print(f"get: {n / get_s:,.0f} ops/s  (hit rate {cache.stats.hit_rate:.1%})")


if __name__ == "__main__":
    bench()
