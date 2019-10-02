import asyncio
import importlib
import sys
import typing as t

import click
from termcolor import colored
import uvloop

from .task import Task
from .host import Host
from .scaffold import scaffold as _scaffold


async def run_hosts(tasks: t.List[Task], hosts: t.List[Host]) -> None:
    await asyncio.gather(*[host(tasks).entrypoint() for host in hosts])


@click.group()
def cli():
    pass


@cli.command()
@click.argument("deployment_name")
def scaffold(deployment_name) -> None:
    """
    Creates a deployment template.
    """
    print(deployment_name)
    _scaffold(deployment_name)


@cli.command()
@click.argument("deployment_name")
@click.option(
    "-e", "--environment", default="production", help="production or test"
)
def deploy(deployment_name: str, environment: str) -> None:
    """
    Starts running your deployment tasks.
    """
    breakpoint()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    tasks_module = importlib.import_module(
        f"deployments.{deployment_name}.tasks"
    )
    hosts_module = importlib.import_module(
        f"deployments.{deployment_name}.hosts"
    )

    hosts = hosts_module.host_registry.members.get(environment)

    if not hosts:
        print(colored(f"No hosts defined for {environment}!", "red"))
        sys.exit(1)
    else:
        print(
            colored(f"Deploying {deployment_name} to {environment}", "green")
        )

    for host in hosts:
        host.environment = environment

    loop.run_until_complete(
        run_hosts(tasks_module.task_registry.members, hosts)
    )


if __name__ == "__main__":
    cli()
