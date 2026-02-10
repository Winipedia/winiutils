"""module."""

from winiutils.rig.tools.pyrigger import Pyrigger


class TestPyrigger:
    """Test class."""

    def test_get_dev_dependencies(self) -> None:
        """Test method."""
        result = Pyrigger.get_dev_dependencies()
        assert "types-tqdm" in result
        assert "types-defusedxml" in result
