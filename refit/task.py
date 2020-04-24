from __future__ import annotations

from abc import abstractmethod
import asyncio
from contextvars import ContextVar
import time
import typing as t

from termcolor import colored

from .mixins.apt import AptMixin
from .mixins.docker import DockerMixin
from .mixins.file import FileMixin
from .mixins.path import PathMixin
from .mixins.python import PythonMixin
from .mixins.template import TemplateMixin

if t.TYPE_CHECKING:
    from .registry import HostRegistry
    from .host import Host


class Task(
    AptMixin, DockerMixin, FileMixin, PathMixin, PythonMixin, TemplateMixin
):
    def __init__(
        self, tags: t.List[str] = ["all"], sub_tasks: t.List[Task] = []
    ):
        self.tags = tags
        self.sub_tasks = sub_tasks
        self._host: ContextVar = ContextVar("host", default=None)

    async def create(
        self, host_registry: HostRegistry, environment: str
    ) -> None:
        """
        Creates and runs a task for all matching hosts.
        """
        hosts = host_registry.get_hosts(
            tags=self.tags, environment=environment
        )

        for host in hosts:
            host.start_connection_pool()

        await asyncio.gather(*[self.entrypoint(host=host) for host in hosts])

        for host in hosts:
            host.close_connection_pool()

    @property
    def host(self) -> Host:
        return self._host.get()

    async def entrypoint(self, host: Host):
        """
        Kicks off the task, along with printing some info.
        """
        message = f"{self.__class__.__name__} [{host.address}]"
        line_length = int((100 - len(message)) / 2)
        line = "".join(["-" for i in range(line_length)])
        print(colored(f"{line} {message} {line}", "cyan"))

        self._host.set(host)

        await self.run()

    ###########################################################################

    @abstractmethod
    async def run(self) -> None:
        """
        Override in subclasses. This is what does the actual work in the task,
        and is awaited when the Task is run.
        """
        pass

    ###########################################################################

    async def raw(self, command: str, raise_exception=True):
        """
        Execute a raw shell command on the remote server.
        """
        return await self._execute_command(command, raise_exception)

    ###########################################################################

    def _print_command(self, command: str) -> None:
        print(colored(f"{command}", "green"))

    async def _execute_command(self, command: str, raise_exception=True):
        """
        Runs the command on the host.
        """
        started_at = time.time()
        connection = await self.host.get_connection()

        result = await connection.run(
            command,
            # check=True
        )
        finished_at = time.time()
        took = round(finished_at - started_at, 4)

        self._print_command(f"Running: {command}")

        stdout = colored(result.stdout, "magenta")
        stderr = colored(result.stderr, "red")

        print(f"Took: {took} seconds\n{stdout}\n{stderr}\n")

        if (result.exit_status == 1) and raise_exception:
            raise Exception(f"Command - {command} returned 1 result code!")

        return result


class Concurrent(Task):
    """
    Bundles several tasks to be run concurrently.
    """

    async def run(self):
        await asyncio.gather(
            *[
                task(host_class=self.host_class).run()
                for task in self.sub_tasks
            ]
        )


def new_gathered_task(tasks: t.Iterable[Task]) -> t.Type[Concurrent]:
    """
    Task definitions are classes, not instances, hence why we require this.

    :param tasks: A list of Task classes to execute.
    """
    name = "+".join([task.__class__.__name__ for task in tasks])
    return type(name, (Concurrent,), {"sub_tasks": tasks})
