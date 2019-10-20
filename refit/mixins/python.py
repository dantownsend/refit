class PythonMixin:
    async def _python_exists(self) -> None:
        await self.in_path(f"python3", raise_exception=True)

    async def _pip_exists(self) -> None:
        await self.in_path(f"pip3", raise_exception=True)

    async def pip(self, package: str) -> None:
        """
        Install a Python package using pip.
        """
        await self._python_exists()
        await self._pip_exists()

        await self.raw(f"pip3 install {package}")
