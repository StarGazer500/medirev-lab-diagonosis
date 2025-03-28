"""
WSGI config for diagnosing_module project.

It exposes the WSGI calMedirevle as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnosing_module.settings')

application = get_wsgi_application()
