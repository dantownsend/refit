import importlib
import math
import time
import typing as t
from collections import defaultdict

from termcolor import colored

from .host import Host
from .task import new_gathered_task, Task


class CommandRegistry:
    def __init__(self, deployments: t.Dict[str, str]):
        self.commands = deployments
        self.command_funcs = {}

        for deployment_name, path in deployments.items():
            module_path, func_name = path.split(":")
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            self.command_funcs[deployment_name] = func


class TaskRegistry:
    def __init__(self, host_registry):
        self.tasks = []
        self.host_registry = host_registry

    def print_tasks(self):
        print("\n".join([i.__class__.__name__ for i in self.tasks]))

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

    async def run(self, environment: str):
        """
        Execute the tasks for each matching host.
        """
        start_time = time.time()

        for task in self.tasks:
            await task.create(
                host_registry=self.host_registry, environment=environment
            )

        time_taken = math.floor(time.time() - start_time)
        print(colored(f"Tasks tooks {time_taken} seconds", "blue"))


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
