"""Tests for winipedia_utils.security.keyring module."""

import uuid
from collections.abc import Callable

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from winiutils.src.security.keyring import (
    get_key_as_str,
    get_or_create_aes_gcm,
    get_or_create_fernet,
    get_or_create_key,
    make_service_name,
)

SERVICE_NAME = f"test_keyring_{uuid.uuid4().hex}"
USERNAME = "test_user"
AES_256_KEY_BYTES = 32


def test_get_or_create_fernet(keyring_cleanup: Callable[[str, str], None]) -> None:
    """Test get_or_create_fernet creates and retrieves keys."""
    keyring_cleanup(f"{SERVICE_NAME}_Fernet", USERNAME)

    fernet, key = get_or_create_fernet(SERVICE_NAME, USERNAME)
    assert isinstance(fernet, Fernet)
    assert fernet.decrypt(fernet.encrypt(b"test")) == b"test"

    _, key2 = get_or_create_fernet(SERVICE_NAME, USERNAME)
    assert key == key2


def test_get_or_create_aes_gcm(keyring_cleanup: Callable[[str, str], None]) -> None:
    """Test get_or_create_aes_gcm creates and retrieves keys."""
    keyring_cleanup(f"{SERVICE_NAME}_AESGCM", USERNAME)

    aesgcm, key = get_or_create_aes_gcm(SERVICE_NAME, USERNAME)
    assert isinstance(aesgcm, AESGCM)

    nonce = b"123456789012"
    assert aesgcm.decrypt(nonce, aesgcm.encrypt(nonce, b"test", None), None) == b"test"

    _, key2 = get_or_create_aes_gcm(SERVICE_NAME, USERNAME)
    assert key == key2


def test_get_or_create_key(keyring_cleanup: Callable[[str, str], None]) -> None:
    """Test get_or_create_key with custom key class."""
    keyring_cleanup(f"{SERVICE_NAME}_AESGCM", USERNAME)

    aesgcm, key = get_or_create_key(
        SERVICE_NAME, USERNAME, AESGCM, lambda: AESGCM.generate_key(bit_length=256)
    )
    assert isinstance(aesgcm, AESGCM)
    assert len(key) == AES_256_KEY_BYTES


def test_get_key_as_str(keyring_cleanup: Callable[[str, str], None]) -> None:
    """Test get_key_as_str returns stored key string."""
    keyring_cleanup(f"{SERVICE_NAME}_Fernet", USERNAME)

    assert get_key_as_str(SERVICE_NAME, USERNAME, Fernet) is None

    get_or_create_fernet(SERVICE_NAME, USERNAME)
    result = get_key_as_str(SERVICE_NAME, USERNAME, Fernet)
    assert result is not None


def test_make_service_name() -> None:
    """Test make_service_name combines service and class name."""
    assert make_service_name("my_service", Fernet) == "my_service_Fernet"
    assert make_service_name("my_service", AESGCM) == "my_service_AESGCM"
