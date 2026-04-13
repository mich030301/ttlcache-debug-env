import ttlcache


def test_version_is_exposed():
    assert isinstance(ttlcache.__version__, str)
    assert ttlcache.__version__.count(".") == 2


def test_public_api():
    assert set(ttlcache.__all__) == {"TTLCache", "__version__"}
