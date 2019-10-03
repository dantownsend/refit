import asyncio

from refit.task import Task
from refit.registry import TaskRegistry
from refit.host import Host


RESPONSE = ""


class DockerHost(Host):
    """
    Connects to a SSH server running under Docker.
    """

    username = "root"
    host = "localhost"
    connection_params = {"password": "root"}


registry = TaskRegistry()


@registry.register
class TaskOne(Task):
    async def run(self):
        global RESPONSE
        RESPONSE = (await self.raw("cat /etc/os-release")).stdout


class TestConnection:
    async def run_tasks(self):
        await DockerHost(tasks=registry.members).run()

    def test_decorator(self):
        asyncio.run(self.run_tasks())
        assert "Ubuntu" in RESPONSE
