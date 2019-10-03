Task Sequencing
===============

You can use Refit to execute commands sequentially on a single server. However,
much of it's power is in running several commands at the same time - either on
a single machine, or across multiple machines.

TaskRegistry
------------

Instead of adding your ``Task`` to the ``TaskRegistry`` using the decorator
syntax, you can also use ``register`` or ``gather``.

register
~~~~~~~~

This tells the task registry to execute the given tasks sequentially.

.. code-block:: python

    from ..shared.tasks import AddKeysTask, CreateDatabaseTask

    task_registry = TaskRegistry()
    task_registry.register(AddKeysTask, CreateDatabaseTask)

gather
~~~~~~

This tells the task registry to execute the given tasks concurrently.

.. code-block:: python

    from ..shared.tasks import AddKeysTask, CreateDatabaseTask

    task_registry = TaskRegistry()
    task_registry.gather(AddKeysTask, CreateDatabaseTask)
