import asyncio

from refit.task import Task
from refit.registry import TaskRegistry, HostRegistry
from refit.host import Host


RESPONSE = ""


host_registry = HostRegistry()
task_registry = TaskRegistry()


@host_registry.register(environment="production")
class DockerHost(Host):
    """
    Connects to a SSH server running under Docker.
    """

    username = "root"
    address = "localhost"
    connection_params = {"password": "root", "known_hosts": None}


@task_registry.register
class TaskOne(Task):
    async def run(self):
        global RESPONSE
        RESPONSE = (await self.raw("cat /etc/os-release")).stdout


class TestConnection:
    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.task_classes, environment="production"
        )

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert "Ubuntu" in RESPONSE
