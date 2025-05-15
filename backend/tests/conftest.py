import os

import django
import pytest

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# Configure Django
django.setup()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass 