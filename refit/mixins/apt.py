from .base import MixinBase


class AptMixin(MixinBase):
    async def apt_update(self) -> None:
        await self.raw("apt-get update")

    async def apt_autoremove(self) -> None:
        await self.raw("apt-get autoremove")

    async def apt_install(self, *packages: str) -> None:
        package_list = " ".join(packages)
        await self.raw(f"yes | apt-get install {package_list}")
