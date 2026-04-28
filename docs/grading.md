# Grading

A run is scored by `python tasks/verify.py`:

* `score` is `passed / total` across the whole suite.
* The run **succeeds** only if every test passes and `tests/` is byte-identical
  to the committed digest (`tasks/tests.sha256`).
* Runs that edit tests are rejected regardless of score.

CI additionally proves the environment is well-formed:

1. On `main` the suite must be red (`--expect broken`).
2. After applying `solution/fix.patch` the suite must be green (`--expect fixed`).
