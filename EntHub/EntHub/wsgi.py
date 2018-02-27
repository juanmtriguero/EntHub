"""
WSGI config for EntHub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Heroku
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EntHub.heroku_settings")

application = get_wsgi_application()
