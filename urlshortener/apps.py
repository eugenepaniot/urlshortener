"""
Django contains a registry of installed applications that stores configuration and provides introspection.
It also maintains a list of available models.

This registry is called apps and it’s available in django.apps:

"""
from django.apps import AppConfig


class URLshortenerConfig(AppConfig):
    """
    AppConfig for URLshortenerConfig application
    """

    name = 'urlshortener'
    verbose_name = 'URL Shortener'
