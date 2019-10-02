class PathMixin():
    """
    Utilities for inspecting the path on the remote machine.
    """

    async def in_path(self, executable, raise_exception=False):
        """
        Check whether an executable is available on the path.
        """
        response = await self._run(f'which {executable}')

        if (response.exit_status == 1) and raise_exception:
            raise Exception(f"{executable} doesn't exist!")

        return (response.exit_status != 1)
