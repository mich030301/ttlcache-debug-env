# ttlcache-debug-env

A reproducible debugging environment built around a small, realistic Python
library: a thread-safe LRU cache with per-entry TTLs.

The library ships with several subtle, production-style bugs. The goal of the
environment is to test whether an engineer (or an AI agent) can diagnose them
from the failing test-suite and symptoms alone, without breaking the public API.

Work in progress.
