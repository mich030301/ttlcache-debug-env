#!/usr/bin/env bash
# Applies the reference fix to a clean checkout.
set -euo pipefail
cd "$(dirname "$0")/.."
patch -p1 --forward < solution/fix.patch
