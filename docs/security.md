# Security

The `winiutils.src.security` package provides cryptography utilities and secure credential storage.

---

## Cryptography

**Module:** `winiutils.src.security.cryptography`

AES-GCM authenticated encryption with automatic IV handling.

### `encrypt_with_aes_gcm()`

Encrypt data using AES-GCM (Galois/Counter Mode).

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winiutils.src.security.cryptography import encrypt_with_aes_gcm

# Create cipher
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)

# Encrypt
plaintext = b"Secret message"
aad = b"metadata"  # Optional additional authenticated data
encrypted = encrypt_with_aes_gcm(aes_gcm, plaintext, aad)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `aes_gcm` | `AESGCM` | Initialized AESGCM cipher instance |
| `data` | `bytes` | Plaintext data to encrypt |
| `aad` | `bytes \| None` | Optional additional authenticated data |

**Returns:** `bytes` — IV (12 bytes) + encrypted data

### `decrypt_with_aes_gcm()`

Decrypt AES-GCM encrypted data.

```python
from winiutils.src.security.cryptography import decrypt_with_aes_gcm

decrypted = decrypt_with_aes_gcm(aes_gcm, encrypted, aad)
assert decrypted == plaintext
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `aes_gcm` | `AESGCM` | Same AESGCM cipher used for encryption |
| `data` | `bytes` | Encrypted data (IV + ciphertext) |
| `aad` | `bytes \| None` | Must match AAD used during encryption |

**Returns:** `bytes` — Original plaintext

---

## Keyring Integration

**Module:** `winiutils.src.security.keyring`

Secure key storage using OS-native credential managers.

### Supported Platforms

| Platform | Backend |
|----------|---------|
| macOS | Keychain |
| Windows | Credential Manager |
| Linux | Secret Service (GNOME Keyring, KWallet) |

### `get_or_create_aes_gcm()`

Get or create a 256-bit AES-GCM key stored in the system keyring.

```python
from winiutils.src.security.keyring import get_or_create_aes_gcm

aes_gcm, raw_key = get_or_create_aes_gcm(
    service_name="my_app",
    username="user@example.com"
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `service_name` | `str` | Application identifier |
| `username` | `str` | User or context identifier |

**Returns:** `tuple[AESGCM, bytes]` — Cipher instance and raw key bytes

### `get_or_create_fernet()`

Get or create a Fernet key stored in the system keyring.

```python
from winiutils.src.security.keyring import get_or_create_fernet

fernet, raw_key = get_or_create_fernet(
    service_name="my_app",
    username="user@example.com"
)

# Fernet provides simpler API with timestamps
token = fernet.encrypt(b"Secret data")
original = fernet.decrypt(token)
```

### `get_or_create_key()`

Generic function for custom key types.

```python
from winiutils.src.security.keyring import get_or_create_key
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Custom key generation
cipher, key = get_or_create_key(
    service_name="my_app",
    username="admin",
    key_class=AESGCM,
    generate_key_func=lambda: AESGCM.generate_key(bit_length=128),
)
```

---

## Complete Example

```python
from winiutils.src.security.keyring import get_or_create_aes_gcm
from winiutils.src.security.cryptography import (
    encrypt_with_aes_gcm,
    decrypt_with_aes_gcm,
)

# Get or create encryption key (stored securely in OS keyring)
aes_gcm, _ = get_or_create_aes_gcm("my_app", "user@example.com")

# Encrypt sensitive data
plaintext = b"Sensitive user data"
aad = b"user_id:123"  # Bind to context
encrypted = encrypt_with_aes_gcm(aes_gcm, plaintext, aad)

# Store encrypted data (e.g., in database)
# ...

# Later, decrypt
decrypted = decrypt_with_aes_gcm(aes_gcm, encrypted, aad)
assert decrypted == plaintext
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Authenticated Encryption** | AES-GCM provides confidentiality and integrity |
| **Random IVs** | Unique 12-byte IV for each encryption |
| **No IV Management** | IV prepended to ciphertext automatically |
| **Service Namespacing** | Key class appended to service name |
| **Idempotent** | Multiple calls return same key |
| **Base64 Encoding** | Safe storage of binary keys |

---

## Security Best Practices

1. **Never hardcode keys** — Always use keyring for key storage

2. **Use AAD for context binding** — Bind encrypted data to its context:
   ```python
   aad = f"user:{user_id}:timestamp:{time.time()}".encode()
   ```

3. **Handle decryption errors** — `InvalidTag` indicates tampering:
   ```python
   from cryptography.exceptions import InvalidTag
   
   try:
       decrypted = decrypt_with_aes_gcm(aes_gcm, data, aad)
   except InvalidTag:
       # Data was tampered with or wrong AAD
       raise SecurityError("Decryption failed")
   ```

4. **Rotate keys periodically** — Delete old keyring entry and re-encrypt data

5. **Limit keyring access** — Ensure only authorized users can access system keyring

---

## Architecture

### Service Name Modification

Service names are automatically modified to prevent key collisions:

```
"my_app" + Fernet → "my_app_Fernet"
"my_app" + AESGCM → "my_app_AESGCM"
```

### GitHub Actions Support

In CI environments, a plaintext keyring backend is used automatically:

```python
if running_in_github_actions():
    keyring.set_keyring(PlaintextKeyring())
```

---

## Use Cases

- Encrypting sensitive application data (passwords, tokens, PII)
- Secure configuration file encryption
- Database credential protection
- API key storage and retrieval
- Multi-user applications with per-user encryption
- Compliance with data protection regulations (GDPR, HIPAA)

