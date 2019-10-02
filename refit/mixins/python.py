class PythonMixin():

    async def _python_exists(self):
        await self.in_path(f'python3', raise_exception=True)

    async def _pip_exists(self):
        await self.in_path(f'pip3', raise_exception=True)

    async def pip(self, package):
        await self._python_exists()
        await self._pip_exists()

        await self._run(f'pip3 install {package}')
