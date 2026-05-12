# Contributing

1. Keep the environment *deterministic*: no network, no wall-clock dependence
   (use the injected clock), no sleeps longer than ~100 ms.
2. Every injected bug needs (a) a failing test that pinpoints the behaviour and
   (b) an entry in `solution/EXPLANATION.md`.
3. After changing `tests/`, refresh the digest:
   `python tasks/verify.py --write-digest`.
4. Regenerate `solution/fix.patch` against `main` and run `make verify-fixed`.
