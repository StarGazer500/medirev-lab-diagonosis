import os
import django
from django.conf import settings
import pytest

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnosing_module.settings')
django.setup()




