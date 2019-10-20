import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


COMPLETED = []


host_registry = HostRegistry()
task_registry = TaskRegistry()


@host_registry.register(environment="production")
class DummyHost(Host):
    username = "foo"
    address = "localhost"


@task_registry.register
class TaskOne(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


@task_registry.register
class TaskTwo(Task):
    async def run(self):
        COMPLETED.append(self.__class__.__name__)


class TestTasks:
    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.task_classes, environment="production"
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
