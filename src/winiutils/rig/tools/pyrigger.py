"""Override pyrig's Pyrigger to add custom dev dependencies."""

from pyrig.rig.tools.pyrigger import Pyrigger as BasePyrigger  # deptry: ignore[DEP004]


class Pyrigger(BasePyrigger):
    """Override pyrig's Pyrigger to add custom dev dependencies."""

    def dev_dependencies(self) -> tuple[str, ...]:
        """Add custom dev dependencies to pyrig's default list."""
        return (*super().dev_dependencies(), "types-tqdm", "types-defusedxml")
