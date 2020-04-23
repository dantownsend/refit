import asyncio
import importlib
import os
import sys
import typing as t

from targ import CLI
from termcolor import colored
import uvloop

from refit.task import Task
from refit.host import Host
from refit.registry import HostRegistry, TaskRegistry
from refit.scaffold import scaffold as _scaffold


def alter_path():
    sys.path = [os.getcwd()] + sys.path


def scaffold(deployment_name: str):
    """
    Creates a deployment template.

    :param deployment_name:
        The name of the new deployment to create.

    """
    alter_path()
    print(deployment_name)
    _scaffold(deployment_name)


def deploy(deployment_name: str, environment: str = 'production'):
    """
    Starts running your deployment tasks.

    :param deployment_name:
        The deployment to deploy.
    :param environment:
        For example 'production' or 'test'.

    """
    alter_path()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    tasks_module = importlib.import_module(
        f"deployments.{deployment_name}.tasks"
    )
    hosts_module = importlib.import_module(
        f"deployments.{deployment_name}.hosts"
    )

    host_registry: HostRegistry = getattr(hosts_module, "host_registry", None)
    if not host_registry:
        raise Exception("Can't find 'host_registry' in hosts file.")

    hosts = host_registry.host_class_map.get(environment)

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

    asyncio.run(
        host_registry.run_tasks(
            tasks=task_registry.task_classes, environment=environment
        )
    )


def command_line():
    cli = CLI(description="Refit CLI")
    cli.register(scaffold)
    cli.register(deploy)
    cli.run()


if __name__ == "__main__":
    command_line()
