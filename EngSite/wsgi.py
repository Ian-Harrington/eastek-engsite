"""
WSGI config for EngSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

if os.environ.get("DJANGO_SETTINGS_MODULE"):
	pass   # use present settings (heroku/deployment) 
else:
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EngSite.settings.local")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)