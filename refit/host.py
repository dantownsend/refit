import asyncio
import math
import time
import typing as t

import asyncssh
from termcolor import colored

from .task import Task


class ConnectionPool:
    def __init__(self, username, host):
        self.username = username
        self.host = host

        self.connections = []

    async def get_connection(self):
        """
        Turns out each connection can have multiple sessions, so having
        multiple connections isn't required.

        There might be benefits in the future, hence why this is being kept.
        """
        if not self.connections:
            connection = await asyncio.wait_for(
                asyncssh.connect(self.host, username=self.username), 10
            )

            self.connections.append(connection)

        return self.connections[0]

    def close(self):
        """
        Close all the connections.
        """
        print("closing ...")
        for connection in self.connections:
            connection.close()
        print("closed...")


class Host:

    # Override in subclasses:
    username: t.Optional[str] = None
    host: t.Optional[str] = None
    environment_vars: t.Dict[str, t.Any] = {}

    def __init__(self, tasks: t.Iterable[t.Type[Task]]):
        self.tasks = tasks

        if (not self.username) or (not self.host):
            raise ValueError("Define user and host!")

        self.connection_pool = ConnectionPool(self.username, self.host)

    def get_connection(self):
        return self.connection_pool.get_connection()

    async def entrypoint(self):
        message = f"Running tasks for {self.host}"
        line_length = int((100 - len(message)) / 2)
        line = "".join(["=" for i in range(line_length)])
        print(colored(f"{line} {message} {line}", "magenta"))
        await self.run()

    async def run(self):
        start_time = time.time()

        # The top level of self.tasks is synchronous, hence why it's in a
        # loop and not asyncio.gather.
        for task in self.tasks:
            await task(self).entrypoint()

        time_taken = math.floor(time.time() - start_time)
        print(colored(f"Tasks tooks {time_taken} seconds", "blue"))

        self.connection_pool.close()
