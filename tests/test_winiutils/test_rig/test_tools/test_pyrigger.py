"""module."""

from winiutils.rig.tools.pyrigger import Pyrigger


class TestPyrigger:
    """Test class."""

    def test_dev_dependencies(self) -> None:
        """Test method."""
        result = Pyrigger.dev_dependencies()
        assert "types-tqdm" in result
        assert "types-defusedxml" in result
