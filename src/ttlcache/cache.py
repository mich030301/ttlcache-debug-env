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
