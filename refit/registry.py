from .task import new_gathered_task, Task


class TaskRegistry:
    def __init__(self):
        self.members = []

    def gather(self, *tasks: Task) -> None:
        """
        Register tasks, which will execute concurrently.
        """
        self.members.append(new_gathered_task(tasks))

    def register(self, *members) -> None:
        """
        Register tasks for execution.
        """
        self.members.extend(members)
        # If used as a decorator:
        return self.members[0]


class HostRegistry:
    def __init__(self):
        self.members = {"production": [], "test": []}

    def register(self, environment: str = "production", *members) -> None:
        """
        Register hosts as possible deployment targets.
        """
        if members:
            self.members[environment].extend(members)
            return

        # If used as a decorator
        def _register(*members):
            self.members[environment].extend(members)

        return _register
