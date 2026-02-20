"""Shared pytest configuration for markdown-to-pdf tests."""


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: requires external tools (mmdc/playwright)"
    )
