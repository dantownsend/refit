import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


COMPLETED = []


host_registry = HostRegistry()


@host_registry.register()
class DummyHost(Host):
    username = "foo"
    address = "localhost"


registry = TaskRegistry()


@registry.register
class TaskOne(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


class TestDecorator:
    async def run_tasks(self):
        await TaskOne.create(
            host_registry=host_registry, environment="production"
        )

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne"]
