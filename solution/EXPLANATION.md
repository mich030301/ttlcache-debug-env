# Root causes

| # | Symptom | Cause | Fix |
|---|---------|-------|-----|
| 1 | Inflated hit rate | `get` bumped `hits` *before* checking expiry, so expired lookups counted as hits | Check expiry first; expired lookup is a miss (+ an expiration) |
| 2 | Entries live one tick too long | `_is_expired` used `>` instead of `>=` | Boundary is inclusive: expired when `now >= expires_at` |
| 3 | Unrelated keys vanish on overwrite | `set` evicted whenever `len >= capacity`, even when the key already existed | Only evict when inserting a **new** key |
| 4 | `KeyError`s, skewed stats | No synchronisation: check-then-act on `OrderedDict` and non-atomic `+=` counters | One `RLock` around every public method |
| 5 | Duplicate upstream calls | `get_or_set` was a racy check-then-set | Run the factory under the lock (single-flight) |
| 6 | `in` returned True for expired keys | `__contains__` ignored TTL | Reuse `_is_expired` |

## Trade-off

Holding the lock during `factory()` serialises slow factories across *different*
keys. A per-key lock table would remove that, at the cost of more code and
lock-lifetime management. Kept simple here; documented in the docstring.
