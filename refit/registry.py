import math
import time
import typing as t
from collections import defaultdict

from termcolor import colored

from .host import Host
from .task import new_gathered_task, Task


class TaskRegistry:
    def __init__(self, host_registry):
        self.tasks = []

    def gather(self, *tasks: Task, tags: t.List[str] = ["all"]) -> None:
        """
        Register tasks, which will execute concurrently.
        """
        self.tasks.append(new_gathered_task(tasks))

    def register(self, *tasks: Task, tags: t.List[str] = ["all"]):
        """
        Register tasks for execution - used either directly, or as a decorator.
        """
        for task in tasks:
            task.tags = tags
        self.tasks.extend(tasks)


class HostRegistry:
    def __init__(self):
        self.host_map: t.Dict[str, t.List[Host]] = defaultdict(
            list, {"production": [], "test": []}
        )

    def register(
        self, *hosts, environment: str = "production", tags: t.List[str] = []
    ):
        """
        Register hosts as possible deployment targets.
        """
        for host in hosts:
            host.tags = tags
        self.host_map[environment].extend(hosts)

    def get_hosts(
        self, environment: str, tags: t.List[str]
    ) -> t.Sequence[Host]:
        """
        Returns hosts matching the given tags.

        If no tags are given, all hosts match.
        """
        hosts = self.host_map[environment]
        if "all" in tags:
            return hosts
        else:
            output: t.List[Host] = []
            for host in hosts:
                if set(host.tags).intersection(set(tags)):
                    output.append(host)
            return output

    async def run_tasks(self, tasks: t.List[Task], environment: str):
        """
        Create and execute a Task for each matching host.
        """
        start_time = time.time()

        for task in tasks:
            await task.create(host_registry=self, environment=environment)

        time_taken = math.floor(time.time() - start_time)
        print(colored(f"Tasks tooks {time_taken} seconds", "blue"))
