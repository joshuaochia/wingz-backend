import pytest
from django.conf import settings


@pytest.fixture(scope='session', autouse=True)
def setup_test_settings():
    """Override settings for tests."""
    # Faster password hashing
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]