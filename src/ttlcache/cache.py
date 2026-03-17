"""A small in-memory cache."""

from __future__ import annotations

from typing import Any, Hashable

_MISSING = object()


class TTLCache:
    """In-memory key/value cache."""

    def __init__(self) -> None:
        self._data: dict[Hashable, Any] = {}

    def get(self, key: Hashable, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: Hashable, value: Any) -> None:
        self._data[key] = value

    def delete(self, key: Hashable) -> bool:
        """Remove *key*. Returns True if it was present."""
        return self._data.pop(key, _MISSING) is not _MISSING

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data
