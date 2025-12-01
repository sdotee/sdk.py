"""Shared test fixtures and configuration."""

import pytest


@pytest.fixture
def api_key() -> str:
    """Return a test API key."""
    return "test-api-key-12345"


@pytest.fixture
def base_url() -> str:
    """Return a test base URL."""
    return "https://api.test.see.url"


@pytest.fixture
def sample_url() -> str:
    """Return a sample URL for testing."""
    return "https://example.com/very/long/url/path"
