import pytest

from ttlcache import TTLCache
from ttlcache.errors import InvalidCapacityError, InvalidTTLError


@pytest.mark.parametrize("bad", [0, -1, -100])
def test_rejects_non_positive_capacity(bad):
    with pytest.raises(InvalidCapacityError):
        TTLCache(capacity=bad)


def test_capacity_error_is_a_value_error():
    with pytest.raises(ValueError):
        TTLCache(capacity=0)


@pytest.mark.parametrize("bad", [0, -1, -0.5])
def test_rejects_non_positive_default_ttl(bad):
    with pytest.raises(InvalidTTLError):
        TTLCache(ttl=bad)


@pytest.mark.parametrize("bad", [0, -3])
def test_rejects_non_positive_per_key_ttl(bad):
    c = TTLCache()
    with pytest.raises(InvalidTTLError):
        c.set("a", 1, ttl=bad)
