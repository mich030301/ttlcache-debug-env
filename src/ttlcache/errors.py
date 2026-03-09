"""Exception types raised by ttlcache."""


class CacheError(Exception):
    """Base class for all ttlcache errors."""


class InvalidCapacityError(CacheError, ValueError):
    """Raised when a cache is created with a non-positive capacity."""

    def __init__(self, capacity: object) -> None:
        super().__init__(f"capacity must be a positive integer, got {capacity!r}")


class InvalidTTLError(CacheError, ValueError):
    """Raised when a non-positive TTL is supplied."""

    def __init__(self, ttl: object) -> None:
        super().__init__(f"ttl must be a positive number of seconds, got {ttl!r}")
