# Task: intermittent cache misbehaviour in production

Our service uses `ttlcache.TTLCache` in front of a slow upstream. After the
last release on-call has reported:

* Dashboards show an impossible **hit rate** (higher than the true cache
  effectiveness) for workloads with lots of expiring keys.
* Entries sometimes survive for one tick longer than their TTL.
* Writing to a key that already exists occasionally makes **other, unrelated
  keys disappear**.
* Under load we see sporadic `KeyError`s from inside the cache and metrics that
  don't add up.
* Several requests for the same cold key all call the expensive upstream
  instead of just one.

## Your job

Find the root causes and fix them in `src/ttlcache/`.

## Rules

* Do not modify anything under `tests/` (the verifier detects this).
* Keep the public API backwards compatible.
* Standard library only.
* Read `docs/design.md` for the intended behaviour.

## Done when

`python tasks/verify.py` exits with status 0.
