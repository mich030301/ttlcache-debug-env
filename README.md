# ttlcache-debug-env

A reproducible **debugging environment** built around a small, realistic Python
library: a thread-safe LRU cache with per-entry TTLs. The library on `main`
contains several subtle, production-style bugs; the test-suite is red until they
are found and fixed.

It is designed to test whether an engineer (or an AI agent) can diagnose a
multi-cause failure from symptoms, tests and code, without breaking the public
API or touching the tests.

## Layout

| Path | Purpose |
|------|---------|
| `src/ttlcache/` | The library under repair |
| `tests/` | Behavioural + concurrency tests (read-only for the task) |
| `tasks/TASK.md` | The bug report handed to the solver |
| `tasks/verify.py` | Grader: score report + tamper detection |
| `solution/` | Golden patch and root-cause write-up (excluded from the image) |
| `docs/design.md` | Intended invariants |
| `.github/workflows/ci.yml` | Proves *broken on main, green after the patch* |

## Quick start

```bash
pip install -e ".[dev]"
python tasks/verify.py              # exits non-zero: the env is broken
bash solution/apply.sh              # apply the reference fix
python tasks/verify.py              # exits 0
```

Or with Docker:

```bash
docker build -t ttlcache-debug-env .
docker run --rm ttlcache-debug-env
```

## Design goals

* **Deterministic**: time is injected; the only timing-based test uses a barrier.
* **Diagnosable**: every bug maps to a specific failing test.
* **Hard to game**: tests are hash-pinned; the golden patch is not in the image.
* **Verifiable**: CI checks both the broken and the fixed state on 3 Python versions.

See [`docs/design.md`](docs/design.md) and [`docs/grading.md`](docs/grading.md).
