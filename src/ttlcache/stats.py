"""Counters describing cache behaviour."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def lookups(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        """Fraction of lookups served from cache (0.0 when there were none)."""
        return self.hits / self.lookups if self.lookups else 0.0

    def reset(self) -> None:
        self.hits = self.misses = self.evictions = self.expirations = 0

    def as_dict(self) -> dict[str, float]:
        d: dict[str, float] = dict(asdict(self))
        d["hit_rate"] = self.hit_rate
        return d
