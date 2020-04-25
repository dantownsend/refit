import asyncio
import os
import sys

from targ import CLI
import uvloop

from refit.registry import CommandRegistry
from refit.scaffold import scaffold as _scaffold


def alter_path():
    sys.path = [os.getcwd()] + sys.path


alter_path()


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def init(name: str):
    """
    Creates a project template.

    :param name:
        The name of the new app to create.

    """
    _scaffold(name)


def command_line():
    cli = CLI(description="Refit CLI")
    cli.register(init)

    import refit_conf

    COMMAND_REGISTRY: CommandRegistry = getattr(refit_conf, "COMMAND_REGISTRY")

    for command_name, func in COMMAND_REGISTRY.command_funcs.items():
        cli.register(func, command_name=command_name)

    cli.run()


if __name__ == "__main__":
    command_line()
