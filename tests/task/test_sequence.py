import asyncio

from refit.task import Task
from refit.registry import TaskRegistry
from refit.host import Host


COMPLETED = []


class DummyHost(Host):
    username = "foo"
    host = "localhost"


registry = TaskRegistry()


class TaskOne(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


class TaskTwo(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


class TestTasks:
    async def run_tasks(self):
        await DummyHost(tasks=registry.members).run()

    @classmethod
    def setup_class(cls):
        global COMPLETED
        COMPLETED = []

    def test_sequence(self):
        """
        Makes sure the tasks get executed in the correct sequence.
        """
        registry.register(TaskOne, TaskTwo)
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne", "TaskTwo"]
