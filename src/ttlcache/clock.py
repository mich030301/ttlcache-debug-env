"""Injectable clock so tests (and callers) can control time."""

from __future__ import annotations

import time
from typing import Callable

Clock = Callable[[], float]

#: Default clock. Monotonic so wall-clock adjustments never affect expiry.
monotonic: Clock = time.monotonic
