"""Conftest file."""

from collections.abc import Callable, Iterator
from pathlib import Path

import keyring
import pytest  # deptry: ignore[DEP004]
from keyrings.alt.file import PlaintextKeyring  # deptry: ignore[DEP004]


@pytest.fixture
def keyring_cleanup(tmp_path: Path) -> Iterator[Callable[[str, str], None]]:
    """Factory fixture to clean up keyring entries after test.

    Swaps in a private per-test PlaintextKeyring backend (a file under
    tmp_path) instead of whatever backend is configured for the process, so
    tests never touch a developer's real OS keyring and stay isolated from
    each other, including across parallel pytest-xdist workers.

    Usage:
        def test_something(keyring_cleanup):
            keyring_cleanup("service_name", "username")
            # ... test code that creates keyring entries ...
    """
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

    keyring.set_keyring(previous_keyring)
