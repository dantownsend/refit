from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
import typing as t

import asyncssh


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


@dataclass
class Host:
    name: str
    username: t.Optional[str] = None
    address: t.Optional[str] = None
    environment_vars: t.Dict[str, t.Any] = field(default_factory=dict)
    environment: t.Optional[str] = None
    connection_params: t.Dict[str, t.Any] = field(default_factory=dict)
    tags: t.List[str] = field(default_factory=list)

    connection_pool: t.Optional[ConnectionPool] = None

    def get_connection(self):
        return self.connection_pool.get_connection()

    def start_connection_pool(self):
        if (not self.username) or (not self.address):
            raise ValueError("Define username and address!")

        self.connection_pool = ConnectionPool(
            self.username, self.address, **self.connection_params
        )

    def close_connection_pool(self):
        self.connection_pool.close()
