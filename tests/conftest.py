"""Pytest configuration for tests.

This defines the pyrig pytest plugin that provides access to pyrig's test
infrastructure, including fixtures, hooks, and test utilities.
"""

pytest_plugins = ["pyrig.rig.tests.conftest"]

"""Pytest configuration for tests.

This module configures pytest plugins for the test suite, setting up the necessary
fixtures and hooks for the different
test scopes (function, class, module, package, session).
It also import custom plugins from tests/base/scopes.
This file should not be modified manually.
"""

pytest_plugins = ["pyrig.dev.tests.conftest"]
