"""
A view is a “type” of Web page in your Django application that
generally serves a specific function and has a specific template.
"""
import hashlib
import logging
from base64 import urlsafe_b64encode
from urllib.parse import urlparse

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings
from django.views.decorators.cache import never_cache

from .models import URL

logger = logging.getLogger(__name__)


def _get_normalized_url(url) -> str:
    """
    Helper function to get normalized url.
    Normalized url is a url that contain scheme - http or https.

    :param url: url to normalize
    :return: normalized url
    """
    o = urlparse(url.encode('utf-8'))

    if o.scheme not in (b'http', b'https'):
        url = "http://" + url
        logger.debug('Normalized url is %s', url)

    return url


def _get_hashable_url(url, limit=settings.SHORT_URL_MIN_LENGTH) -> str:
    """
    Helper function to generate hexdigest on md5 hashable url with length limit.
    The above code takes string and converts it into the byte equivalent using encode()
    so that it can be accepted by the hash function.
    The md5 hash function encodes it and then using hexdigest(), hexadecimal equivalent encoded string is printed.

    Hashing functions is important to avoid possible bruteforce attack.

    :param url: url to calculate hash and digest
    :param limit: limit number of string to return
    :return: hexdigest
    """
    ret = cache.get_or_set(key=urlsafe_b64encode(url.encode('utf-8'))[:244],
                           default=hashlib.md5(url.encode('utf-8')).hexdigest(),
                           timeout=3)

    return ret[:limit]


@never_cache
def page_not_found(request, exception) -> HttpResponse:
    """
    View function for 404 error handler

    :param request:
    :param exception:
    :return:
    """
    context = {
        'error_message': str(exception)
    }

    response = render(request=request, template_name='index.html', context=context)
    response.status_code = 404

    return response


@never_cache
def top10(request) -> HttpResponse:
    """
    View function for Top10 page

    :param request:
    :return: HttpResponse
    """

    urls = URL.objects.order_by('-usage_count')[0:10]

    context = {
        'urls': urls,
        'error_message': None
    }

    return render(request=request, template_name='top10.html', context=context)


def index(request) -> HttpResponse:
    """
    View function for home page of site

    :param request:
    :return:
    """

    context = {
        'error_message': None
    }

    return render(request=request, template_name='index.html', context=context)


@never_cache
def shorten(request) -> HttpResponse:
    """
    View function for shorten http request

    :param request:
    :return:
    """
    if request.method == 'GET':
        return redirect('/')

    error_message = None
    tiny = None
    status_code = 200

    try:
        target = _get_normalized_url(request.POST["target"])

        try:
            tiny = URL.objects.get(target=target)
            logger.info('Record %s already exists. Points to %s', tiny, target)

        except URL.DoesNotExist:
            tries = 0

            while tries <= settings.SHORT_URL_MAX_LENGTH_SCALING:
                tiny = _get_hashable_url(target, limit=settings.SHORT_URL_MIN_LENGTH+tries)
                try:
                    """
                        In case of collision, it shifts through the md5 hexdigest until an available SHORT_URL_MAX_LENGTH_SCALING
                        character window is found
                    """
                    if URL.objects.get(tiny=tiny):
                        raise Exception("Collision occurred for %s, Trying to scale tiny size", tiny)
                except URL.DoesNotExist:
                    break
                except Exception as e:
                    logger.warning(e)
                    tries += 1

                    continue
            else:
                if tries > settings.SHORT_URL_MAX_LENGTH_SCALING:
                    raise Exception("Max tries %s exceeded. Not enough entropy. "
                                    "Please increase SHORT_URL_MAX_LENGTH_SCALING" % settings.SHORT_URL_MAX_LENGTH_SCALING)

            logger.debug('Add tiny record %s to %s', tiny, target)

            entry = URL(tiny=tiny, target=target)
            entry.save(force_insert=True)

    except Exception as e:
        error_message = e
        status_code = 500

    context = {
        'tiny': tiny,
        'error_message': error_message
    }

    return render(request=request, template_name='index.html', context=context, status=status_code)


def retrieve(request, tiny) -> HttpResponseRedirect:
    """
    View function for tinyies and redirect client

    :param request:
    :param tiny:
    :return:
    """

    url = get_object_or_404(URL, tiny=tiny)

    try:
        url.usage_count += 1
        url.save(update_fields=["usage_count"])
    except Exception as e:
        logger.warning(e)

    logger.debug('Send redirect for tiny %s to %s', tiny, url.target)

    return redirect(url.target, permanent=False)
