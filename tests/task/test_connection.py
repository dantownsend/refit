import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


RESPONSE = ""


host_registry = HostRegistry()
task_registry = TaskRegistry()


host_registry.register(
    Host(
        name="DockerHost",
        username="root",
        address="localhost",
        connection_params={"password": "root", "known_hosts": None},
    ),
    environment="production",
)


class TaskOne(Task):
    async def run(self):
        global RESPONSE
        RESPONSE = (await self.raw("cat /etc/os-release")).stdout


task_registry.register(TaskOne())


class TestConnection:
    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.tasks, environment="production"
        )

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert "Ubuntu" in RESPONSE
