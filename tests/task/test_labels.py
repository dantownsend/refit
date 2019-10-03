import asyncio

from refit.task import Task
from refit.registry import TaskRegistry
from refit.host import Host


registry = TaskRegistry()


COMPLETED = []


class DummyHost(Host):
    username = "foo"
    host = "localhost"


@registry.register(labels=["database"])
class TaskOne(Task):
    async def run(self):
        global RESPONSE
        COMPLETED.append(self.__class__.__name__)


class TestLabels:
    async def run_tasks(self):
        await DummyHost(tasks=registry.members).run()

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne"]
