import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


COMPLETED = []


host_registry = HostRegistry()
task_registry = TaskRegistry()


host_registry.register(
    Host(name="DummyHost", username="foo", address="localhost"),
    environment="production",
)


class TaskOne(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


class TaskTwo(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


task_registry.register(TaskOne(), TaskTwo())


class TestTasks:
    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.tasks, environment="production"
        )

    @classmethod
    def setup_class(cls):
        global COMPLETED
        COMPLETED = []

    def test_sequence(self):
        """
        Makes sure the tasks get executed in the correct sequence.
        """
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne", "TaskTwo"]
