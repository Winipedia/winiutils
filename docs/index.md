# winiutils Documentation

Welcome to the winiutils documentation. This library provides production-ready utilities for Python development.

---

## Modules

### [Data Processing](./data.md)

Tools for data manipulation and cleaning:

- **DataFrame Cleaning Pipeline** — Extensible Polars DataFrame cleaning with an 8-step pipeline
- **Data Structures** — Dictionary utilities and text/string manipulation

### [Iterating & Concurrency](./iterating.md)

Parallel execution framework:

- **Multiprocessing** — CPU-bound parallel processing with spawn context
- **Multithreading** — I/O-bound concurrent execution with ThreadPoolExecutor
- **Timeout Handling** — Decorator for enforcing execution time limits

### [OOP Utilities](./oop.md)

Object-oriented programming patterns:

- **ABCLoggingMeta** — Metaclass for automatic method logging
- **ABCLoggingMixin** — Ready-to-use mixin with built-in logging

### [Security](./security.md)

Cryptography and credential management:

- **AES-GCM Encryption** — Authenticated encryption with automatic IV handling
- **Keyring Integration** — Secure key storage using OS-native credential managers

---

## Quick Links

| Resource | Description |
|----------|-------------|
| [GitHub Repository](https://github.com/Winipedia/winiutils) | Source code and issues |
| [PyPI Package](https://pypi.org/project/winiutils/) | Installation via pip |
| [README](../README.md) | Project overview and quick start |

---

## Requirements

- Python 3.12+
- See `pyproject.toml` for full dependency list

## Installation

```bash
# Using uv (recommended)
uv add winiutils

# Using pip
pip install winiutils
```
