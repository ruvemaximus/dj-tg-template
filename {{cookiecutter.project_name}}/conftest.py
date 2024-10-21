"""Набор фикстур для автотестов."""

import pytest
from django.test import Client


@pytest.fixture
def user(django_user_model):
    """Фикстура для создания пользователя."""
    user = django_user_model.objects.create_user(email="test@test.com", password="***")
    yield user
    # user.delete()


@pytest.fixture
def client(user):
    """Фикстура для создания клиента."""
    c = Client()
    c.force_login(user)
    return c
