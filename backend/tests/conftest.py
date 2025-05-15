import os
from datetime import datetime, timedelta

import django
import jwt
import pytest

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# Configure Django
django.setup()

JWT_SECRET = "your-secret-key-here"

@pytest.fixture
def auth_token():
    expiration = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "id": 1,
        "exp": expiration,
        "type": "access"
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass 