PY ?= python3

.PHONY: install test lint verify verify-broken verify-fixed bench docker

install:
	$(PY) -m pip install -e ".[dev]"

test:
	$(PY) -m pytest

lint:
	ruff check src tests tasks benchmarks

verify:
	$(PY) tasks/verify.py

verify-broken:
	$(PY) tasks/verify.py --expect broken

verify-fixed:
	bash solution/apply.sh
	$(PY) tasks/verify.py --expect fixed

bench:
	$(PY) benchmarks/bench.py

docker:
	docker build -t ttlcache-debug-env .
