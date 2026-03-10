"""
conftest.py

Root-level pytest configuration.
pytest-playwright automatically provides the `page`, `browser`, and
`playwright` fixtures — no manual fixture definitions needed here.

This file configures:
  - Browser launch options for CI (headless, slow_mo disabled)
  - Base URL so Playwright tests can use relative paths if desired
"""

import pytest


def pytest_configure(config):
    """Register custom markers to avoid PytestUnknownMarkWarning."""
    config.addinivalue_line("markers", "api: API tests against Open Library REST API")
    config.addinivalue_line("markers", "e2e: E2E UI tests against openlibrary.org")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Override default browser context args.
    Sets base_url so E2E tests can navigate with relative paths.
    """
    return {
        **browser_context_args,
        "base_url": "https://openlibrary.org",
    }
