"""An in-memory LRU cache."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Callable, Hashable, Optional

from .errors import InvalidCapacityError
from .stats import CacheStats

_MISSING = object()

EvictCallback = Callable[[Hashable, Any, str], None]


class TTLCache:
    """Bounded in-memory key/value cache with least-recently-used eviction."""

    def __init__(self, capacity: int = 128, on_evict: Optional[EvictCallback] = None) -> None:
        if capacity <= 0:
            raise InvalidCapacityError(capacity)
        self.capacity = capacity
        self._on_evict = on_evict
        self._data: OrderedDict[Hashable, Any] = OrderedDict()
        self.stats = CacheStats()

    def get(self, key: Hashable, default: Any = None) -> Any:
        if key in self._data:
            self._data.move_to_end(key)
            self.stats.hits += 1
            return self._data[key]
        self.stats.misses += 1
        return default

    def set(self, key: Hashable, value: Any) -> None:
        if len(self._data) >= self.capacity:
            self._evict_one()
        self._data[key] = value
        self._data.move_to_end(key)

    def delete(self, key: Hashable) -> bool:
        """Remove *key*. Returns True if it was present."""
        return self._data.pop(key, _MISSING) is not _MISSING

    def _evict_one(self) -> None:
        key, value = self._data.popitem(last=False)
        self.stats.evictions += 1
        if self._on_evict is not None:
            self._on_evict(key, value, "capacity")

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data
