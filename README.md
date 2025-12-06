# winiutils

[![built with pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=python&logoColor=white)](https://github.com/Winipedia/pyrig)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)

A comprehensive Python utility library providing production-ready tools for data processing, concurrent execution, security, and object-oriented programming patterns.

> Built with [pyrig](https://github.com/Winipedia/pyrig)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Modules](#modules)
- [Development](#development)
- [License](#license)

---

## Features

- **DataFrame Cleaning Pipeline** — Extensible Polars DataFrame cleaning with an 8-step pipeline
- **Concurrent Processing** — Unified multiprocessing and multithreading with automatic resource optimization
- **OOP Utilities** — Metaclasses and mixins for automatic method logging and instrumentation
- **Security Tools** — OS keyring integration and AES-GCM encryption utilities
- **Type Safety** — Full type hints with strict mypy compliance
- **Production Ready** — Comprehensive test coverage and logging integration

---

## Installation

### Using uv (recommended)

```bash
uv add winiutils
```

### Using pip

```bash
pip install winiutils
```

### From source

```bash
git clone https://github.com/Winipedia/winiutils.git
cd winiutils
uv sync
```

---

## Quick Start

### DataFrame Cleaning

```python
from winiutils.src.data.dataframe.cleaning import CleaningDF
import polars as pl

class UserDataCleaner(CleaningDF):
    """Clean and standardize user data."""

    USER_ID = "user_id"
    EMAIL = "email"
    SCORE = "score"

    @classmethod
    def get_rename_map(cls):
        return {cls.USER_ID: "UserId", cls.EMAIL: "Email", cls.SCORE: "Score"}

    @classmethod
    def get_col_dtype_map(cls):
        return {cls.USER_ID: pl.Int64, cls.EMAIL: pl.Utf8, cls.SCORE: pl.Float64}

    # ... implement other abstract methods

# Usage
cleaned = UserDataCleaner(raw_dataframe)
result = cleaned.df
```

### Concurrent Processing

```python
from winiutils.src.iterating.concurrent.multiprocessing import multiprocess_loop
from winiutils.src.iterating.concurrent.multithreading import multithread_loop

# CPU-bound tasks (multiprocessing)
def process_chunk(data, config):
    return heavy_computation(data, config)

results = multiprocess_loop(
    process_function=process_chunk,
    process_args=[(chunk,) for chunk in data_chunks],
    process_args_static=(config,),
    process_args_len=len(data_chunks),
)

# I/O-bound tasks (multithreading)
def fetch_url(url, headers):
    return requests.get(url, headers=headers)

results = multithread_loop(
    process_function=fetch_url,
    process_args=[(url,) for url in urls],
    process_args_static=(headers,),
    process_args_len=len(urls),
)
```

### Automatic Method Logging

```python
from winiutils.src.oop.mixins.mixin import ABCLoggingMixin

class MyService(ABCLoggingMixin):
    def process_data(self, data: list) -> dict:
        # Automatically logged with timing
        return {"processed": len(data)}

# Logs: "MyService - Calling process_data with (...) and {...}"
# Logs: "MyService - process_data finished with 0.5 seconds -> returning {...}"
```

### Encryption with Keyring

```python
from winiutils.src.security.keyring import get_or_create_aes_gcm
from winiutils.src.security.cryptography import encrypt_with_aes_gcm, decrypt_with_aes_gcm

# Get or create encryption key (stored in OS keyring)
aes_gcm, key = get_or_create_aes_gcm("my_app", "user@example.com")

# Encrypt and decrypt
encrypted = encrypt_with_aes_gcm(aes_gcm, b"Secret message")
decrypted = decrypt_with_aes_gcm(aes_gcm, encrypted)
```

---

## Documentation

Full documentation is available in the [docs](./docs/) folder:

- [**Data Processing**](./docs/data.md) — DataFrame cleaning pipeline and data structures
- [**Iterating & Concurrency**](./docs/iterating.md) — Parallel processing utilities
- [**OOP Utilities**](./docs/oop.md) — Metaclasses and mixins
- [**Security**](./docs/security.md) — Encryption and keyring integration

---

## Modules

| Module | Description |
|--------|-------------|
| [`winiutils.src.data`](./docs/data.md) | DataFrame cleaning pipeline and data structure utilities |
| [`winiutils.src.iterating`](./docs/iterating.md) | Concurrent processing with multiprocessing and multithreading |
| [`winiutils.src.oop`](./docs/oop.md) | Metaclasses and mixins for automatic method logging |
| [`winiutils.src.security`](./docs/security.md) | AES-GCM encryption and OS keyring integration |

---

## Development

### Setup

```bash
git clone https://github.com/Winipedia/winiutils.git
cd winiutils
uv sync --all-groups
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Type checking
uv run mypy .

# Security scanning
uv run bandit -r winiutils/
```

### Pre-commit Hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

---

## Project Structure

```
winiutils/
├── src/                          # Main source code
│   ├── data/                     # Data processing
│   │   ├── dataframe/            # Polars DataFrame cleaning
│   │   └── structures/           # Dicts, text utilities
│   ├── iterating/                # Iteration utilities
│   │   └── concurrent/           # Multiprocessing & multithreading
│   ├── oop/                      # OOP patterns
│   │   └── mixins/               # Logging metaclass & mixin
│   └── security/                 # Security utilities
│       ├── cryptography.py       # AES-GCM encryption
│       └── keyring.py            # OS keyring integration
├── dev/                          # Development tools
│   ├── cli/                      # CLI subcommands
│   └── tests/fixtures/           # Test fixtures
├── docs/                         # Documentation
└── tests/                        # Test suite
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass (`uv run pytest`)
2. Code passes linting (`uv run ruff check .`)
3. Types are correct (`uv run mypy .`)
4. New features include tests
5. Documentation is updated for API changes