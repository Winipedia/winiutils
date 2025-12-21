# winiutils Documentation

<!-- tooling -->
[![pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Container](https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6)](https://podman.io/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![MkDocs](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://www.mkdocs.org/)
<!-- code-quality -->
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)[![mypy](https://img.shields.io/badge/type%20checked-mypy-039dfc.svg)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org/)
[![codecov](https://codecov.io/gh/Winipedia/winiutils/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/winiutils)
<!-- package-info -->
[![PyPI](https://img.shields.io/pypi/v/winiutils?logo=pypi&logoColor=white)](https://pypi.org/project/winiutils/)
[![Python](https://img.shields.io/badge/python-3.12|3.13|3.14-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/Winipedia/winiutils)](https://github.com/Winipedia/winiutils/blob/main/LICENSE)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/winiutils/health_check.yaml?label=CI&logo=github)](https://github.com/Winipedia/winiutils/actions/workflows/health_check.yaml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/winiutils/release.yaml?label=CD&logo=github)](https://github.com/Winipedia/winiutils/actions/workflows/release.yaml)
<!-- documentation -->
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-black?style=for-the-badge&logo=github&logoColor=white)](https://Winipedia.github.io/winiutils)

---

> A utility library for Python development

---

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
