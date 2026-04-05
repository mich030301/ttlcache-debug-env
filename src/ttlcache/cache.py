"""An in-memory LRU cache with per-entry TTLs."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Callable, Hashable, Optional

from .clock import Clock, monotonic
from .errors import InvalidCapacityError, InvalidTTLError
from .stats import CacheStats

_MISSING = object()

EvictCallback = Callable[[Hashable, Any, str], None]


class TTLCache:
    """Bounded key/value cache with LRU eviction and optional expiry.

    Entries are stored as ``(value, expires_at)`` where ``expires_at`` is an
    absolute reading of the injected clock, or ``None`` for "never expires".
    Expired entries are removed lazily on access (or via ``purge_expired``).
    """

    def __init__(
        self,
        capacity: int = 128,
        ttl: Optional[float] = None,
        clock: Clock = monotonic,
        on_evict: Optional[EvictCallback] = None,
    ) -> None:
        if capacity <= 0:
            raise InvalidCapacityError(capacity)
        if ttl is not None and ttl <= 0:
            raise InvalidTTLError(ttl)
        self.capacity = capacity
        self.default_ttl = ttl
        self._clock = clock
        self._on_evict = on_evict
        self._data: OrderedDict[Hashable, tuple[Any, Optional[float]]] = OrderedDict()
        self.stats = CacheStats()

    # -- helpers ---------------------------------------------------------
    def _expires_at(self, ttl: Optional[float]) -> Optional[float]:
        effective = ttl if ttl is not None else self.default_ttl
        if effective is None:
            return None
        if effective <= 0:
            raise InvalidTTLError(effective)
        return self._clock() + effective

    def _is_expired(self, expires_at: Optional[float]) -> bool:
        return expires_at is not None and self._clock() > expires_at

    # -- public API ------------------------------------------------------
    def get(self, key: Hashable, default: Any = None) -> Any:
        if key in self._data:
            value, expires_at = self._data[key]
            self._data.move_to_end(key)
            self.stats.hits += 1
            if self._is_expired(expires_at):
                del self._data[key]
                self.stats.expirations += 1
                self._notify(key, value, "expired")
                return default
            return value
        self.stats.misses += 1
        return default

    def set(self, key: Hashable, value: Any, ttl: Optional[float] = None) -> None:
        expires_at = self._expires_at(ttl)
        if len(self._data) >= self.capacity:
            self._evict_one()
        self._data[key] = (value, expires_at)
        self._data.move_to_end(key)

    def delete(self, key: Hashable) -> bool:
        """Remove *key*. Returns True if it was present."""
        return self._data.pop(key, _MISSING) is not _MISSING

    # -- internals -------------------------------------------------------
    def _notify(self, key: Hashable, value: Any, reason: str) -> None:
        if self._on_evict is not None:
            self._on_evict(key, value, reason)

    def _evict_one(self) -> None:
        key, (value, _) = self._data.popitem(last=False)
        self.stats.evictions += 1
        self._notify(key, value, "capacity")

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def peek(self, key: Hashable, default: Any = None) -> Any:
        """Read a value without touching recency or statistics."""
        entry = self._data.get(key)
        if entry is None or self._is_expired(entry[1]):
            return default
        return entry[0]

    def clear(self) -> None:
        """Drop every entry. No callbacks fire and stats are untouched."""
        self._data.clear()

    def purge_expired(self) -> int:
        """Eagerly remove expired entries and return how many were removed."""
        removed = 0
        for key in list(self._data):
            value, expires_at = self._data[key]
            if self._is_expired(expires_at):
                del self._data[key]
                self.stats.expirations += 1
                self._notify(key, value, "expired")
                removed += 1
        return removed
