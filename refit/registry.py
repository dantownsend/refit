from functools import wraps
import math
import time
import typing as t
from collections import defaultdict

from termcolor import colored

from .host import Host
from .task import new_gathered_task, Task


class TaskRegistry:
    def __init__(self):
        self.task_classes = []

    def gather(
        self, *task_classes: t.Type[Task], tags: t.Iterable[str] = ["all"]
    ) -> None:
        """
        Register tasks, which will execute concurrently.
        """
        self.task_classes.append(new_gathered_task(task_classes))

    def register(
        self, *task_classes: t.Type[Task], tags: t.Iterable[str] = ["all"]
    ) -> t.Union[t.Callable, t.Type[Task]]:
        """
        Register tasks for execution - used either directly, or as a decorator.
        """
        # Used as a function.
        if task_classes:
            for task_class in task_classes:
                task_class.tags = tags
            self.task_classes.extend(task_classes)
            return task_classes[0]

        # Used as a decorator
        def _register(task_class: t.Type[Task]) -> t.Type[Task]:
            task_class.tags = tags
            self.task_classes.append(task_class)
            return Task

        return _register


class HostRegistry:
    def __init__(self):
        self.host_class_map: t.Dict[str, t.List[t.Type[Host]]] = defaultdict(
            list, {"production": [], "test": []}
        )

    def register(
        self,
        *host_classes,
        environment: str = "production",
        tags: t.Iterable[str] = [],
    ) -> t.Union[t.Callable, t.Type[Host]]:
        """
        Register hosts as possible deployment targets.
        """
        # Used as a function
        if host_classes:
            for host_class in host_classes:
                host_class.tags = tags
            self.host_class_map[environment].extend(host_classes)
            return host_classes[0]

        # Used as a decorator
        def _register(host_class: t.Type[Host]):
            host_class.tags = tags
            self.host_class_map[environment].append(host_class)

        return _register

    def get_host_classes(
        self, environment: str, tags: t.Iterable[str]
    ) -> t.Sequence[t.Type[Host]]:
        """
        Returns hosts matching the given tags.

        If no tags are given, all hosts match.
        """
        hosts = self.host_class_map[environment]
        if "all" in tags:
            return hosts
        else:
            output: t.List[t.Type[Host]] = []
            for host in hosts:
                if set(host.tags).intersection(set(tags)):
                    output.append(host)
            return output

    async def run_tasks(
        self, tasks: t.List[t.Type[Task]], environment: str
    ) -> None:
        """
        Create and execute a Task for each matching host.
        """

        start_time = time.time()

        for _Task in tasks:
            await _Task.create(host_registry=self, environment=environment)

        time_taken = math.floor(time.time() - start_time)
        print(colored(f"Tasks tooks {time_taken} seconds", "blue"))
