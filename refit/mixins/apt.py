class AptMixin():

    async def apt_update(self):
        await self._run(
            'apt update'
        )

    async def apt_autoremove(self):
        await self._run(
            'apt autoremove'
        )

    async def apt(self, *packages):
        package_list = ' '.join(packages)
        await self._run(
            f'yes | apt install {package_list}'
        )
