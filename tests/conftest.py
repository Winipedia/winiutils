"""Pytest configuration for automatic fixture discovery across the pyrig ecosystem.

Registers fixture modules from pyrig and all installed packages that depend on
it as pytest plugins. This makes all discovered fixtures available in every
test module without explicit imports.

The registration walks the ``<project_name>.rig.tests.fixtures`` package path in
pyrig and all pyrig dependent packages, collecting all Python modules except
``__init__.py`` modules and registers them as plugins.
"""

from collections.abc import Callable, Iterator

import keyring
import pytest  # deptry: ignore[DEP004]


@pytest.fixture
def keyring_cleanup() -> Iterator[Callable[[str, str], None]]:
    """Factory fixture to clean up keyring entries after test.

    Usage:
        def test_something(keyring_cleanup):
            keyring_cleanup("service_name", "username")
            # ... test code that creates keyring entries ...
    """
    entries: list[tuple[str, str]] = []

    def register(service_name: str, username: str) -> None:
        entries.append((service_name, username))

    yield register

    for service_name, username in entries:
        keyring.delete_password(service_name, username)


pytest_plugins = [
    "pyrig_fixtures.rig.tests.conftest",
]
