# Design notes

`TTLCache` is a bounded, in-memory cache.

## Invariants

1. `len(cache) <= capacity` at all times (expired-but-unvisited entries count
   until they are purged or touched).
2. An entry stored at time *t* with TTL *d* is **live** for `now < t + d` and
   **expired** for `now >= t + d`.
3. Overwriting a key never evicts another key and refreshes both recency and TTL.
4. `hits + misses` equals the number of `get` calls. An expired lookup is a miss.
5. `on_evict` fires for `"capacity"` and `"expired"` removals only, never for
   `delete`, `clear` or overwrites.
6. All public methods are safe to call from multiple threads, and `get_or_set`
   invokes its factory at most once per missing key.

## Non-goals

Cross-process sharing, persistence, async API.
