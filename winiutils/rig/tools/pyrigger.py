"""Override pyrig's Pyrigger to add custom dev dependencies."""

from pyrig.rig.tools.pyrigger import Pyrigger as BasePyrigger


class Pyrigger(BasePyrigger):
    """Override pyrig's Pyrigger to add custom dev dependencies."""

    @classmethod
    def get_dev_dependencies(cls) -> list[str]:
        """Add custom dev dependencies to pyrig's default list."""
        return [*super().get_dev_dependencies(), "types-tqdm", "types-defusedxml"]
