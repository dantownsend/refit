from .base import MixinBase


class PathMixin(MixinBase):
    """
    Utilities for inspecting the path on the remote machine.
    """

    async def in_path(self, executable: str, raise_exception=False) -> bool:
        """
        Check whether an executable is available on the path.
        """
        response = await self.raw(f"which {executable}")

        if (response.exit_status == 1) and raise_exception:
            raise Exception(f"{executable} doesn't exist!")

        return response.exit_status != 1
