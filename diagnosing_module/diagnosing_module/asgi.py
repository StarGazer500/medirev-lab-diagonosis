"""
ASGI config for diagnosing_module project.

It exposes the ASGI calMedirevle as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnosing_module.settings')

application = get_asgi_application()
