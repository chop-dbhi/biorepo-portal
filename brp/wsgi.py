"""
WSGI config for brp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

# from django.core.wsgi import get_wsgi_application
# from configurations.wsgi import get_wsgi_application
# import django.core.handlers.wsgi
from dj_static import Cling
# from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brp.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
# application = WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = Cling(get_wsgi_application())
# application = django.core.handlers.wsgi.WSGIHandler()
