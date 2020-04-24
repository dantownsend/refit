import asyncio
import os
import subprocess

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
        await self.apt_update()
        await self.apt_install("apt-utils")
        await self.apt_install("rolldice")
        global RESPONSE
        RESPONSE = (await self.raw("/usr/games/rolldice -v")).stdout


task_registry.register(TaskOne())


class TestConnection:
    def setup_class(self):
        path = os.path.dirname(os.path.dirname(__file__))
        for script in ("remove_target.sh", "start_target.sh"):
            script_path = os.path.join(path, script)
            subprocess.call(script_path)

    async def run_tasks(self):
        await host_registry.run_tasks(
            task_registry.tasks, environment="production"
        )

    def test_apt_install(self):
        asyncio.run(self.run_tasks())
        assert "rolldice" in RESPONSE
