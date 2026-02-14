# base/tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email='admin@example.com',
        password='testpass123',
        role='admin',
        username='admin1',
        is_staff=True
    )


@pytest.fixture
def rider(db):
    return User.objects.create_user(
        email='rider@example.com',
        password='testpass123',
        role='rider',
        username='rider1'
    )


@pytest.fixture
def driver(db):
    return User.objects.create_user(
        email='driver@example.com',
        password='testpass123',
        role='driver',
        username='driver1'
    )


@pytest.fixture
def authenticated_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client