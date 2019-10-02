from .task import new_gathered_task


class TaskRegistry():

    def __init__(self):
        self.members = []

    def gather(self, *tasks):
        """
        Makes the tasks operate concurrently.
        """
        self.members.append(
            new_gathered_task(tasks)
        )

    def register(self, *members):
        """
        Helper for registering tasks / hosts etc.

        """
        self.members.extend(members)
        # If used as a decorator:
        return self.members[0]


class HostRegistry():

    def __init__(self):
        self.members = {
            'production': [],
            'test': []
        }

    def register(self, environment: str = 'production', *members):
        """
        Helper for registering tasks / hosts etc.

        """
        if members:
            self.members[environment].extend(members)
            return

        # If used as a decorator
        def _register(*members):
            self.members[environment].extend(members)

        return _register
