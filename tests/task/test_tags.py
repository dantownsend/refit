import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


host_registry = HostRegistry()
task_registry = TaskRegistry()


COMPLETED = []


host_registry.register(
    Host(name="DummyHost", username="foo", address="localhost"),
    tags=["database"],
)


class TaskOne(Task):
    async def run(self):
        global RESPONSE
        COMPLETED.append(self.__class__.__name__)


task_registry.register(TaskOne(), tags=["database"])


class TestTags:
    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.tasks, environment="production"
        )

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne"]
