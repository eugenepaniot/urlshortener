import pytest

from urlshortener.views import _get_hashable_url, _get_normalized_url


@pytest.mark.parametrize(
    'target, tiny', [
        ('http://127.0.0.1', '5c016e8f'),
        ('http://::1', 'f48589f0'),
        ('http://fe80::2e59:e5ff:fe42:398c', 'cd491bff'),
        ('http://localhost', '86a9106a'),
        ('http://localhost.localdomain', 'f6f809c2'),
    ]
)
def test_unit__get_hashable_url(target, tiny):
    assert tiny == _get_hashable_url(target)


@pytest.mark.parametrize(
    'target, tiny, limit', [
    ]
)
def test_unit__get_hashable_url_with_limit(target, tiny, limit):
    assert tiny == _get_hashable_url(target, limit)


@pytest.mark.parametrize(
    'url, normalized_url', [
        ('127.0.0.1', 'http://127.0.0.1'),
    ]
)
def test_unit__get_normalized_url(url, normalized_url):
    assert normalized_url == _get_normalized_url(url)
