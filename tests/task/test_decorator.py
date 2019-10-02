import asyncio

from refit.task import Task
from refit.registry import TaskRegistry
from refit.host import Host


COMPLETED = []


class DummyHost(Host):
    username = "foo"
    host = "localhost"


registry = TaskRegistry()


@registry.register
class TaskOne(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


class TestDecorator:
    async def run_tasks(self):
        await DummyHost(tasks=registry.members).run()

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne"]
