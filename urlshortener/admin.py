"""
Customizing the AdminSite to register our Model to Admin Interface
"""

from django.contrib import admin
from .models import URL

admin.site.register(URL)
