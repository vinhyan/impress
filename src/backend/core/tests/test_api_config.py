"""
Test config API endpoints in the Impress core app.
"""

from django.test import override_settings

import pytest
from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.test import APIClient

from core import factories

pytestmark = pytest.mark.django_db


@override_settings(
    COLLABORATION_SERVER_URL="http://testcollab/",
    FRONTEND_THEME="test-theme",
    MEDIA_BASE_URL="http://testserver/",
    SENTRY_DSN="https://sentry.test/123",
)
def test_api_config_anonymous():
    """Anonymous users should be allowed to get the configuration."""
    client = APIClient()
    response = client.get("/api/v1.0/config/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "COLLABORATION_SERVER_URL": "http://testcollab/",
        "ENVIRONMENT": "test",
        "FRONTEND_THEME": "test-theme",
        "LANGUAGES": [["en-us", "English"], ["fr-fr", "French"], ["de-de", "German"]],
        "LANGUAGE_CODE": "en-us",
        "MEDIA_BASE_URL": "http://testserver/",
        "SENTRY_DSN": "https://sentry.test/123",
    }


@override_settings(
    COLLABORATION_SERVER_URL="http://testcollab/",
    FRONTEND_THEME="test-theme",
    MEDIA_BASE_URL="http://testserver/",
    SENTRY_DSN="https://sentry.test/123",
)
def test_api_config_authenticated():
    """Authenticated users should be allowed to get the configuration."""
    user = factories.UserFactory()

    client = APIClient()
    client.force_login(user)

    response = client.get("/api/v1.0/config/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "COLLABORATION_SERVER_URL": "http://testcollab/",
        "ENVIRONMENT": "test",
        "FRONTEND_THEME": "test-theme",
        "MEDIA_BASE_URL": "http://testserver/",
        "LANGUAGES": [["en-us", "English"], ["fr-fr", "French"], ["de-de", "German"]],
        "LANGUAGE_CODE": "en-us",
        "SENTRY_DSN": "https://sentry.test/123",
    }
