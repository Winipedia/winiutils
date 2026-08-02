"""Conftest file."""

import os
from collections.abc import Callable, Iterator
from pathlib import Path

import keyring
import pytest  # deptry: ignore[DEP004]
from keyrings.alt.file import PlaintextKeyring  # deptry: ignore[DEP004]


@pytest.fixture
def keyring_cleanup(tmp_path: Path) -> Iterator[Callable[[str, str], None]]:
    """Factory fixture to clean up keyring entries after test.

    In CI, winiutils.core.security.keyring switches to keyrings.alt's
    PlaintextKeyring, which stores all entries in a single shared file with
    no locking. Under pytest-xdist that file is shared by every worker, so
    concurrent tests can clobber each other's writes. Point the backend at a
    private per-test file to avoid that race.

    Usage:
        def test_something(keyring_cleanup):
            keyring_cleanup("service_name", "username")
            # ... test code that creates keyring entries ...
    """
    previous_keyring = None
    if os.getenv("GITHUB_ACTIONS", "false") == "true":
        previous_keyring = keyring.get_keyring()
        isolated_keyring = PlaintextKeyring()
        isolated_keyring.file_path = str(tmp_path / "keyring_pass.cfg")  # ty: ignore[invalid-assignment]
        keyring.set_keyring(isolated_keyring)

    entries: list[tuple[str, str]] = []

    def register(service_name: str, username: str) -> None:
        entries.append((service_name, username))

    yield register

    for service_name, username in entries:
        keyring.delete_password(service_name, username)

    if previous_keyring is not None:
        keyring.set_keyring(previous_keyring)
