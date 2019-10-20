import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


host_registry = HostRegistry()
task_registry = TaskRegistry()


COMPLETED = []


@host_registry.register(tags=["database"])
class DummyHost(Host):
    username = "foo"
    address = "localhost"


@task_registry.register(tags=["database"])
class TaskOne(Task):
    async def run(self):
        global RESPONSE
        COMPLETED.append(self.__class__.__name__)


class TestTags:
    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.task_classes, environment="production"
        )

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne"]
