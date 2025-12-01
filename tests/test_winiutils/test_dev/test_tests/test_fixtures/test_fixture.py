"""module."""

from collections.abc import Callable


def test_keyring_cleanup(keyring_cleanup: Callable[[str, str], None]) -> None:
    """Test function."""
    assert callable(keyring_cleanup), "Expected keyring_cleanup to be callable"
