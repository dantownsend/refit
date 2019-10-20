import asyncio
import importlib
import sys
import typing as t

import click
from termcolor import colored
import uvloop

from .task import Task
from .host import Host
from .registry import HostRegistry, TaskRegistry
from .scaffold import scaffold as _scaffold


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
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    tasks_module = importlib.import_module(
        f"deployments.{deployment_name}.tasks"
    )
    hosts_module = importlib.import_module(
        f"deployments.{deployment_name}.hosts"
    )

    host_registry: HostRegistry = getattr(hosts_module, "host_registry", None)
    if not host_registry:
        raise Exception("Can't find 'host_registry' in hosts file.")

    hosts = host_registry.hosts.get(environment)

    if not hosts:
        print(colored(f"No hosts defined for {environment}!", "red"))
        sys.exit(1)
    else:
        print(
            colored(f"Deploying {deployment_name} to {environment}", "green")
        )

    for host in hosts:
        host.environment = environment

    task_registry: TaskRegistry = getattr(tasks_module, "task_registry", None)
    if not task_registry:
        raise Exception("Can't find 'task_registry' in tasks file.")

    loop.run_until_complete(
        host_registry.run_tasks(
            tasks=task_registry.task_classes, environment=environment
        )
    )


if __name__ == "__main__":
    cli()
