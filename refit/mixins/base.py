from abc import ABC, abstractmethod


class MixinBase(ABC):
    @abstractmethod
    async def raw(self, command: str, raise_exception=True):
        pass
