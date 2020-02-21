import pprint
from string import punctuation, printable, whitespace

import pytest
from django.urls import reverse

from urlshortener.views import _get_normalized_url


@pytest.mark.django_db
def test_view_index(client):
    url = reverse('index')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_view_top10(client):
    url = reverse('top10')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_view_shorten(client):
    url = reverse('shorten')
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.xfail(strict=True)
@pytest.mark.django_db
@pytest.mark.parametrize(
    'target', [
        pytest.param(None),
        "http://",
        "https://"
    ]+list(punctuation+whitespace)
)
def test_view_shorten_post_invalid(client, target):
    url = reverse('shorten')
    response = client.post(url, data={"target": target})
    pprint.pprint(response)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'tiny', [
        "1",
        "2",
        "3"
    ]
)
def test_view_get_invalid(client, tiny):
    url = reverse('retrieve', args=(tiny,))
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    'target, tiny', [
        ('http://127.0.0.1', '5c016e8f'),
        ('http://localhost', '86a9106a'),
        ('http://localhost.localdomain', 'f6f809c2')
    ]
)
def test_view_shorten_post(client, target, tiny):
    url = reverse('shorten')
    response = client.post(url, data={"target": target})

    assert response.status_code == 200

    url = reverse('retrieve', args=(tiny,))
    response = client.get(url)

    assert response.status_code == 302
    assert response['Location'] == _get_normalized_url(target)
