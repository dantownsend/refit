import asyncio
import time

from termcolor import colored

from .mixins.apt import AptMixin
from .mixins.docker import DockerMixin
from .mixins.file import FileMixin
from .mixins.path import PathMixin
from .mixins.python import PythonMixin
from .mixins.systemd import SystemdMixin
from .mixins.template import TemplateMixin


class Task(
    AptMixin,
    DockerMixin,
    FileMixin,
    PathMixin,
    PythonMixin,
    SystemdMixin,
    TemplateMixin,
):
    def __init__(self, host):
        self.host = host

    async def entrypoint(self) -> None:
        """
        Called instead of run - so we don't have to use super() from every
        run method.
        """
        message = f"Task {self.__class__.__name__}"
        line_length = int((100 - len(message)) / 2)
        line = "".join(["-" for i in range(line_length)])
        print(colored(f"{line} {message} {line}", "cyan"))
        await self.run()

    async def run(self) -> None:
        """
        Override in subclasses. This is what does the actual work in the task,
        and is awaited when the Task is run.
        """
        print("Override me ...")

    ###########################################################################

    async def raw(self, command, raise_exception=True):
        """
        What does this do??? Vs just _run???
        """
        return await self._run(command, raise_exception)

    ###########################################################################

    def _print_command(self, command: str) -> None:
        print(colored(f"{command}", "green"))

    async def _run(self, command, raise_exception=True):
        started_at = time.time()
        connection = await self.host.get_connection()

        result = await connection.run(
            command,
            # check=True
        )
        finished_at = time.time()
        took = finished_at - started_at

        self._print_command(f"Running: {command}")

        stdout = colored(result.stdout, "magenta")
        stderr = colored(result.stderr, "red")

        print(
            f"Started at:  {started_at}\n"
            f"Finished at: {finished_at}\n"
            f"Took:        {took} seconds\n"
            f"{stdout}"
            f"{stderr}"
        )

        if (result.exit_status == 1) and raise_exception:
            raise Exception(f"Command - {command} returned 1 result code!")

        return result


class Gathered(Task):
    async def run(self):
        await asyncio.gather(*[task(self.host).run() for task in self.tasks])


def new_gathered_task(tasks: list) -> Gathered:
    """
    Task definitions are classes, not instances, hence why we require this.

    :param tasks: A list of Task objects to execute.
    """
    name = "+".join([task.__name__ for task in tasks])
    return type(name, (Gathered,), {"tasks": tasks})
