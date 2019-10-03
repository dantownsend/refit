import typing as t

from .task import new_gathered_task, Task


class TaskRegistry:
    def __init__(self):
        self.members = []

    def gather(self, *tasks: t.Type[Task]) -> None:
        """
        Register tasks, which will execute concurrently.
        """
        self.members.append(new_gathered_task(tasks))

    def register(
        self, labels: t.Iterable[str] = [], *members: t.Type[Task]
    ) -> t.Callable:
        """
        Register tasks for execution - used either directly, or as a decorator.
        """
        # Used as a function.
        if members:
            for member in members:
                member.labels = labels
            self.members.extend(members)
            # This does nothing - just for type inference.
            return lambda x: None

        # Used as a decorator
        def _register(member: t.Type[Task]):
            member.labels = labels
            self.members.append(member)

        return _register


class HostRegistry:
    def __init__(self):
        self.members = {"production": [], "test": []}

    def register(
        self, environment: str = "production", *members
    ) -> t.Optional[t.Callable]:
        """
        Register hosts as possible deployment targets.
        """
        if members:
            self.members[environment].extend(members)
            return None

        # If used as a decorator
        def _register(*members):
            self.members[environment].extend(members)

        return _register
