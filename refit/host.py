from __future__ import annotations

import asyncio
import math
import time
import typing as t

import asyncssh
from termcolor import colored

if t.TYPE_CHECKING:
    from .task import Task


class ConnectionPool:
    def __init__(self, username, host, **connection_params):
        self.username = username
        self.address = host
        self.connection_params = connection_params

        self.connections = []

    async def get_connection(self):
        """
        Turns out each connection can have multiple sessions, so having
        multiple connections isn't required.

        There might be benefits in the future, hence why this is being kept.
        """
        if not self.connections:
            connection = await asyncio.wait_for(
                asyncssh.connect(
                    self.address,
                    username=self.username,
                    **self.connection_params
                ),
                10,
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
    address: t.Optional[str] = None
    environment_vars: t.Dict[str, t.Any] = {}
    environment: t.Optional[str] = None
    connection_params: t.Dict[str, t.Any] = {}
    tags: t.Iterable[str] = []

    connection_pool: t.Optional[ConnectionPool] = None

    @classmethod
    def get_connection(self):
        return self.connection_pool.get_connection()

    @classmethod
    def start_connection_pool(cls):
        if (not cls.username) or (not cls.address):
            raise ValueError("Define username and address!")

        cls.connection_pool = ConnectionPool(
            cls.username, cls.address, **cls.connection_params
        )

    @classmethod
    def close_connection_pool(cls):
        cls.connection_pool.close()
