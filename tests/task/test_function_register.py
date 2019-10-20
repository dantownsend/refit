"""
Make sure the task_registry can be used in non-decorator form.
"""

import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


host_registry = HostRegistry()
task_registry = TaskRegistry()


COMPLETED = []


@host_registry.register(environment="production", tags=["database"])
class DummyHost(Host):
    username = "foo"
    address = "localhost"


class TaskOne(Task):
    async def run(self):
        global RESPONSE
        COMPLETED.append(self.__class__.__name__)


task_registry.register(TaskOne, tags=["database"])


class TestTags:
    async def run_tasks(self):
        await host_registry.run_tasks(
            tasks=task_registry.task_classes, environment="production"
        )

    def test_register_with_function(self):
        asyncio.run(self.run_tasks())
        assert COMPLETED == ["TaskOne"]
