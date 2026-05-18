#!/usr/bin/env python3
"""Grade the workspace.

Default mode runs the test-suite and exits 0 only if everything passes *and*
the tests were not tampered with. ``--expect broken|fixed`` is used by CI to
assert the environment is in the intended state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIGEST_FILE = ROOT / "tasks" / "tests.sha256"


def tests_digest() -> str:
    h = hashlib.sha256()
    for path in sorted((ROOT / "tests").glob("*.py")):
        h.update(path.name.encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def run_pytest() -> dict[str, int]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    counts = {"passed": 0, "failed": 0, "error": 0}
    for n, word in re.findall(r"(\d+) (passed|failed|error)", out):
        counts[word] = int(n)
    counts["returncode"] = proc.returncode
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", choices=["broken", "fixed"])
    ap.add_argument("--write-digest", action="store_true")
    args = ap.parse_args()

    if args.write_digest:
        DIGEST_FILE.write_text(tests_digest() + "\n")
        return 0

    tampered = DIGEST_FILE.read_text().strip() != tests_digest()
    res = run_pytest()
    total = res["passed"] + res["failed"] + res["error"]
    all_green = res["returncode"] == 0 and total > 0
    report = {**res, "total": total, "tests_tampered": tampered,
              "score": (res["passed"] / total) if total else 0.0}
    print(json.dumps(report, indent=2))

    if tampered:
        print("FAIL: tests/ was modified", file=sys.stderr)
        return 2
    if args.expect == "broken":
        return 0 if not all_green else 1
    return 0 if all_green else 1


if __name__ == "__main__":
    raise SystemExit(main())
